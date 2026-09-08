---
name: commit-and-pr
description: >-
  Automates writing git commit messages and creating GitHub pull requests.
  Inspects staged/unstaged changes, drafts a Conventional Commits message,
  commits, pushes to a feature branch, and opens a PR (via the `gh` CLI) with
  a structured Summary / Changes / Test Plan description. Use this skill when
  the user asks to commit changes, write a commit message, open/create a PR
  or pull request, "커밋해줘", "커밋 메시지 써줘", "PR 만들어줘", "풀리퀘스트 올려줘",
  ship a branch, or wrap up a change for review.
---

# Commit & PR Automation

Turns a working-tree diff into a clean commit and, optionally, a ready-to-review
GitHub pull request — without the user having to dictate commit-message wording
or PR boilerplate each time.

## When to use this skill

- User asks to commit their changes ("커밋해줘", "commit this", "얘 커밋 좀")
- User asks for a commit message only ("커밋 메시지 뭐라고 쓸까")
- User asks to open a PR ("PR 만들어줘", "pull request 올려줘", "ship this")
- User asks to do both in one go ("커밋하고 PR까지 올려줘")

Do **not** use this skill just to explain what `git commit` does, or for
read-only history questions (`git log`, `git blame`) — those need no
automation.

## Preconditions — check before doing anything

1. Confirm this is a git repo: `git rev-parse --is-inside-work-tree`. If not,
   stop and tell the user.
2. Confirm `gh` is available and authenticated if a PR is requested:
   `gh auth status`. If not authenticated, stop and tell the user to run
   `gh auth login` — do not attempt to log in on their behalf.
3. Run `git status --porcelain` and `git branch --show-current`.
   - If there is nothing to commit, say so and stop.
   - If the current branch is the repo's default branch (`main`/`master`, or
     whatever `git symbolic-ref refs/remotes/origin/HEAD` resolves to),
     **do not commit directly on it**. Create a new branch first
     (`git checkout -b <type>/<short-slug>`) unless the user explicitly says
     to commit on the default branch.

## Step 1 — Understand the diff

```bash
git status
git diff            # unstaged
git diff --staged   # staged
```

- If nothing is staged and the user didn't specify which files, ask whether
  to stage everything (`git add -A`) or only specific files — don't guess on
  a repo with unrelated in-flight changes.
- Read enough of the diff to describe *why* the change was made, not just
  *what* changed. If the intent isn't obvious from the diff alone (e.g. a
  one-line config flip), ask the user rather than inventing a rationale.

## Step 2 — Write the commit message

Use [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <short imperative summary, ≤72 chars>

<body: why this change, not a restatement of the diff — wrap ~72 cols>

<optional footer: BREAKING CHANGE:, Fixes #123, refs>
```

Type reference:

| type       | use for                                              |
|------------|-------------------------------------------------------|
| `feat`     | new user-facing capability                             |
| `fix`      | bug fix                                                 |
| `docs`     | documentation only                                      |
| `refactor` | code change that's neither a fix nor a feature          |
| `test`     | adding or fixing tests only                             |
| `chore`    | tooling, deps, build config, no source behavior change  |
| `style`    | formatting only, no logic change                        |
| `perf`     | performance improvement                                 |

Rules:
- Summary line: imperative mood ("add", not "added"/"adds"), no trailing period.
- Skip the type prefix only if the repo's existing `git log` history clearly
  doesn't use Conventional Commits — match the repo's actual convention,
  don't impose one.
- If the diff mixes clearly unrelated changes, tell the user and suggest
  splitting into separate commits rather than writing one message that tries
  to cover both.
- Never invent a ticket/issue number — only add `Fixes #N` if the user gave one.
- Append whatever commit-message attribution footer this session's own
  instructions specify (Claude Code appends a `Co-Authored-By:` / session-link
  footer automatically) — don't drop it just because this skill's template
  above doesn't show it.

## Step 3 — Commit

```bash
git add -A            # or the specific files agreed in Step 1
git commit -m "$(cat <<'EOF'
<type>(<scope>): <summary>

<body>
EOF
)"
```

- Never use `--no-verify` / skip hooks unless the user explicitly says to.
- If a pre-commit hook fails, fix the underlying issue (or report it) —
  don't bypass it.
- Never `git commit --amend` on a commit that's already been pushed/shared
  unless the user explicitly asks.

## Step 4 — Push

```bash
git push -u origin <branch-name>
```

- Never `--force` (or `--force-with-lease`) without the user explicitly
  asking for it, and only after confirming no one else's work would be
  clobbered.

## Step 5 — Open the PR (only if the user asked for a PR)

```bash
gh pr create --title "<same summary as commit, or a slightly fuller title>" --body "$(cat <<'EOF'
## Summary
- <1-3 bullets: what changed and why, for a reviewer skimming>

## Changes
- <notable files/areas touched, grouped logically>

## Test Plan
- <how this was verified: tests run, manual steps, or "N/A" with a reason>
EOF
)"
```

- Base branch: default to the repo's default branch unless the user names
  another target.
- If the branch already has an open PR, update it (`gh pr edit`) instead of
  creating a duplicate — check with `gh pr list --head <branch>` first.
- Draft PRs: pass `--draft` if the user says the work is WIP / not ready for
  review.
- After creation, hand back the PR URL from `gh pr create`'s output — don't
  reconstruct it manually.
- Never merge the PR yourself (`gh pr merge`) unless the user explicitly asks.
- Append whatever PR-body attribution footer this session's own instructions
  specify (Claude Code appends a "Generated with Claude Code" footer
  automatically).

## Guardrails

- Ask before any destructive or hard-to-reverse step (force-push, amending a
  pushed commit, merging, committing directly to the default branch) unless
  the user has already authorized it for this session.
- If `git diff` shows secrets/credentials being added, stop and flag it
  instead of committing.
- Keep the commit message and PR description honest about what was actually
  tested — don't claim a test plan that wasn't run.
