---
name: setup
description: Set up a software project for the minidev development cycle (interview, document, build, fix and chore skills, tester and reviewer agents) by making it a git repository if needed, writing or updating its CLAUDE.md, allowing its test and build commands in the project's permissions, creating the product documents, and pointing out what adopting the cycle left orphaned or redundant. Run only when the user invokes it.
disable-model-invocation: true
---

# Setup

Prepares a project so it works with the development cycle of the `minidev` plugin: the `interview`, `document`, `build`, `fix` and `chore` skills and the `tester` and `reviewer` agents, which come with this plugin. The cycle's steps live in those skills; the CLAUDE.md only holds the project's facts and says which skill handles each step, so updating the plugin updates every project. The cycle is the same in every project; what changes is the project's own facts (commands, conventions, how tests are written), so the CLAUDE.md has a fixed part, copied from the template below, and a discovered part, found in the repository or asked.

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
- **Integration:** where the repository lives (`git remote -v`): on GitHub, on another host, or with no remote; and whether `gh` is installed and signed in (`gh auth status`). On GitHub, read the main branch's protection (`gh api repos/<owner>/<repo>/rules/branches/<main>` lists a rule, or `gh api repos/<owner>/<repo>/branches/<main>/protection` answers; that one needs admin rights, so a 403 means unknown, not unprotected): if it requires an approving review (`required_approving_review_count` of 1 or more in the rule or the protection), that's a sign for pull requests merged by the reviewer. Then also read the repository's squash setting (`gh api repos/<owner>/<repo> --jq .squash_merge_commit_message`), for step 3; empty means unknown (it needs admin rights). If pull requests target a branch other than the remote's default (e.g. `develop`, per CONTRIBUTING or recent pull requests), note it for a `Main branch:` line.
- **Backlog:** whether the repository has GitHub issues turned on (`gh repo view --json hasIssuesEnabled`). With pull requests, they show the backlog as it changes, instead of a BACKLOG.md that only changes with each merge.
- **Where the session stands:** the current branch, uncommitted changes and worktrees, as `references/commit.md` says (Before writing).
- **Commit rules:** hooks that check commits (`.husky/`, `.pre-commit-config.yaml`, `lefthook.yml`, `.git/hooks/` that aren't samples) and a commit message convention (`commitlint.config.*`, conventional commits in `git log`). The cycle's own messages adapt to a convention (the `build` skill's `references/git-flow.md`, Checkpoints): note it for the Development cycle section.
- **Release:** whether the project publishes versions (a store, a registry, deploys) and where the steps are written (e.g. a `STORE.md`, `RELEASING.md`, a CI workflow).
- **Product documents:** which of `SPEC.md`, `BACKLOG.md`, `CHANGELOG.md` exist, and the language of the project's existing docs. Whether a tool generates the changelog (`release-please-config.json`, `.changeset/`, `.releaserc`, `cliff.toml`).

## 3. Ask

In one short round with a suggested answer for each, ask only what you couldn't find. Always include:

- **The integration mode**, recommending:
  - pull requests merged by the reviewer when the main branch requires an approving review;
  - pull requests when the repository is on GitHub and `gh` is signed in;
  - with no remote and `gh` signed in, creating a GitHub repository for the project (read `references/remote.md`), which brings pull requests; if the user declines, local merge;
  - local merge otherwise (a remote on another host, or `gh` missing or signed out), saying what's missing and that running setup again once it's there switches the project.
- **Where the backlog lives**, when you recommend either pull request mode and issues are on (a repository setup creates has them on), recommending GitHub issues: the backlog shows what's being built without waiting for a merge. Otherwise it's BACKLOG.md, without asking; if the user picks a pull request mode you didn't recommend, ask it then, as a short follow-up.
- **Uncommitted changes and the session's branch**, when step 2 found either: the questions in `references/commit.md` (Before writing).
- "What rule would someone new to this project break without knowing it?" Its answers become Conventions. If there are none, the Conventions section is left out.

When recommending pull requests merged by the reviewer, say with it what step 2 found of the squash setting: if it's `COMMIT_MESSAGES` or `BLANK`, the main branch's commits won't carry the verification record as written; if it's unknown, that it couldn't be read. Either way, it should be "Title and description" (`PR_BODY`), set in GitHub's Settings → General → Pull Requests.

## 4. Write the draft

Build the file from the template below. Fill every `<…>`; the final file has no placeholders. Leave out a line or section the project has nothing for, as the template notes say.

### Template

````markdown
# <Project name>

<What the project is, in one sentence.>
- How it works today: `SPEC.md`. Ideas, the features in progress and bugs or debt left for later: <`BACKLOG.md` | the repository's GitHub issues>. What changed in each version: `CHANGELOG.md`.

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
- Integration: <local merge | pull requests | pull requests, merged by the reviewer>.
- Backlog: GitHub issues. <only when the backlog lives in the repository's issues>
- Documents: <language of BACKLOG.md, SPEC.md and CHANGELOG.md>.
- Releases: <where the release steps live>.
- Main branch: <name, only when it isn't the remote's default branch>.
- Commit messages: <the convention a hook enforces, e.g. conventional commits; only when there is one>.
- Changelog: generated by <tool>; don't edit it by hand. <only when a tool generates it>
````

Template notes:
- The **Development cycle** section is copied as is. Only the Integration, Documents and Releases lines change, the Backlog line is added only when the backlog lives in GitHub issues, and the last three lines are added only when step 2 found them.
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
- the git commands the cycle uses locally: `git status`, `git diff`, `git log`, `git show`, `git blame`, `git rev-parse`, `git merge-base`, `git symbolic-ref`, `git write-tree`, `git branch --list`, `git branch -r`, `git worktree list`, `git remote`, `git ls-remote`, `git add`, `git commit`, `git switch`, `git merge`, `git fetch`, `git pull --ff-only`, `git pull --rebase`, `git rebase --abort`, `git read-tree`, `git restore`, `git branch -m`, `git remote set-head`, `git tag`;
- in either pull request mode, the read-only `gh` commands: `gh pr view`, `gh pr list`, `gh pr checks`, `gh auth status`;
- with the backlog in GitHub issues, the read-only `gh issue view`, `gh issue list`, `gh label list`, `gh repo view`.

Never add install, publish, deploy, `git push`, `git reset`, `gh repo create`, `gh pr create`, `gh pr merge` or `gh issue` commands that write (create, edit, close, reopen, comment), or anything that deletes files or branches: those keep asking. If the file exists, merge: keep every existing entry and setting, add only what's missing. Show the resulting list. Add no `git -C` rule: when the main branch is checked out in another worktree (often in a worktree the app made for the session), `git-flow.md` runs its steps there with `git -C <path>`, and no rule allows those without letting a push or reset through, so they keep asking; say so with the list.

## 7. Orphans and redundancies

Check only what adopting the cycle leaves behind. This is not a general cleanup: anything unrelated to the cycle stays as it is, even if it looks unnecessary.

- **Old documents** that now overlap BACKLOG, SPEC or CHANGELOG (`TODO.md`, `FEATURES.md`, `ROADMAP.md`, `HISTORY.md`…). Don't convert them: point them out; aligning them is the `document` skill's job (step 9).
- **Sections of the old CLAUDE.md** that the new text replaces: an older workflow, backlog or test rules that the skills now own, the longer Development cycle section written by earlier versions of this skill (idea, build, bug and release steps spelled out), or a line saying the cycle is installed globally in `~/.claude/`.
- **Local skills, agents and commands** (`.claude/skills/`, `.claude/agents/`, `.claude/commands/`) that overlap the cycle: a local build, backlog or tester, or an old copy of one of this plugin's skills. If one has something project-specific the plugin's doesn't cover, propose moving that part into the CLAUDE.md before removing it. Other local skills are just listed.
- **Global copies of the cycle** in `~/.claude/skills/` (`grilling`, `interview`, `document`, `build`, `fix`, `chore`, `brainstorm`, `bootstrap`) or `~/.claude/agents/` (`tester.md`, `reviewer.md`): they duplicate this plugin and may be older versions. Point them out and suggest removing them; they're outside the project, so this always needs its own explicit OK.
- **Broken references:** the CLAUDE.md (old or new) pointing to a file, script or command that doesn't exist.

For each item, say what it is, why it's orphaned or redundant, and what you suggest (remove, move a part to the CLAUDE.md, leave).

## 8. Review

Show everything in one message: git setup and, if there were no tests, the test setup (step 1), the GitHub repository to create, if the user accepted one (`references/remote.md`, Show), the CLAUDE.md draft or its changes (steps 4–5), the permissions (step 6), the orphans (step 7) and, when the backlog moves to issues and BACKLOG.md exists, the list of issues to create, said to be visible to everyone who can see the repository as soon as they're created (`document`, `references/issues.md`, Migrate from BACKLOG.md). Wait for the OK; the user may approve parts. If they decline the list of issues, the backlog stays in BACKLOG.md: redo the CLAUDE.md's backlog lines and the permissions for it, keeping the integration mode, and show them again.

## 9. Finish

1. In a repository with commits, before writing anything, settle where setup's commit goes, as `references/commit.md` says (Where it goes). Then apply what was approved, in this order: `git init` and `.gitignore`; the GitHub repository, if one was approved (`references/remote.md`, Create); the test setup, run and shown passing (if it fails, fix it or stop before the CLAUDE.md); the CLAUDE.md (when the backlog moves to issues and BACKLOG.md exists, with `BACKLOG.md` in its first line and no Backlog line until step 2's migration is done); `.claude/settings.json`; the removals.
2. If any of `SPEC.md`, `BACKLOG.md` (unless the backlog lives in issues), `CHANGELOG.md` is missing, an old document was pointed out in step 7, or the backlog moves to issues and BACKLOG.md exists, load the `document` skill and create or align them with it. When the backlog moves to issues and BACKLOG.md exists, `document` migrates it first (`references/issues.md`, Migrate from BACKLOG.md), from the list approved in step 8, and creates the other documents after. That way a new SPEC.md's `Missing tests` Debt entries go where the backlog lives by then: as issues (`references/issues.md`, Operations), or to BACKLOG.md if the migration failed. Until every issue exists, the CLAUDE.md's first line keeps `BACKLOG.md` and has no Backlog line; write them for issues once the migration is done, so a failed migration doesn't leave the backlog in two places. Don't write the documents yourself: their formats belong to that skill. For existing code, `document` checks each rule of a new SPEC.md against the code as it writes it, so untested rules become `Missing tests` Debt entries before the first feature. If SPEC.md already exists with Behavior rules, it was written before the cycle and may have drifted: offer the spec audit (a SPEC.md fresh from `brainstorm` has no Behavior yet, so there's nothing to audit) (`document`, `references/spec-audit.md`), now or later. A large product is audited one area at a time.
3. Offer a commit with the changes, and don't commit without the OK. Its message is one line (e.g. `chore: set up the minidev cycle`); when the backlog moved to issues, its body lists them (`Backlog moved to GitHub issues: #40, #41`, never `Closes`), so the record stays on the main branch. Bring it in as `references/commit.md` says (Bring it in).
