#!/usr/bin/env python3
"""Change history numbers for /minidev:checkup. Reads git; changes nothing.

Run from the project's root:

    python3 history.py [--since <commit>] [--last 200] [--top 10]
                       [--ref <branch>] [--git <path>]

It reads the first-parent history of the branch. A change is a commit there
that touches something other than a Markdown file: the cycle's document
commits (an idea noted, a feature set In progress, the check-up's own record)
aren't changes. It prints:

- the project's size: code and test files, and their lines;
- how many changes and fixes the history has, in all and since --since;
- the code files that change most, with how many of those changes were fixes;
- the folders where fixes concentrate;
- code files in different folders that change together.

Code files are the tracked text files that aren't documents, data, config or
lock files. A change counts as a fix when its subject starts with fix, bugfix,
hotfix or revert, or when its message has a "Regression tests:" block with
entries and no "Critical tests:" block with entries (the commit a fix leaves
on the main branch in the minidev cycle).

Python 3.8+, standard library only.
"""
import argparse
import collections
import itertools
import os
import re
import subprocess
import sys

NOT_CODE_EXT = {
    # documents
    ".md", ".mdx", ".txt", ".rst", ".adoc",
    # data and config
    ".json", ".jsonc", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env",
    ".csv", ".tsv", ".xml", ".svg", ".snap", ".lock", ".map",
}
NOT_CODE_NAME = {
    "package-lock.json", "yarn.lock", "pnpm-lock.yaml", "go.sum", "license",
    "licence", ".gitignore", ".gitattributes", ".editorconfig",
}
TEST_RE = re.compile(
    r"(^|/)(tests?|specs?|__tests__|e2e|testing|fixtures)(/|$)"
    r"|(^|/)test_[^/]*$"
    r"|[._-](test|spec)s?\.[^/.]+$",
    re.I,
)
FIX_SUBJECT = re.compile(r"^\s*(fix|bugfix|hotfix|revert)\b", re.I)
MAX_FILE_BYTES = 2_000_000
MAX_FILES_FOR_PAIRS = 30  # a change that touches more is a sweep, not coupling
MIN_TOGETHER = 3
MIN_SHARE = 0.5
FEW_CHANGES = 20
CHANGE_PATHS = ["--", ".", ":(exclude)*.md"]  # what makes a commit a change

GIT = "git"


def git(*args):
    result = subprocess.run([GIT, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.decode("utf-8", "replace").strip() or "git failed")
    return result.stdout.decode("utf-8", "replace")


def is_code(path):
    name = os.path.basename(path).lower()
    ext = os.path.splitext(name)[1]
    return name not in NOT_CODE_NAME and ext not in NOT_CODE_EXT


def is_test(path):
    return bool(TEST_RE.search(path))


def folder(path, depth=2):
    parts = path.split("/")[:-1]
    return "/".join(parts[:depth]) if parts else "(root)"


def block_has_entries(body, name):
    m = re.search(r"^" + re.escape(name) + r"[ \t]*\n((?:.+\n?)*)", body, re.M)
    if not m:
        return False
    lines = [line.strip() for line in m.group(1).splitlines() if line.strip()]
    return any(line.lower() != "(none)" for line in lines)


def is_fix(subject, body):
    if FIX_SUBJECT.match(subject):
        return True
    return block_has_entries(body, "Regression tests:") and not block_has_entries(body, "Critical tests:")


def read_changes(ref, last=None, names=True):
    """The branch's changes, newest first: (hash, date, subject, is_fix, files)."""
    args = ["log", "--first-parent", "--no-renames", "--date=short",
            "--format=%x1e%H%x1f%ad%x1f%s%x1f%b%x1d"]
    if names:
        args += ["-m", "--name-only"]
    if last:
        args += ["-n", str(last)]
    out = git(*args, ref, *CHANGE_PATHS)
    changes = []
    for record in out.split("\x1e")[1:]:
        header, _, rest = record.partition("\x1d")
        commit, date, subject, body = (header.split("\x1f") + ["", "", ""])[:4]
        files = [line for line in rest.splitlines() if line.strip()]
        changes.append((commit, date, subject, is_fix(subject, body), files))
    return changes


def tracked_files():
    return [p for p in git("ls-files", "-z").split("\0") if p]


def count_lines(path):
    """Lines of a text file, or None when it's binary, too big or not a file."""
    try:
        if os.path.islink(path) or not os.path.isfile(path) or os.path.getsize(path) > MAX_FILE_BYTES:
            return None
        with open(path, "rb") as f:
            data = f.read()
    except OSError:
        return None
    if b"\0" in data[:8192]:
        return None
    return data.count(b"\n") + (1 if data and not data.endswith(b"\n") else 0)


def table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


def n(number):
    return f"{number:,}"


def main():
    global GIT
    parser = argparse.ArgumentParser(description="Change history numbers for /minidev:checkup. Reads git; changes nothing.")
    parser.add_argument("--since", help="commit of the last check-up: changes and fixes after it are counted apart")
    parser.add_argument("--last", type=int, default=200, help="how many of the latest changes to read (default 200)")
    parser.add_argument("--top", type=int, default=10, help="rows per table (default 10)")
    parser.add_argument("--ref", default="HEAD", help="branch to read (default HEAD)")
    parser.add_argument("--git", default="git", help="git executable (default git)")
    args = parser.parse_args()
    GIT = args.git

    try:
        git("rev-parse", "--verify", "--quiet", args.ref + "^{commit}")
    except (RuntimeError, OSError) as error:
        print(f"No history to read: {args.ref} isn't a commit here, or git isn't available ({error}).")
        return 1

    changes = read_changes(args.ref, last=args.last)
    total = int(git("rev-list", "--count", "--first-parent", args.ref, *CHANGE_PATHS).strip())
    fixes = sum(1 for c in changes if c[3])

    # Size
    lines = {}
    for path in tracked_files():
        if is_code(path):
            count = count_lines(path)
            if count is not None:
                lines[path] = count
    code = {p: c for p, c in lines.items() if not is_test(p)}
    tests = {p: c for p, c in lines.items() if is_test(p)}

    print(f"# Change history ({args.ref})")
    print()
    if changes:
        print(f"Read: the latest {n(len(changes))} of {n(total)} changes ({changes[-1][1]} to {changes[0][1]}), "
              f"{n(fixes)} of them fixes.")
    if args.since:
        try:
            git("merge-base", "--is-ancestor", args.since, args.ref)
            since = read_changes(f"{args.since}..{args.ref}", names=False)
            print(f"Since {args.since[:12]}: {n(len(since))} changes, {n(sum(1 for c in since if c[3]))} of them fixes.")
        except RuntimeError:
            print(f"Since {args.since[:12]}: that commit isn't in this branch's history, so nothing is counted apart.")
    if len(changes) < FEW_CHANGES:
        print(f"With fewer than {FEW_CHANGES} changes, the tables below say little: read them as a first look.")
    print()

    print("## Size")
    print()
    print(f"Code: {n(len(code))} file(s), {n(sum(code.values()))} lines. "
          f"Tests: {n(len(tests))} file(s), {n(sum(tests.values()))} lines.")
    print()

    # Per-file counts, only for code files that still exist
    file_changes = collections.Counter()
    file_fixes = collections.Counter()
    folder_changes = collections.Counter()
    folder_fixes = collections.Counter()
    together = collections.Counter()
    for _commit, _date, _subject, fix, files in changes:
        touched = sorted({f for f in files if f in lines})
        for f in touched:
            file_changes[f] += 1
            file_fixes[f] += fix
        for d in {folder(f) for f in touched if f in code}:
            folder_changes[d] += 1
            folder_fixes[d] += fix
        sources = [f for f in touched if f in code]
        if 2 <= len(sources) <= MAX_FILES_FOR_PAIRS:
            for a, b in itertools.combinations(sources, 2):
                if os.path.dirname(a) != os.path.dirname(b):
                    together[(a, b)] += 1

    print("## Files that change most")
    print()
    hot = sorted((f for f in file_changes if f in code), key=lambda f: (-file_changes[f], -file_fixes[f], f))[:args.top]
    if hot:
        print(table(["File", "Changes", "Fixes", "Lines"], [(f, file_changes[f], file_fixes[f], n(code[f])) for f in hot]))
    else:
        print("(no code file changed in the changes read)")
    print()

    print("## Where fixes concentrate")
    print()
    fix_folders = sorted((d for d in folder_fixes if folder_fixes[d] >= 2), key=lambda d: (-folder_fixes[d], d))[:args.top]
    if fix_folders:
        print(table(["Folder", "Fixes", "Changes"], [(d, folder_fixes[d], folder_changes[d]) for d in fix_folders]))
    else:
        print("(no folder with two or more fixes)")
    print()

    print("## Files in different folders that change together")
    print()
    pairs = []
    for (a, b), count in together.items():
        share = count / min(file_changes[a], file_changes[b])
        if count >= MIN_TOGETHER and share >= MIN_SHARE:
            pairs.append((count, a, b))
    pairs.sort(key=lambda p: (-p[0], p[1], p[2]))
    if pairs:
        print(table(["File", "File", "Together", "Changes of each"],
                    [(a, b, count, f"{file_changes[a]} and {file_changes[b]}") for count, a, b in pairs[:args.top]]))
    else:
        print(f"(no pair changed together {MIN_TOGETHER} times or more, in at least half the changes of one of them)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
