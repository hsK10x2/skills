# Agent Skills Collection

A collection of custom [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for **Claude Code** and **Google Antigravity**.

Designed to streamline development workflows, automate Git operations, and generate high-density documentation for learning and maintaining code.

---

## 📦 Included Skills

| Skill | Description | Triggers |
| :--- | :--- | :--- |
| **[`commit-and-pr`](./commit-and-pr)** | Inspects working-tree changes, drafts Conventional Commits messages, commits, pushes, and opens GitHub PRs via `gh`. | `/commit-and-pr`, `커밋해줘`, `PR 만들어줘` |
| **[`explain-code`](./explain-code)** | Generates high-density, junior-developer-friendly Markdown explanation documents (`<file>.explain.md` / `EXPLAIN.md`) for code study and maintenance. | `/explain-code`, `이 코드 설명해줘`, `코드 설명 md 만들어줘` |

---

## 🚀 Installation

Works with any AI agent supporting the open Agent Skills standard (`SKILL.md`).

### Claude Code

Clone this repository and copy the desired skill(s) into your Claude skills folder:

```bash
git clone https://github.com/hsK10x2/commit-and-pr.git /tmp/my-skills

# Install all skills globally (all projects)
cp -r /tmp/my-skills/commit-and-pr ~/.claude/skills/
cp -r /tmp/my-skills/explain-code ~/.claude/skills/

# Or install in a specific project
cp -r /tmp/my-skills/<skill-name> <project>/.claude/skills/
```

### Google Antigravity

Copy the skill's `SKILL.md` to your Antigravity configuration directory:

```bash
# Global installation (recommended)
cp -r /tmp/my-skills/<skill-name> ~/.gemini/config/skills/

# Or per-project installation
cp -r /tmp/my-skills/<skill-name> <project>/.agents/skills/
```
Antigravity automatically discovers and activates skills on the next turn or session.

---

## 📖 Skill Overviews

### 1. `commit-and-pr`
- Inspects `git status` and `git diff` to extract the *why* behind changes.
- Formats messages in [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, etc.).
- Automatically creates a feature branch if on `main`/`master`.
- Opens a structured GitHub PR using `gh pr create` (Summary / Changes / Test Plan).
- Asks for confirmation before any destructive actions (force-push, amending pushed commits).

### 2. `explain-code`
- **Grounded & Concrete**: Maps explanations directly to function names, line numbers, and parameters.
- **High Readability**: Replaces walls of text with structured tables and numbered steps.
- **Educational (Study Focus)**: Includes **💡 Key Study Points** detailing core CS concepts (e.g., Concurrency, RLock, Lazy Evaluation, Factory Pattern) and architectural trade-offs.
- **Professional Terminology**: Accurately explains engineering concepts for junior developers.
- **Zero Fluff**: High-density format maximizing token efficiency.
- **Automatic Scoping**: Outputs `<filename>.explain.md` for single files, and `EXPLAIN.md` for multi-file projects.

---

## 🛠️ Requirements

- **`git`**
- **`gh`** ([GitHub CLI](https://cli.github.com/)), authenticated — required for `commit-and-pr` PR creation.

---

## 📄 License

MIT — see [LICENSE](LICENSE).
