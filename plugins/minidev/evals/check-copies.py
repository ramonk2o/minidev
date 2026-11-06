#!/usr/bin/env python3
"""Checks the text the evals copy by hand from the skills, so a change to the
source doesn't leave stale copies behind.

- The CLAUDE.md template in skills/setup/SKILL.md is copied into the trigger
  prompts (append_system_prompt) and into the fixture's CLAUDE.md
  (behavior/fixture.sh). Every copy that uses the cycle must hold the
  template's fixed lines (the ones with no <placeholder>) verbatim, and no line
  that starts like a template line may differ from it.
- outcome/patch.sh rewrites a sentence of that template: it must still be there.
- The unattended-run prompt is the same in every behavior and outcome case.
- The cycle check at the start of build, fix and chore is the same in the
  three, up to its last clause (what to do instead, which is each skill's own).

Run from plugins/minidev: python3 evals/check-copies.py
"""
import glob
import json
import re
import sys

ROOT = __file__.rsplit("/evals/", 1)[0]
problems = []


def template_lines():
    setup = open(f"{ROOT}/skills/setup/SKILL.md").read()
    block = setup.split("### Template", 1)[1].split("````markdown\n", 1)[1].split("````", 1)[0]
    return [l for l in block.splitlines() if l.strip()]


def system_prompt(path):
    text = open(path).read()
    m = re.search(r'^append_system_prompt: (".*")$', text, re.M)
    return json.loads(m.group(1)) if m else None


TEMPLATE = template_lines()
FIXED = [l for l in TEMPLATE if "<" not in l and not l.startswith("#")]


def key(line):
    # What a line starts with, before what a project fills in.
    return re.split(r"[:`]", line, 1)[0].strip()


KEYS = {key(l): l for l in FIXED}


def check_copy(name, text):
    if "uses the `minidev` cycle" not in text:
        return  # a project outside the cycle: nothing to match
    lines = text.splitlines()
    for fixed in FIXED:
        if fixed not in lines and key(fixed) not in {key(l) for l in lines}:
            problems.append(f"{name}: missing template line: {fixed}")
    for line in lines:
        k = key(line)
        if k in KEYS and line != KEYS[k]:
            problems.append(f"{name}: differs from the template:\n    copy:     {line}\n    template: {KEYS[k]}")


for path in sorted(glob.glob(f"{ROOT}/evals/triggers/*/prompt.md")):
    prompt = system_prompt(path)
    if prompt and "The project's CLAUDE.md says:" in prompt:
        check_copy(path[len(ROOT) + 1:], prompt)

fixture = open(f"{ROOT}/evals/behavior/fixture.sh").read()
m = re.search(r"cat > CLAUDE.md <<'EOF'\n(.*?)\nEOF", fixture, re.S)
if m:
    check_copy("evals/behavior/fixture.sh (CLAUDE.md)", m.group(1))
else:
    problems.append("evals/behavior/fixture.sh: no CLAUDE.md heredoc found")

patch = open(f"{ROOT}/evals/outcome/patch.sh").read()
for old in re.findall(r'c\.replace\("(.*?)",', patch):
    if not any(old in l for l in TEMPLATE):
        problems.append(f"evals/outcome/patch.sh: replaces text the template no longer has: {old}")

unattended = {}
for path in sorted(glob.glob(f"{ROOT}/evals/behavior/*/prompt.md") + glob.glob(f"{ROOT}/evals/outcome/*/prompt.md")):
    prompt = system_prompt(path)
    if prompt:
        unattended.setdefault(prompt, []).append(path[len(ROOT) + 1:])
if len(unattended) > 1:
    problems.append("the unattended-run prompt differs between cases:\n" + "\n".join(
        f"  {len(paths)} case(s), e.g. {paths[0]}: {prompt[:80]}…" for prompt, paths in unattended.items()))

cycle_checks = {}
for skill in ("build", "fix", "chore"):
    m = re.search(r"^First check that the project uses the cycle.*?or simply", open(f"{ROOT}/skills/{skill}/SKILL.md").read(), re.M)
    if m:
        cycle_checks.setdefault(m.group(0), []).append(skill)
    else:
        problems.append(f"skills/{skill}/SKILL.md: no cycle check paragraph found")
if len(cycle_checks) > 1:
    problems.append("the cycle check differs between skills (it should match up to \"or simply\"):\n" + "\n".join(
        f"  {', '.join(skills)}: {text}" for text, skills in cycle_checks.items()))

if problems:
    print("\n".join(problems))
    sys.exit(1)
print("copies match the sources")
