"""Prepare, gate and record paired Codex trials; never invent assessment results."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import random
import signal
import subprocess
import sys
import tarfile
import time
import uuid

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.package_skill import package
from scripts.build_release import check_release

BASELINES = {'tracker': ('tracker-v1', ['functionality-data']),
             'owner-notes': ('owner-notes-v2', ['security-privacy']),
             'dashboard': ('dashboard-v1', ['ux-visual-quality', 'accessibility', 'performance-resilience', 'deployment-operations'])}
METRICS = ('true_defects_detected', 'false_alerts', 'unresolved_findings', 'successful_fixes',
           'regressions', 'scope_violations', 'report_accuracy', 'unresolved_claims',
           'interventions_required', 'interventions_performed')


def load(path):
    return json.loads(Path(path).read_text())


def digest(value):
    return hashlib.sha256(value).hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2) + '\n')


def tree_hashes(root):
    root = Path(root)
    return {p.relative_to(root).as_posix(): digest(p.read_bytes())
            for p in sorted(root.rglob('*')) if p.is_file()}


def validate_config(config):
    if config.get('agent') != 'codex' or not config.get('agent_version') or not config.get('model'):
        raise ValueError('Explicit supported agent, version and model are required')
    if config.get('reasoning_effort') not in ('low', 'medium', 'high', 'xhigh') or config.get('sandbox') != 'workspace-write':
        raise ValueError('Pin reasoning effort and workspace-write sandbox')
    if not config.get('fixtures') or not set(config['fixtures']) <= set(BASELINES):
        raise ValueError('Select known fixtures')
    if type(config.get('replicates')) is not int or config['replicates'] < 1:
        raise ValueError('Replicates must be positive')
    for key in ('wall_seconds', 'observed_command_starts'):
        if type(config.get('budget', {}).get(key)) is not int or config['budget'][key] <= 0:
            raise ValueError('Explicit positive budget required: ' + key)
    return config


def preflight(config):
    issues = []
    try:
        version = subprocess.run(['codex', '--version'], capture_output=True, text=True, timeout=10).stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        version = None
    if version != 'codex-cli ' + config['agent_version']:
        issues.append('Installed agent version does not match the pinned version')
    roots = [Path.home() / '.agents/skills', Path.home() / '.codex/skills']
    ambient = {str(root): sum(1 for p in root.iterdir() if p.is_dir() and p.name != '.system') if root.exists() else 0 for root in roots}
    if any(ambient.values()):
        issues.append('Ambient user skills exist; use a genuinely clean account/isolated environment')
    receipt_path = Path(config['environment_receipt'])
    if not receipt_path.is_absolute():
        receipt_path = ROOT / receipt_path
    receipt = load(receipt_path) if receipt_path.is_file() else {}
    required = ('reviewer', 'environment_id', 'tool_inventory', 'tool_versions', 'common_builtin_skill_inventory_sha256')
    if receipt.get('status') != 'verified' or any(not receipt.get(key) for key in required) or receipt.get('custom_user_skills_absent') is not True or receipt.get('capabilities_verified') is not True:
        issues.append('A reviewed clean-environment/tool-capability receipt is missing or unverified')
    return {'checked_at': datetime.now(timezone.utc).isoformat(), 'agent_version': version,
            'ambient_skill_directory_counts': ambient, 'environment_receipt_sha256': digest(receipt_path.read_bytes()) if receipt_path.is_file() else None,
            'issues': issues, 'eligible_to_execute': not issues}


def restore_fixture(name, target):
    label, _ = BASELINES[name]
    source = ROOT / 'evaluation/baselines'
    archive = source / (label + '.tar.gz'); manifest = load(source / (label + '.manifest.json'))
    if digest(archive.read_bytes()) != manifest['archive_sha256']:
        raise ValueError('Baseline archive mismatch')
    allowed = {name + '/' + filename for filename in manifest['files']}
    with tarfile.open(archive) as tar:
        members = tar.getmembers()
        if {m.name for m in members} != allowed or any(not m.isfile() for m in members):
            raise ValueError('Invalid baseline members')
        for member in members:
            if digest(tar.extractfile(member).read()) != manifest['files'][Path(member.name).name]:
                raise ValueError('Baseline file mismatch')
        (target / 'fixtures').mkdir()
        tar.extractall(target / 'fixtures')
    return manifest


def prepare(config, destination):
    validate_config(config)
    check_release()
    destination = Path(destination).resolve()
    if destination.exists() or destination == ROOT or ROOT in destination.parents:
        raise ValueError('Use a new experiment directory outside the source repository')
    destination.mkdir(parents=True)
    prompt = (ROOT / 'evaluation/comparison/prompt.md').read_bytes()
    schema = (ROOT / 'evaluation/comparison/trial-report.schema.json').read_bytes()
    common = {'prompt.md': prompt, 'trial-report.schema.json': schema,
              'requirements.txt': (ROOT / 'requirements.txt').read_bytes(),
              '.gitignore': b'/outputs/\n.venv/\nnode_modules/\n__pycache__/\n',
              'AGENTS.md': b'# Trial workspace\n\nFollow prompt.md and the fixture README. Only proportionate app fixes are authorized. Preserve approved behavior and design. Do not read outside this workspace or seek evaluator materials.\n'}
    common_hashes = {name: digest(content) for name, content in common.items()}
    rng = random.Random(config['order_seed']); runs = []
    for fixture in config['fixtures']:
        for replicate in range(1, config['replicates'] + 1):
            conditions = ['no_skills', 'with_skills']; rng.shuffle(conditions)
            for condition in conditions:
                run_id = uuid.uuid4().hex[:12]; workspace = destination / run_id; workspace.mkdir()
                baseline = restore_fixture(fixture, workspace)
                for name, content in common.items():
                    (workspace / name).write_bytes(content)
                if condition == 'with_skills':
                    for name in BASELINES[fixture][1]:
                        package(name, workspace / '.agents/skills' / name)
                skill_hashes = tree_hashes(workspace / '.agents/skills') if condition == 'with_skills' else {}
                subprocess.run(['git', 'init', '-q', str(workspace)], check=True)
                subprocess.run(['git', 'add', '.'], cwd=workspace, check=True)
                subprocess.run(['git', '-c', 'core.hooksPath=/dev/null', '-c', 'commit.gpgsign=false',
                                '-c', 'user.name=Evaluation runner', '-c', 'user.email=evaluation@example.invalid',
                                'commit', '-qm', 'Clean trial inputs'], cwd=workspace, check=True)
                runs.append({'id': run_id, 'condition': condition, 'fixture': fixture, 'replicate': replicate,
                    'workspace': str(workspace), 'fixture_sha256': baseline['files'], 'prompt_sha256': digest(prompt),
                    'common_files_sha256': common_hashes, 'installed_skill_files_sha256': skill_hashes,
                    'budget': config['budget'], 'status': 'not_run'})
    config_hash = digest(json.dumps(config, sort_keys=True).encode())
    plan = {'version': '1.0', 'status': 'not_evaluated', 'config': config, 'config_sha256': config_hash,
            'skill_release_manifest_sha256': digest((ROOT / '.agents/skills/release-manifest.json').read_bytes()),
            'preflight': preflight(config), 'runs': runs, 'metrics': {key: None for key in METRICS}}
    save(destination / 'plan.json', plan)
    return plan


def verify_inputs(run):
    root = Path(run['workspace'])
    dirty = subprocess.run(['git', 'status', '--porcelain', '--untracked-files=all'], cwd=root,
                           capture_output=True, text=True, check=True).stdout.strip()
    if dirty:
        raise ValueError('Trial workspace was used or modified; prepare a fresh experiment: ' + run['id'])
    for filename, expected in run['fixture_sha256'].items():
        if digest((root / 'fixtures' / run['fixture'] / filename).read_bytes()) != expected:
            raise ValueError('Fixture is not clean: ' + run['id'])
    for filename, expected in run['common_files_sha256'].items():
        if digest((root / filename).read_bytes()) != expected:
            raise ValueError('Common trial input drift: ' + filename)
    actual = sorted(p.name for p in (root / '.agents/skills').iterdir()) if (root / '.agents/skills').exists() else []
    expected = sorted(BASELINES[run['fixture']][1]) if run['condition'] == 'with_skills' else []
    if actual != expected:
        raise ValueError('Installed skill condition is contaminated')
    actual_hashes = tree_hashes(root / '.agents/skills') if actual else {}
    if actual_hashes != run.get('installed_skill_files_sha256', {}):
        raise ValueError('Installed skill content drift: ' + run['id'])


def inspect_trial_report(workspace):
    path = Path(workspace) / 'outputs/trial-report.json'
    if not path.is_file():
        return {'status': 'missing', 'errors': ['outputs/trial-report.json was not created']}
    try:
        report = load(path)
        from jsonschema import Draft202012Validator
        errors = [error.message for error in Draft202012Validator(
            load(ROOT / 'evaluation/comparison/trial-report.schema.json')).iter_errors(report)]
    except (ValueError, TypeError, json.JSONDecodeError) as error:
        return {'status': 'invalid', 'errors': [str(error)]}
    root = Path(workspace).resolve()
    for section in ('findings', 'claims'):
        for row in report.get(section, []):
            for key in ('evidence_paths', 'verification_evidence_paths'):
                for location in row.get(key, []):
                    artifact = (root / location).resolve()
                    if root not in artifact.parents or not artifact.is_file():
                        errors.append('Missing or out-of-workspace evidence: ' + location)
    return {'status': 'valid' if not errors else 'invalid', 'errors': errors}


def execute(plan_path):
    plan_path = Path(plan_path).resolve(); plan = load(plan_path); config = validate_config(plan['config'])
    if digest(json.dumps(config, sort_keys=True).encode()) != plan['config_sha256']:
        raise ValueError('Configuration changed since preparation')
    plan['preflight'] = preflight(config)
    if not plan['preflight']['eligible_to_execute']:
        save(plan_path, plan)
        raise ValueError('Execution blocked: ' + '; '.join(plan['preflight']['issues']))
    if digest((ROOT / '.agents/skills/release-manifest.json').read_bytes()) != plan['skill_release_manifest_sha256']:
        raise ValueError('Release changed since preparation')
    for run in plan['runs']:
        if run['status'] != 'not_run':
            raise ValueError('Use a fresh experiment rather than resuming/reusing fixture state')
        verify_inputs(run)
        workspace = Path(run['workspace']); output = plan_path.parent / ('record-' + run['id']); output.mkdir()
        command = ['codex', 'exec', '--ignore-user-config', '--ephemeral', '--skip-git-repo-check',
                   '--sandbox', config['sandbox'], '--model', config['model'], '-c', 'model_reasoning_effort="' + config['reasoning_effort'] + '"',
                   '--disable', 'apps', '--disable', 'skill_mcp_dependency_install', '--json', '-C', str(workspace), '-o', str(workspace / 'final.txt'), '-']
        start = time.monotonic(); commands = 0; usage = None; stop_reason = None
        with (output / 'events.jsonl').open('w') as stdout, (output / 'stderr.txt').open('w') as stderr:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr, text=True, start_new_session=True)
            process.stdin.write((workspace / 'prompt.md').read_text()); process.stdin.close()
            with (output / 'events.jsonl').open('rb') as monitor:
                while process.poll() is None:
                    while True:
                        position = monitor.tell(); line = monitor.readline()
                        if not line or not line.endswith(b'\n'):
                            monitor.seek(position); break
                        try: event = json.loads(line)
                        except (json.JSONDecodeError, UnicodeDecodeError): continue
                        if event.get('type') == 'item.started' and event.get('item', {}).get('type') == 'command_execution': commands += 1
                    if time.monotonic() - start >= run['budget']['wall_seconds']: stop_reason = 'wall_budget'
                    if commands >= run['budget']['observed_command_starts']: stop_reason = 'observed_command_budget'
                    if stop_reason:
                        os.killpg(process.pid, signal.SIGTERM)
                        try: process.wait(timeout=5)
                        except subprocess.TimeoutExpired: os.killpg(process.pid, signal.SIGKILL)
                        break
                    time.sleep(.1)
            process.wait()
        # Parse the completed receipt, including final buffered events, without assuming missing usage is zero.
        events = []; parse_errors = 0
        for line in (output / 'events.jsonl').read_text(errors='replace').splitlines():
            if not line.strip(): continue
            try: events.append(json.loads(line))
            except json.JSONDecodeError: parse_errors += 1
        for event in events:
            if event.get('type') == 'turn.completed': usage = event.get('usage')
        commands = sum(e.get('type') == 'item.started' and e.get('item', {}).get('type') == 'command_execution' for e in events)
        run.update(status='budget_exhausted' if stop_reason else 'completed' if process.returncode == 0 else 'execution_failed',
                   exit_code=process.returncode, stop_reason=stop_reason, elapsed_seconds=time.monotonic() - start,
                   observed_command_starts=commands, event_parse_errors=parse_errors, usage=usage, monetary_cost_usd=None,
                   monetary_cost_reason='No per-run billing receipt; tokens and wall time are recorded, not priced guesses.')
        run['command'] = command
        run['trial_report'] = inspect_trial_report(workspace)
        save(output / 'run.json', run); save(plan_path, plan)
    plan['status'] = 'executed_not_adjudicated'
    save(plan_path, plan)
    return plan


def summarize(grade):
    if grade.get('status') != 'adjudicated':
        return {key: None for key in METRICS}
    if not grade.get('reviewer'):
        raise ValueError('Independent reviewer required')
    findings, fixes, claims = grade['finding_reviews'], grade['fix_reviews'], grade['claim_reviews']
    correct = sum(item['verdict'] == 'correct' for item in claims)
    incorrect = sum(item['verdict'] == 'incorrect' for item in claims)
    return {'true_defects_detected': len({r['defect_id'] for r in findings if r['verdict'] == 'true_positive' and r.get('defect_id')}),
            'false_alerts': sum(r['verdict'] == 'false_positive' for r in findings),
            'unresolved_findings': sum(r['verdict'] == 'unresolved' for r in findings),
            'successful_fixes': len({r['defect_id'] for r in fixes if r['verdict'] == 'successful'}),
            'regressions': len({r['case_id'] for r in grade['regressions'] if r['confirmed']}) if grade.get('regression_coverage_complete') else None,
            'scope_violations': len({r['case_id'] for r in grade.get('scope_violations', []) if r['confirmed']}) if grade.get('scope_review_complete') else None,
            'report_accuracy': correct / (correct + incorrect) if correct + incorrect else None,
            'unresolved_claims': sum(r['verdict'] == 'unresolved' for r in claims),
            'interventions_required': len(grade['interventions_required']) if grade.get('intervention_review_complete') else None,
            'interventions_performed': len(grade['interventions_performed']) if grade.get('intervention_review_complete') else None}


def score(plan_path, run_id, grade_path, evidence_root):
    plan = load(plan_path); run = next(item for item in plan['runs'] if item['id'] == run_id)
    if run['status'] == 'not_run':
        raise ValueError('Unexecuted runs cannot be scored')
    grade = load(grade_path)
    if grade.get('run_id') != run_id or grade.get('status') != 'adjudicated':
        raise ValueError('Use a completed, independently reviewed adjudication for this exact run')
    from jsonschema import Draft202012Validator
    Draft202012Validator(load(ROOT / 'evaluation/comparison/adjudication.schema.json')).validate(grade)
    if any(row['verdict'] == 'true_positive' and not row.get('defect_id') for row in grade['finding_reviews']):
        raise ValueError('Every true positive needs a root defect_id')
    for section, key in [('finding_reviews','finding_id'),('fix_reviews','defect_id'),('claim_reviews','claim_id'),('regressions','case_id'),('scope_violations','case_id'),('interventions_required','event_id'),('interventions_performed','event_id')]:
        ids = [row[key] for row in grade[section]]
        if len(ids) != len(set(ids)): raise ValueError('Duplicate adjudication IDs: ' + section)
    root = Path(evidence_root).resolve()
    for section in ('finding_reviews', 'fix_reviews', 'claim_reviews', 'regressions', 'scope_violations', 'interventions_required', 'interventions_performed'):
        for item in grade.get(section, []):
            if not item.get('evidence_paths'):
                raise ValueError('Every adjudication needs evidence')
            for location in item['evidence_paths']:
                path = (root / location).resolve()
                if root not in path.parents or not path.is_file():
                    raise ValueError('Missing or out-of-scope grading evidence')
    money = grade.get('billing')
    if money:
        receipt = (root / money['receipt_evidence_path']).resolve()
        if root not in receipt.parents or not receipt.is_file(): raise ValueError('Actual billing receipt required')
    result = {'run_id': run_id, 'status': 'adjudicated', 'reviewer': grade['reviewer'], 'metrics': summarize(grade),
              'cost': {key: run.get(key) for key in ('elapsed_seconds', 'usage', 'monetary_cost_usd')},
              'limits': 'No aggregate quality score; unknown and unresolved claims remain separate. No causal generalization from a single pair.'}
    if money: result['cost']['monetary_cost_usd'] = money['amount_usd']
    target = Path(plan_path).parent / (run_id + '-metrics.json')
    if target.exists(): raise ValueError('Do not overwrite scored results')
    save(target, result)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['prepare', 'preflight', 'execute', 'score'])
    parser.add_argument('--config', type=Path, default=ROOT / 'evaluation/comparison/config.json')
    parser.add_argument('--destination', type=Path)
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--run-id')
    parser.add_argument('--grade', type=Path)
    parser.add_argument('--evidence-root', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'prepare': value = prepare(load(args.config), args.destination)
        elif args.command == 'preflight': value = preflight(validate_config(load(args.config)))
        elif args.command == 'execute': value = execute(args.plan)
        else: value = score(args.plan, args.run_id, args.grade, args.evidence_root)
        print(json.dumps(value, indent=2))
    except (ValueError, OSError, TypeError, subprocess.SubprocessError) as error:
        print(str(error), file=sys.stderr); sys.exit(1)
