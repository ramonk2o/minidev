---
tags: [behavior]
runs: 1
max_turns: 200
timeout_seconds: 2400
append_system_prompt: "This is an unattended evaluation run: the user is away and has approved in advance every list, draft and plan you would show them for an OK (a start message with its critical test list, open points and size, a backlog draft), accepts every tester assumption you adopted, and confirms that anything to check by hand works. When a step says to wait for the user, say what you would ask and go on. The repository has no remote, so nothing is pushed. This sandbox blocks the system git: run git as `./.tools/git` (from the project folder) wherever a step says `git`."
---

Build the Note titles feature from the backlog. I want the tester to check this one too.
