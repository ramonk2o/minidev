# CHANGELOG.md

`CHANGELOG.md`, at the project root, records what changed in each version, for the people who use the product. It follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

## Entries

- **One or two sentences per change, from the user's point of view:** what they can now do, what works differently, what was fixed. Start with the feature's name in bold when it's a feature.
- **No detailed rules.** Edge cases, formats and conditions live in SPEC.md; the entry says what changed, not every rule of it. Copies drift.
- **Categories**, in this order, only those with entries: Added, Changed, Deprecated, Removed, Fixed, Security.
- New entries go under `## [Unreleased]`.
- Changes that don't affect the product (project docs, tooling) are recorded only if notable, and say so, e.g. "(project docs only, the product doesn't change)".
- Follow the existing file's wording style where it has one.
- If a tool generates the changelog (release-please, changesets, semantic-release, git-cliff; the project's CLAUDE.md says so), don't edit the file by hand: record the change the way that tool reads it (a changeset file, a conventional commit message) and leave releases to it.

Example:

```markdown
### Added
- **Power and remainder in calculations**: `2^10=` (or `2**10=`) and `7%3=` now work, following the usual math rules.

### Fixed
- Plain-text copies keep line breaks made with Shift+Enter.
```

## Creating it

When the project has no `CHANGELOG.md`, create it:

```markdown
# Changelog

All notable changes to this project are documented here. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/).

## [Unreleased]
```

If the project already has released versions (git tags, a version in its manifest or package file), ask whether to reconstruct past versions from the git history or start from now.

## Releases

A release is made on the main branch, brought up to date (`../../build/references/git-flow.md`, The main branch): from a work branch, commit its work as a checkpoint and switch first, so the version holds only what reached the main branch.

When the user releases a version:
1. **Pick the number** with Semantic Versioning: major for breaking changes, minor for new features, patch for fixes only. Propose it from the `[Unreleased]` entries; the user decides.
2. **Show** the version, the date and the entries that go into it, and wait for the OK. If backlog entries are still planned for this version (their Version, or the open issues in its milestone), list them in the same message and ask where each goes: the next version, or none.
3. **Move** the `[Unreleased]` entries under `## [<version>] - <YYYY-MM-DD>`, leaving `## [Unreleased]` empty above it. A short line under the heading can say where it went (e.g. "Submitted to the store as an update").
4. **Update the links** at the end of the file:
   ```markdown
   [Unreleased]: <repo>/compare/<version>...HEAD
   [<version>]: <repo>/compare/<previous>...<version>
   ```
   The first version links to `<repo>/tree/<version>`. `<repo>` is the remote's web address; with no remote, or a host without compare pages, leave the links out.
5. **Tag** the release commit with an annotated tag named like the existing tags (e.g. `1.4.0`), locally.
6. Push the commit and the tag, if the repository has a remote.
7. With the backlog in GitHub issues, close the version's milestone if it has one: its number from `gh api repos/{owner}/{repo}/milestones`, then `gh api -X PATCH repos/{owner}/{repo}/milestones/<number> -f state=closed`.

In pull request mode (the project's CLAUDE.md says so), the main branch can't take a direct push, so steps 5 and 6 change: make the release commit on a `release/<version>` branch instead and bring it in as in the `build` skill's `references/git-flow.md` (`../../build/references/git-flow.md` from this file), with "Release <version>" as the message. Then tag the squashed commit on the updated main branch and push only the tag (`git push <remote> <version>`, the remote as in that file's The main branch). When pull requests are merged by the reviewer, tag it once the reviewer has merged, when the user asks to continue (that file's Merge and push, Merged by the reviewer).

Other release steps (bumping the version in package or manifest files, building a package, submitting to a store) belong to the project: follow its instructions.
