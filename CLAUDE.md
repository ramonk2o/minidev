# minidev

A Claude Code plugin with a fixed development cycle (plan, interview, build test-first, fix, chore, document) for developers who want the same process in every project.

## Maintenance with sensei

This repository is maintained with the sensei plugin. If sensei is installed:
- creating or changing a skill, judging an issue or pull request, or auditing consistency: the `train` skill;
- BACKLOG.md and CHANGELOG.md: the `log` skill (`train` writes its own changelog entries);
- releasing a version: `/sensei:graduate`.

Other skills or plugins that write skills or manage these files don't apply in this repository. Without sensei, follow `docs/principles.md` and keep CHANGELOG.md in the Keep a Changelog format.

**The skills are the object of the work here, not tools.** When the conversation is about the plugin's subject (a development cycle: planning, building features test-first, fixing bugs, chores, BACKLOG/SPEC/CHANGELOG), it's about improving the skills. Don't run a skill's flow unless explicitly asked to use it.

## Project facts

- **Documents:** English.
- **Principles:** `docs/principles.md`. Every change is checked against them.
- **Skills stand alone:** no. A reference shared by several skills lives in one skill's folder and the others point to it by path; the plugin ships whole, with no per-skill zips.
- **Layout:** the marketplace is at the root (`.claude-plugin/marketplace.json`); the plugin is in `plugins/minidev/`. The version lives in `plugins/minidev/.claude-plugin/plugin.json`, and its `description` must match the one in `marketplace.json`.
- **Validate:** sensei's check script on every change (it runs `claude plugin validate` on the last commit); `--release` at release, which adds `--profile directory`.
- **Evals:** run from `plugins/minidev` (commands in the README's "Developing the plugin"). Trigger evals cost about $0.10 a run, behavior evals a few dollars, the outcome run about $10: ask before running behavior or outcome evals.
- **Commits:** author `Ramon K. <contato@ramonk.com>`; trailers: the environment's default (`Co-Authored-By`).
- **Integration:** a local branch per change, merged into main with `--no-ff`; push main when the maintainer says so or at release.
- **Tags:** annotated `vX.Y.Z`; CHANGELOG.md keeps a compare link for every version.
- The README's "Developing the plugin" describes every eval case; a change that adds, removes or renames a case updates it.
