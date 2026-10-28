import subprocess, json, datetime, pathlib
root=pathlib.Path('audits/standard-20261028')
commands=[['python3','-m','http.server','8765','--bind','127.0.0.1','--directory','tracker'], ['node','-e','const s=require("http").createServer(); s.on("error",e=>{console.error(e);process.exit(1)}); s.listen(8765,"127.0.0.1")'], ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--version'], ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome','--headless=new','--no-first-run','--no-default-browser-check','--remote-debugging-pipe','--user-data-dir='+str(root.resolve()/'chrome-profile'),'about:blank'], ['.venv/bin/python','scripts/audit.py','select','--profile',str(root/'profile.json'),'--level','Standard','--group','F'], ['.venv/bin/python','scripts/audit.py','template','--profile',str(root/'profile.json'),'--level','Standard','--group','F']]
results=[]
for cmd in commands:
 try:
  p=subprocess.run(cmd,capture_output=True,text=True,timeout=5)
  results.append(dict(command=cmd,returncode=p.returncode,stdout=p.stdout,stderr=p.stderr))
 except subprocess.TimeoutExpired as e:
  results.append(dict(command=cmd,timeout=True,stdout=str(e.stdout),stderr=str(e.stderr)))
(root/'tooling.json').write_text(json.dumps(dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(),results=results),indent=2))
