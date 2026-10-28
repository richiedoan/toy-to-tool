# Contributing

Contributions should preserve the evidence model and keep the installable release reproducible.

1. Create a focused branch and avoid committing credentials, production data, evaluator secrets or local virtual environments.
2. Edit canonical criteria in `criteria/v1.json`, schemas in `schemas/`, shared behavior in `scripts/audit.py`, and skill instructions in `authoring/<skill>/SKILL.md.in`.
3. Regenerate install-ready bundles with `python3 scripts/build_release.py --write`. Do not hand-edit generated `.agents/skills/<skill>/` files.
4. Add or update rejection and behavior tests. Do not weaken validation, remove failing tests, mark unexecuted checks as pass or replace blocker visibility with a total score.
5. Run:

   ```sh
   python3 scripts/audit.py validate
   python3 scripts/build_release.py
   python3 -m unittest discover -s tests -v
   ```

6. For packaging changes, test `npx skills add <repo> --list` and a copied installation into a new project. Record versions, commands, exits and limitations; do not invent support claims.
7. For comparison changes, never reuse a trial workspace. Keep model, prompt, base tools, fixture and budget identical across the pair. Evaluation answers must stay outside agent workspaces.

Pull requests should explain the motivation, affected criteria/skills, verification evidence, compatibility impact and remaining unknowns. By contributing, you agree that your contribution is licensed under the repository's MIT License.
