# Choose for me

For someone who doesn't know git or GitHub and can't judge step 3's questions. It replaces the rest of step 3's round; steps 1, 2 and 4 to 9 run as they are, and step 8 still shows everything for one OK. The user triggers it by saying "choose for me" (in any language) or by giving it as the command's argument, or you offer it when their answers show the terms mean nothing to them.

## What it means

Take every recommendation step 3 would make (integration mode, where the backlog lives, the GitHub repository if there's no remote). Don't ask those questions. Say each choice in one plain sentence with what it changes day to day, e.g. "Pull requests: each change waits on GitHub for you to look at it before it joins the project." Avoid the words "integration mode", "squash" and "main branch" unless explaining them.

## What is skipped

- "What rule would someone new to this project break without knowing it?": leave Conventions out, and say they can ask Claude to add rules later.

## What is still asked

- **Uncommitted changes and the session's branch,** when step 2 found either: the questions in `references/commit.md` (Before writing), in plain words ("There is unsaved work in this folder. Save it as its own commit, or set it aside, before I continue"), with its recommendation. They protect the user's work, so choose-for-me doesn't skip them.

## When `gh` is missing or signed out

Say what is lost and how to get it, in plain words: "GitHub isn't connected on this computer, so changes will join the project directly, with no review step and no list of ideas on GitHub. To get those, install `gh` if needed, sign in with `gh auth login` and run `/minidev:setup` again." Then continue with local merge and BACKLOG.md, unless the user says they want to sign in now: then stop and let them run setup again once they have.

## The squash setting

Mention it only when step 3 recommends pull requests merged by the reviewer and step 2 found the setting isn't `PR_BODY`: one sentence ("a GitHub setting keeps a record of the checks in each saved change; it's off") and where to turn it on (Settings → General → Pull Requests → "Title and description"). Setup doesn't change it.

## At the end (step 9.4)

After the usual closing line, list what was chosen for them, one line each with what it changes (integration, backlog, GitHub repository, no Conventions), and end with: "To change any of these, run `/minidev:setup` again and say which."
