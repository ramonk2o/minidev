"""Scores outcome eval runs by their hidden acceptance tests.

usage: score.py <result.json from claude plugin eval --json> <outcome dir>

For each run it copies the src/ folder the run left (in the kept temp dir) to a
fresh folder, next to the case's hidden tests, and runs them with node --test.
The run's own files are only read, never executed in place.
"""
import json, os, re, shutil, subprocess, sys, tempfile

result, outcome = sys.argv[1], sys.argv[2]
data = json.load(open(result))
rows, totals = [], {}

def workspace(trace):
    root = os.path.dirname(os.path.dirname(trace))  # <tmp>/out/trace.jsonl -> <tmp>
    for d in (root, os.path.join(root, 'sealed')):
        if os.path.isdir(d):
            os.chmod(d, 0o700)
    return os.path.join(root, 'sealed', 'home', 'cwd')

def hidden_score(case, trace):
    hidden = os.path.join(outcome, case, 'hidden')
    src = os.path.join(workspace(trace), 'src') if trace else None
    if not src or not os.path.isdir(src):
        return None, 'no src/'
    tmp = tempfile.mkdtemp()
    shutil.copytree(src, os.path.join(tmp, 'src'))
    os.makedirs(os.path.join(tmp, 'test'))
    for f in os.listdir(hidden):
        shutil.copy(os.path.join(hidden, f), os.path.join(tmp, 'test', f))
    open(os.path.join(tmp, 'package.json'), 'w').write('{"type": "module"}\n')
    p = subprocess.run(['node', '--test', 'test/'], cwd=tmp, capture_output=True, text=True, timeout=120)
    out = p.stdout + p.stderr
    shutil.rmtree(tmp, ignore_errors=True)
    passed = int((re.search(r'^ℹ pass (\d+)', out, re.M) or [0, 0])[1])
    failed = int((re.search(r'^ℹ fail (\d+)', out, re.M) or [0, 0])[1])
    names = re.findall(r'^not ok \d+ - (.+)$', out, re.M)
    return (passed, passed + failed), '; '.join(names)

for c in data['cases']:
    case = c.get('name')
    for arm, runs in c.get('arms', {}).items():
        for i, r in enumerate(runs, 1):
            score, failed = hidden_score(case, r.get('tracePath'))
            cost = r.get('costUsd') or 0
            rows.append((case, arm, i, score, cost, failed))
            t = totals.setdefault((case, arm), [0, 0, 0.0, 0])
            if score:
                t[0] += score[0]; t[1] += score[1]
            t[2] += cost; t[3] += 1

print(f"{'case':<16} {'arm':<8} {'run':>3} {'hidden':>7} {'cost':>7}  failed")
for case, arm, i, score, cost, failed in rows:
    s = f'{score[0]}/{score[1]}' if score else '-'
    print(f'{case:<16} {arm:<8} {i:>3} {s:>7} {cost:>7.2f}  {failed}')
print()
for (case, arm), (p, n, cost, k) in totals.items():
    rate = f'{100 * p / n:.0f}%' if n else '-'
    print(f'{case:<16} {arm:<8} hidden tests {rate:>4}  mean cost ${cost / k:.2f}')
