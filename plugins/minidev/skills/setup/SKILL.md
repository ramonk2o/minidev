---
name: setup
description: Set up a software project for the minidev development cycle (grilling, document, build, fix and chore skills, tester and reviewer agents) by making it a git repository if needed, writing or updating its CLAUDE.md, allowing its test and build commands in the project's permissions, creating the product documents, and pointing out what adopting the cycle left orphaned or redundant. Run only when the user invokes it.
disable-model-invocation: true
---

# Setup

Prepares a project so it works with the development cycle of the `minidev` plugin: the `grilling`, `document`, `build`, `fix` and `chore` skills and the `tester` and `reviewer` agents, which come with this plugin. The cycle's steps live in those skills; the CLAUDE.md only holds the project's facts and says which skill handles each step, so updating the plugin updates every project. The cycle is the same in every project; what changes is the project's own facts (commands, conventions, how tests are written), so the CLAUDE.md has a fixed part, copied from the template below, and a discovered part, found in the repository or asked.

Talk to the user in the language of the conversation. Write the CLAUDE.md in English.

Personal working rules (reply language, how the user likes code, when to use the browser…) are not this skill's business: don't add them, and leave any that an existing CLAUDE.md already has untouched.

Nothing is written before the user's OK. Collect the proposals of steps 1 and 4–7 and show them together in step 8, so the user approves once.

## 1. Check the project

If the folder isn't a software project, say that this skill is for software projects and stop. If it's empty or holds only notes for a project that doesn't exist yet, point to the `brainstorm` skill, which plans and scaffolds a new project, and stop.

**Git.** The cycle commits after each feature, bug fix, chore and document change, and builds features, fixes and chores on their own branches, so the project must be a git repository. If it isn't one, propose `git init` and, when there's no `.gitignore`, a short one for the project's stack (dependencies, build output, test reports, `.env`, OS files like `.DS_Store`, and `.claude/settings.local.json`). If it's a repository with no commits yet, note that the first commit will come at the end (step 9).

**Tests.** The cycle needs automated tests: `build` writes them first and `tester` runs them. Find the test framework and command (package.json scripts, Makefile, pyproject, Cargo.toml, go.mod, CI config…). If there's none, propose a minimal one in the same approval as the rest: the standard test framework for the stack (checked against its current docs), its config, a test command and one smoke test that passes. Set it up and show the test passing before writing the CLAUDE.md. If the user declines, stop: don't generate a cycle that can't run. Tests for the existing code come later, as chores ("add tests to <module>"), before the features that change it.

## 2. Discover

Read the repository to fill the project-specific sections. Look, don't guess:

- **Project line:** what the project is, in one sentence (README, package description, manifest).
- **Commands:** install, develop/watch, build, tests, lint, type-check, run or load the app, package/release. A project with no build step leaves Build out, and the skills then run only the tests. In a monorepo, list the commands per package, and say which run for a change in each. Take them from the real scripts; note side effects worth knowing (e.g. install also enables a hook, build also type-checks).
- **Tests:** where test files live and how they're named, shared fakes, mocks or helpers, and how rules that change data or state are tested (find one existing test that does it well, to cite as the example). Also what only shows in the real app (visuals, focus, browser or device behavior): that's what goes to "To check by hand".
- **Conventions:** only rules with clear evidence in the code: a module that centralizes access to something, strict compiler settings, a test that checks consistency between files, a lint rule. Don't invent conventions and don't list what any developer would do anyway.
- **Integration:** whether branches should reach the main branch by local merge or by pull request. Signs for pull requests: a GitHub remote plus CI workflows (`.github/workflows/`), a protected main branch (`gh api repos/<owner>/<repo>/rules/branches/<main>` lists a rule, or `gh api repos/<owner>/<repo>/branches/<main>/protection` answers; that one needs admin rights, so a 403 means unknown, not unprotected), or commits from more than one author (`git shortlog -sn`). Pull requests need `gh` signed in (`gh auth status`); if it isn't, say so. If pull requests target a branch other than the remote's default (e.g. `develop`, per CONTRIBUTING or recent pull requests), note it for a `Main branch:` line.
- **Commit rules:** hooks that check commits (`.husky/`, `.pre-commit-config.yaml`, `lefthook.yml`, `.git/hooks/` that aren't samples) and a commit message convention (`commitlint.config.*`, conventional commits in `git log`). The cycle's own messages adapt to a convention (the `build` skill's `references/git-flow.md`, Checkpoints): note it for the Development cycle section.
- **Release:** whether the project publishes versions (a store, a registry, deploys) and where the steps are written (e.g. a `STORE.md`, `RELEASING.md`, a CI workflow).
- **Product documents:** which of `SPEC.md`, `BACKLOG.md`, `CHANGELOG.md` exist, and the language of the project's existing docs. Whether a tool generates the changelog (`release-please-config.json`, `.changeset/`, `.releaserc`, `cliff.toml`).

## 3. Ask

In one short round with a suggested answer for each, ask only what you couldn't find. Always include the integration mode, recommending pull requests when step 2 found signs for them and local merge otherwise, and one question: "What rule would someone new to this project break without knowing it?" Its answers become Conventions. If there are none, the Conventions section is left out.

## 4. Write the draft

Build the file from the template below. Fill every `<…>`; the final file has no placeholders. Leave out a line or section the project has nothing for, as the template notes say.

### Template

````markdown
# <Project name>

<What the project is, in one sentence.>
- How it works today: `SPEC.md`. Ideas, the feature in progress and bugs or debt left for later: `BACKLOG.md`. What changed in each version: `CHANGELOG.md`.

## Commands
- Install: `<command>` <(side effects worth knowing)>
- Develop: `<command>`
- Build: `<command>` <(what it also checks, where the output goes)>
- Tests: `<command>` (<framework>)
- Lint: `<command>`
- Type-check: `<command>`
- <Run / Load / Package>: <how>

## Conventions
- <rule with evidence or given by the user>

## Tests
- Tests live <where, naming pattern>.
- <Shared fakes, mocks or helpers, and what they replace.>
- <Rules that change data or state> are tested <how>, as in `<example test file>`. Only what needs <the real app, named for this project: e.g. a real browser, a device> (<what: e.g. focus, dragging, visuals>) goes into "To check by hand".

## Development cycle
This project uses the `minidev` cycle. When a step needs one of its skills and it isn't available, tell the user and stop; don't imitate it from memory.
- Ideas: `document`. Features: `build`. Bugs: `fix`. Refactoring, upgrades and other changes that keep the behavior: `chore`.
- Integration: <local merge | pull requests>.
- Documents: <language of BACKLOG.md, SPEC.md and CHANGELOG.md>.
- Releases: <where the release steps live>.
- Main branch: <name, only when it isn't the remote's default branch>.
- Commit messages: <the convention a hook enforces, e.g. conventional commits; only when there is one>.
- Changelog: generated by <tool>; don't edit it by hand. <only when a tool generates it>
````

Template notes:
- The **Development cycle** section is copied as is. Only the Integration, Documents and Releases lines change, and the last three lines are added only when step 2 found them.
- **Release:** if the project doesn't publish versions, drop the Releases line. If it does but the steps aren't written anywhere, use "cut the version with `document`" and offer to write the steps down later.
- **Commands:** drop a line the project has no command for (e.g. Type-check when the build already type-checks: say so in the Build line).
- **Tests:** if no existing test shows how state-changing rules are tested, drop the "as in" part rather than citing a weak example.
- **Conventions:** drop the section when there's nothing to put in it.
- Keep the project's existing specifics that still hold (an extra section, a rule about permissions, a doc pointer): they belong to the project, not to this template.

## 5. Existing CLAUDE.md

If the project already has a `CLAUDE.md` (or `AGENTS.md`, `.claude/CLAUDE.md`), don't overwrite it. Show what changes, section by section: what's added, what the new text replaces, what stays. Keep everything project-specific that's still true.

## 6. Permissions

The cycle runs the same commands many times (tests before and after the code, the build, the tester's rounds, commits), and a permission prompt on each one breaks the flow. Propose `.claude/settings.json` entries under `permissions.allow` for:

- the test, build, lint and type-check commands from step 2, each as a prefix rule so its arguments are covered (e.g. `Bash(npm test:*)`, `Bash(npm run build:*)`, `Bash(npx vitest:*)`);
- the git commands the cycle uses locally: `git status`, `git diff`, `git log`, `git show`, `git blame`, `git rev-parse`, `git merge-base`, `git symbolic-ref`, `git write-tree`, `git branch --list`, `git branch -r`, `git worktree list`, `git remote`, `git ls-remote`, `git add`, `git commit`, `git switch`, `git merge`, `git fetch`, `git pull --ff-only`, `git pull --rebase`;
- in pull request mode, the read-only `gh` commands: `gh pr view`, `gh pr list`, `gh pr checks`, `gh auth status`.

Never add install, publish, deploy, `git push`, `git reset`, `gh pr create` or `gh pr merge` commands, or anything that deletes files or branches: those keep asking. If the file exists, merge: keep every existing entry and setting, add only what's missing. Show the resulting list.

## 7. Orphans and redundancies

Check only what adopting the cycle leaves behind. This is not a general cleanup: anything unrelated to the cycle stays as it is, even if it looks unnecessary.

- **Old documents** that now overlap BACKLOG, SPEC or CHANGELOG (`TODO.md`, `FEATURES.md`, `ROADMAP.md`, `HISTORY.md`…). Don't convert them: point them out; aligning them is the `document` skill's job (step 9).
- **Sections of the old CLAUDE.md** that the new text replaces: an older workflow, backlog or test rules that the skills now own, the longer Development cycle section written by earlier versions of this skill (idea, build, bug and release steps spelled out), or a line saying the cycle is installed globally in `~/.claude/`.
- **Local skills, agents and commands** (`.claude/skills/`, `.claude/agents/`, `.claude/commands/`) that overlap the cycle: a local build, backlog or tester, or an old copy of one of this plugin's skills. If one has something project-specific the plugin's doesn't cover, propose moving that part into the CLAUDE.md before removing it. Other local skills are just listed.
- **Global copies of the cycle** in `~/.claude/skills/` (`grilling`, `document`, `build`, `fix`, `chore`, `brainstorm`, `bootstrap`) or `~/.claude/agents/` (`tester.md`, `reviewer.md`): they duplicate this plugin and may be older versions. Point them out and suggest removing them; they're outside the project, so this always needs its own explicit OK.
- **Broken references:** the CLAUDE.md (old or new) pointing to a file, script or command that doesn't exist.

For each item, say what it is, why it's orphaned or redundant, and what you suggest (remove, move a part to the CLAUDE.md, leave).

## 8. Review

Show everything in one message: git setup and, if there were no tests, the test setup (step 1), the CLAUDE.md draft or its changes (steps 4–5), the permissions (step 6) and the orphans (step 7). Wait for the OK; the user may approve parts.

## 9. Finish

1. Apply what was approved, in this order: `git init` and `.gitignore`; the test setup, run and shown passing (if it fails, fix it or stop before the CLAUDE.md); the CLAUDE.md; `.claude/settings.json`; the removals.
2. If any of `SPEC.md`, `BACKLOG.md`, `CHANGELOG.md` is missing, or an old document was pointed out in step 7, load the `document` skill and create or align them with it. Don't write them yourself: their formats belong to that skill.
3. Offer a commit with the changes (the first commit, in a new repository). Don't commit without the OK.
