# commit-and-pr

An [Agent Skill](https://docs.claude.com/en/docs/claude-code/skills) that
automates writing git commit messages and opening GitHub pull requests.

Point it at a dirty working tree and it will:

1. Read `git status` / `git diff` to understand *why* the change was made
2. Draft a [Conventional Commits](https://www.conventionalcommits.org/) message
3. Commit (creating a feature branch first if you're on `main`/`master`)
4. Push
5. Open a PR via `gh pr create` with a Summary / Changes / Test Plan body

It asks before anything hard-to-reverse (force-push, amending a pushed
commit, merging, committing straight to the default branch) and refuses to
commit if it spots secrets in the diff.

Works with any agent that supports the Agent Skills format — built and
tested with **Claude Code**; also compatible with **Google Antigravity**.

## Install

**Claude Code** — clone anywhere, then copy the `commit-and-pr/` folder into
your skills directory:

```bash
git clone https://github.com/hsK10x2/commit-and-pr /tmp/commit-and-pr

# per-user (all projects)
cp -r /tmp/commit-and-pr/commit-and-pr ~/.claude/skills/commit-and-pr

# or per-project instead
cp -r /tmp/commit-and-pr/commit-and-pr <project>/.claude/skills/commit-and-pr
```

Then use it with `/commit-and-pr` or just ask naturally: "커밋해줘", "commit
this and open a PR".

**Google Antigravity** — copy `commit-and-pr/SKILL.md` into
`~/.gemini/config/skills/commit-and-pr/SKILL.md` (global) or
`<project>/.agents/skills/commit-and-pr/SKILL.md` (per-project). The agent
picks it up automatically based on the `description` field; no restart
needed for the CLI, next-session for the IDE.

## Requirements

- `git`
- [`gh`](https://cli.github.com/) (GitHub CLI), authenticated — only needed
  for the PR step

## License

MIT — see [LICENSE](LICENSE).
