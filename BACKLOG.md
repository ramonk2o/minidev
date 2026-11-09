# Backlog

Ideas, bugs and debt for this plugin, managed with sensei's `log` skill. Each entry starts from a real case. Done work leaves this file: what changed goes to CHANGELOG.md.

## build

### Resume with a pull request waiting and another branch in progress
- **Type:** Idea
- **Motivation:** At Mediacraft (a non-technical team prototyping in Claude Code), the author never merges their own pull request, so with "Integration: pull requests, merged by the reviewer" the author keeps building one feature while another's pull request waits for the reviewer. Two open work branches become the normal state, and a bare "continua" makes Resume show the branches and ask which, every time; a cold-reader test of `references/git-flow.md` found that "continua" could equally mean reporting the waiting pull request or carrying on the other feature.
- **Description:** When "continue" matches several branches, read the pull requests' states first and answer half the question in the same message (e.g. "Filtros: approved, waiting for the reviewer's merge. Shall I go on with Busca?").

### "Update" after the reviewer merges doesn't reliably trigger build
- **Type:** Bug
- **Motivation:** In pull requests merged by the reviewer, the author's natural request after the merge is "atualiza aí" or "o PR foi mergeado, atualiza". A cold reader flagged that build's description matches "continue X where we left off", not these, so the request may be answered with a plain `git pull` that skips the cleanup and the squash check in `references/git-flow.md` (Merged by the reviewer, step 6). A trigger run on 0.25.3 (2026-11-09, 3 runs each, project set to "pull requests, merged by the reviewer") confirmed it: "The Tables PR got merged, update things on your side." fired build 3/3, "O PR da Tabelas foi mergeado, atualiza aí." 2/3, "O revisor aprovou e mergeou o PR. Atualiza." 0/3 and "Reviewer merged it. Sync up." 0/3. The near-misses "Puxa a main do remote pra mim." and "git pull on main, please." correctly fired nothing.
- **Description:** Build's description covers a merged pull request being reported or an update asked after it, so these requests fire build, while a plain pull of main still doesn't. The six phrasings above become trigger cases.

### Document commits that ride in another branch go unrecorded
- **Type:** Bug
- **Motivation:** A cold reader of `references/git-flow.md` found that an idea recorded on the main branch before another work branch started (e.g. while a pull request waited for the reviewer) is carried by that branch's squash, but the final message only lists document changes made on the branch. Reverting that branch would drop the idea without a trace (When a merged change breaks relies on the final message). It already happened in pull request mode; reviewer merges make the wait, and the case, more common.
- **Description:** The final message also lists document changes the branch carries from the main branch that aren't part of the work, so a revert reapplies them.
