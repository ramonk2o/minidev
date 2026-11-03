# SPEC.md

`SPEC.md`, at the project root, describes how the product works **today**: its rules, its data and the technical decisions behind it. It's what someone (a person or an agent) reads to change the product without breaking what exists. It's not a plan (that's the backlog), a history (that's the changelog) or a manual of screens.

## What belongs in it

- **Rules, not visuals.** Write what the product does and under which conditions ("an empty note isn't saved"; "the title follows the first line until renamed"), not how it looks (colors, spacing, icons). Visual details change often and are better read from the product itself.
- **Behavior someone could break.** Edge cases that were decided belong here ("remainder by zero writes nothing"). Obvious behavior doesn't need a line.
- **Present tense, only what exists.** A planned rule stays in the feature's Decisions in the backlog until the feature is built.
- **No code or file paths in rules.** Name modules or files only in the technical decisions, where the structure is the point.

## Creating it, adapted to the project

There's a default outline, but a spec is only useful if it fits the product it describes. A browser extension, a command-line tool, a library and a web API are described by different things, so adapt the outline before writing.

### 1. Understand the project
Read what already says what the product is and does: README, existing docs, the code's entry points, the tests (they're often the best record of decided behavior), configuration and manifests. Work out:
- **What kind of product it is**, and who uses it (end users, developers calling an API, other programs).
- **Its surfaces:** where users meet it (screens, commands, functions, endpoints, files it reads or writes).
- **What it stores**, if anything, and where.
- **Constraints** that shape decisions: platform, permissions, dependencies, performance limits.

### 2. Adapt the outline
Default outline:

```markdown
# <Product>

<legend>

## Goal
<what the product is and who it's for, in two or three sentences>

## Behavior
### <Area>
- <rule>

## Data model
<what is stored, where, and its shape>

## Technical decisions
- <decision>: <why>

## Constraints
- <a limit the whole product respects, checkable>: <why>

## Known limitations
- <limitation>
```

Adapt it to the project:
- **Organize Behavior by how users meet the product**, so a reader finds a rule where they'd look for it:
  - an app or extension: by area of the interface or by workflow ("Notes and the sidebar", "Settings and backup")
  - a CLI: by command
  - a library: by public module or function (the **public API** is the behavior)
  - a web API: by resource or endpoint, with its contract (inputs, outputs, errors)
  - a service or pipeline: by stage or event
- **Rename or add sections the project needs.** For example: "Public API" for a library, "Configuration" when there are many options, "Permissions" or "Security" for an extension or a service with access concerns, "Integrations" when other systems are involved, "Compatibility" when versions matter.
- **Drop sections that don't apply.** A product that stores nothing has no Data model; don't keep empty headings.
- Keep Goal first and Known limitations last: the first orients the reader, the last warns them.

### 3. Propose before writing
Show the user the adapted outline: the sections, the Behavior areas, and a sentence on what each one will hold, with why the outline differs from the default where it does. Wait for the OK.

### 4. Write it from what exists
Fill it with the current behavior, taken from the code, tests and docs. Don't describe intended behavior as if it existed. When the code is ambiguous about a rule (behavior that looks accidental, or code and docs that disagree), don't decide it: list those points to the user at the end and ask which is the rule.

## Legend

Right after the title, translated to the file's language:

```markdown
How <product> works today, as rules (not visual details), plus its data and technical decisions. Managed with the `document` skill: it's updated when a feature is finished, describing what was built. Ideas live in BACKLOG.md; what changed and when lives in CHANGELOG.md.
```

## Updating it

- **When a feature is finished:** add or change the rules of what was actually built, including what changed along the way (answers to open questions, decisions made during the work). Use the feature's Decisions as a guide, especially when they name a SPEC rule that changes.
- **Put each rule in the area where a reader would look for it.** If no area fits, add one; if an area grew too big or no longer matches how the product is organized, propose a reorganization.
- **Remove rules that no longer hold.** A spec with stale rules is worse than a short one.
- **A feature's Constraints** go next to the rule they limit in Behavior, or under Constraints when they hold for the whole product (e.g. "every page works with the keyboard alone").
- **Record new technical decisions with their reason** (a new dependency, permission or storage choice), and new limitations users or developers should know about.
- Keep the existing wording style of the file: its tense, level of detail and how it writes rules.
