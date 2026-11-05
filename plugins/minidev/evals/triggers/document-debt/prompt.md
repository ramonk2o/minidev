---
description: fires document
tags: [trigger]
max_turns: 6
allowed_tools: [Skill]
append_system_prompt: "The project's CLAUDE.md says:\n\n# Notes\n\nA small notes web app.\n- How it works today: `SPEC.md`. Ideas, the features in progress and bugs or debt left for later: `BACKLOG.md`. What changed in each version: `CHANGELOG.md`.\n\n## Development cycle\nThis project uses the `minidev` cycle. When a step needs one of its skills and it isn't available, tell the user and stop; don't imitate it from memory.\n- Ideas: `document`. Features: `build`. Bugs: `fix`. Refactoring, upgrades and other changes that keep the behavior: `chore`.\n- Integration: local merge.\n- Documents: English.\n- Releases: cut the version with `document`."
---

Anota no backlog que a gente deve uma refatoração do módulo de sync. Faço depois, agora não.
