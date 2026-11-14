# Backlog

Ideas, bugs and debt for this plugin, managed with sensei's `log` skill. Each entry starts from a real case. Done work leaves this file: what changed goes to CHANGELOG.md.

## swarm

### Workers make their own worktree when the environment can't
- **Type:** Idea
- **Motivation:** The `swarm-flow` behavior eval (2026-11-14, 0.75): the orchestrator picked both ideas, left the overlapping bug out, set both In progress in one commit and started two subagents with `isolation: worktree`; the eval harness refused ("worktree isolation is unavailable in this session"), so the swarm stopped as its step 1 says and put both entries back to Idea. No worker ran, so `two-squashes` failed and the merge path is still untested. The skill also learns that workers can't start only after its In progress commit.
- **Description:** Without `isolation: worktree`, a subagent worker creates its own worktree (`git worktree add <folder> -b <branch>`) and works there, so the swarm runs wherever a subagent and git exist, and `swarm-flow` tests the whole flow through both squashes.
- **Open questions:**
  - Where the workers' worktrees go, and who removes them at the end.
  - Whether step 1 should test that a worker can start before the In progress commit.
