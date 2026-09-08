# Agent Skills Collection

A curated collection of custom [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) for **Claude Code** and **Google Antigravity**.

Designed to streamline development workflows, automate Git operations, pressure-test decisions before implementation, and generate high-density documentation for studying and maintaining code.

---

## 📦 Included Skills

| Skill | Description | Triggers |
| :--- | :--- | :--- |
| **[`commit-and-pr`](./commit-and-pr)** | Inspects working-tree changes, drafts Conventional Commits messages, commits, pushes, and opens GitHub PRs via `gh`. | `/commit-and-pr`, `커밋해줘`, `PR 만들어줘`, `commit this and open a PR` |
| **[`explain-code`](./explain-code)** | Generates high-density, junior-developer-friendly Markdown explanation documents (`<file>.explain.md` / `EXPLAIN.md`) for code study and maintenance. | `/explain-code`, `이 코드 설명해줘`, `코드 설명 md 만들어줘`, `explain this code` |
| **[`grill-me`](./grill-me)** | Relentlessly interviews the user to expand context, uncover constraints, challenge hidden assumptions, and generate distilled decision logs (`.grill/<slug>.md`). | `/grill-me`, `grill me`, `interview me`, `질문해줘`, `인터뷰해줘`, `의도 구체화해줘`, `아이디어 검증해줘` |

---

## 🚀 Installation

Works with any AI agent supporting the open Agent Skills standard (`SKILL.md`).

### Claude Code

Clone this repository and copy the desired skill(s) into your Claude skills directory:

```bash
git clone https://github.com/hsK10x2/skills.git /tmp/my-skills

# Install all skills globally (available across all projects)
cp -r /tmp/my-skills/commit-and-pr ~/.claude/skills/
cp -r /tmp/my-skills/explain-code ~/.claude/skills/
cp -r /tmp/my-skills/grill-me ~/.claude/skills/

# Or install in a specific project only
cp -r /tmp/my-skills/<skill-name> <project>/.claude/skills/
```

### Google Antigravity

Copy the skill's directory or `SKILL.md` to your Antigravity configuration directory:

```bash
# Global installation (recommended - available in all workspaces)
cp -r /tmp/my-skills/<skill-name> ~/.gemini/config/skills/

# Or per-project installation
cp -r /tmp/my-skills/<skill-name> <project>/.agents/skills/
```

Antigravity automatically discovers and activates skills on the next turn or session.

---

## 📖 Skill Overviews

### 1. `commit-and-pr`
- **Context-Aware Commits**: Inspects `git status` and `git diff` to extract the *why* behind changes.
- **Conventional Commits**: Formats messages strictly in [Conventional Commits](https://www.conventionalcommits.org/) (`feat:`, `fix:`, `docs:`, `refactor:`, etc.).
- **Branch Protection**: Automatically creates a feature branch if on `main`/`master`.
- **Automated PR**: Opens a structured GitHub PR using `gh pr create` with Summary, Changes, and Test Plan sections.
- **Safety First**: Asks before destructive actions (force-push, amending pushed commits) and refuses to commit if secrets are detected.

### 2. `explain-code`
- **Grounded & Concrete**: Maps explanations directly to function names, line numbers, and parameters.
- **High Readability**: Replaces walls of text with structured tables and numbered steps.
- **Educational (Study Focus)**: Includes **💡 Key Study Points** detailing core CS concepts (e.g., Concurrency, RLock, Lazy Evaluation, Factory Pattern) and architectural trade-offs.
- **Professional Terminology**: Accurately explains engineering concepts for junior developers without fluff.
- **Zero Fluff**: High-density format maximizing token efficiency.
- **Automatic Scoping**: Outputs `<filename>.explain.md` for single files, and `EXPLAIN.md` for multi-file projects.

### 3. `grill-me`
- **One Question at a Time**: Asks focused questions one by one, paired with recommended options so the user has something concrete to react against.
- **Drilldown Before Branching**: Pushes past surface-level answers to uncover hidden assumptions, constraints, and unstated alternatives.
- **Multi-Angle Lenses**: Pulls from First-principles, Pre-mortem, Steelman opposite, 5 Whys, Reversibility, and Boundary testing.
- **Action-Oriented Convergence**: Concludes when the next concrete step (writing code, drafting a brief, architecture design) is ready.
- **Distilled Session Logs**: Automatically produces a concise markdown report at `.grill/<slug>.md` capturing Refined Intent, Non-negotiable Constraints, Key Decisions (with alternatives considered), Assumptions, Open Questions, and Out of Scope items.

---

## ➕ Adding New Skills

To add a new skill to this repository:

1. Create a new skill directory containing a `SKILL.md` file:
   ```
   <skill-name>/
   └── SKILL.md
   ```
2. Unignore the new skill directory in `.gitignore`:
   ```gitignore
   !<skill-name>/
   !<skill-name>/**
   ```
3. Update the `README.md` catalog table and description.
4. Commit and push:
   ```bash
   git add .gitignore README.md <skill-name>/
   git commit -m "feat(skills): add <skill-name> skill"
   git push origin main
   ```

---

## 🛠️ Requirements

- **`git`**
- **[`gh`](https://cli.github.com/) (GitHub CLI)**, authenticated — required for `commit-and-pr` PR creation.

---

## 📄 License

MIT — see [LICENSE](LICENSE).
