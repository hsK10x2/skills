# 에이전트 스킬 모음

**저만의 Claude Code**와 **Google Antigravity**를 위한 커스텀 [Agent Skills](https://docs.claude.com/en/docs/claude-code/skills) 모음입니다.
https://claude.ai/code/artifact/40113156-89fe-4b69-9f90-0fa6360e035c

개발 워크플로를 단순화하고, Git 작업을 자동화하며, 실행에 앞서 결정을 검증하고, 코드 학습과 유지보수를 위한 고밀도 문서를 생성하도록 설계했습니다.

---

## 📦 포함된 스킬

| 스킬 | 설명 | 트리거 |
| :--- | :--- | :--- |
| **[`commit-and-pr`](./commit-and-pr)** | 작업 트리 변경사항을 검사하고 Conventional Commits 메시지를 작성한 뒤 커밋·푸시하고, `gh`로 GitHub PR을 엽니다. | `/commit-and-pr`, `커밋해줘`, `PR 만들어줘`, `commit this and open a PR` |
| **[`explain-code`](./explain-code)** | 코드 학습과 유지보수를 위한 고밀도의 주니어 개발자 친화적 마크다운 설명 문서(`<file>.explain.md` / `EXPLAIN.md`)를 생성합니다. | `/explain-code`, `이 코드 설명해줘`, `코드 설명 md 만들어줘`, `explain this code` |
| **[`grill-me`](./grill-me)** | 집요한 질문으로 사용자와의 맥락을 확장하고, 제약을 발굴하며, 숨겨진 전제에 의문을 제기하고, 압축된 결정 로그(`.grill/<slug>.md`)를 생성합니다. | `/grill-me`, `grill me`, `interview me`, `질문해줘`, `인터뷰해줘`, `의도 구체화해줘`, `아이디어 검증해줘` |

---

## 🚀 설치 방법

오픈 Agent Skills 표준(`SKILL.md`)을 지원하는 모든 AI 에이전트에서 동작합니다.

### Claude Code

저장소를 클론한 뒤 원하는 스킬을 Claude 스킬 디렉터리로 복사합니다:

```bash
git clone https://github.com/hsK10x2/skills.git /tmp/my-skills

# 모든 스킬을 전역 설치 (모든 프로젝트에서 사용 가능)
cp -r /tmp/my-skills/commit-and-pr ~/.claude/skills/
cp -r /tmp/my-skills/explain-code ~/.claude/skills/
cp -r /tmp/my-skills/grill-me ~/.claude/skills/

# 또는 특정 프로젝트에만 설치
cp -r /tmp/my-skills/<skill-name> <project>/.claude/skills/
```

### Google Antigravity

스킬 디렉터리 또는 `SKILL.md`를 Antigravity 설정 디렉터리로 복사합니다:

```bash
# 전역 설치 (권장 — 모든 워크스페이스에서 사용 가능)
cp -r /tmp/my-skills/<skill-name> ~/.gemini/config/skills/

# 또는 프로젝트별 설치
cp -r /tmp/my-skills/<skill-name> <project>/.agents/skills/
```

Antigravity는 다음 턴 또는 세션에서 스킬을 자동으로 감지하고 활성화합니다.

---

## 📖 스킬 개요

### 1. `commit-and-pr`
- **맥락 기반 커밋**: `git status`와 `git diff`를 검사해 변경의 *이유*를 추출합니다.
- **Conventional Commits**: [Conventional Commits](https://www.conventionalcommits.org/) 형식(`feat:`, `fix:`, `docs:`, `refactor:` 등)을 엄격히 따릅니다.
- **브랜치 보호**: `main`/`master`에 있으면 자동으로 기능 브랜치를 생성합니다.
- **자동 PR 생성**: `gh pr create`로 Summary, Changes, Test Plan 섹션을 갖춘 구조화된 GitHub PR을 엽니다.
- **안전 우선**: 위험한 작업(force-push, 이미 푸시된 커밋의 amend) 전에는 반드시 확인을 구하며, 민감정보가 감지되면 커밋을 거부합니다.

### 2. `explain-code`
- **근거 기반 설명**: 함수명, 줄 번호, 매개변수에 직접 매핑되는 설명을 작성합니다.
- **높은 가독성**: 긴 줄글 대신 구조화된 표와 번호 매긴 단계로 대체합니다.
- **학습 중심 (Study Focus)**: 핵심 CS 개념(예: 동시성, RLock, 지연 평가, 팩토리 패턴)과 아키텍처 트레이드오프를 짚어주는 **💡 핵심 학습 포인트**를 포함합니다.
- **실무 전문 용어**: 군더더기 없이 정확한 엔지니어링 개념을 주니어 개발자에게 설명합니다.
- **제로 플러프**: 토큰 효율을 극대화하는 고밀도 포맷입니다.
- **자동 범위 판단**: 단일 파일은 `<filename>.explain.md`, 다중 파일 프로젝트는 `EXPLAIN.md`로 출력합니다.

### 3. `grill-me`
- **한 번에 한 질문**: 추천 답변과 함께 질문을 하나씩 던져, 사용자가 백지가 아닌 구체적인 안에 반응하게 합니다.
- **분기 전에 파고들기**: 표면적인 답변을 넘어 숨겨진 전제, 제약, 언급되지 않은 대안을 끌어냅니다.
- **다각도 렌즈**: 원리 우선 분석(First-principles), 사전 부검(Pre-mortem), 반대 입장 스틸맨(Steelman opposite), 5 Whys, 되돌릴 수 있는지 여부(Reversibility), 경계 테스트(Boundary testing)를 활용합니다.
- **실행 지향적 수렴**: 다음 구체적 단계(코드 작성, 문서 초안, 아키텍처 설계)가 준비되면 마무리합니다.
- **압축된 세션 로그**: `.grill/<slug>.md`에 다듬어진 의도, 절대 타협 불가 제약, 핵심 결정(고려한 대안 포함), 전제, 미해결 질문, 범위 외 항목을 요약한 마크다운 보고서를 자동 생성합니다.

---

## ➕ 새 스킬 추가하기

이 저장소에 새 스킬을 추가하려면:

1. `SKILL.md` 파일을 포함한 새 스킬 디렉터리를 만듭니다:
   ```
   <skill-name>/
   └── SKILL.md
   ```
2. `.gitignore`에서 새 스킬 디렉터리를 예외 처리합니다:
   ```gitignore
   !<skill-name>/
   !<skill-name>/**
   ```
3. `README.md`의 카탈로그 표와 설명을 업데이트합니다.
4. 커밋하고 푸시합니다:
   ```bash
   git add .gitignore README.md <skill-name>/
   git commit -m "feat(skills): add <skill-name> skill"
   git push origin main
   ```

---

## 🛠️ 요구사항

- **`git`**
- **[`gh`](https://cli.github.com/) (GitHub CLI)**, 인증 완료 — `commit-and-pr`의 PR 생성 기능에 필요합니다.

---

## 📄 라이선스

MIT — [LICENSE](LICENSE) 참고.
