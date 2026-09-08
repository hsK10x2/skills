---
name: explain-code
description: >-
  Writes a companion Markdown explanation file for code AI just wrote or any existing file/directory.
  Optimized for junior/beginner developers to study and maintain code independently.
  Focuses on high information density, concrete code mapping, core CS/architecture concepts,
  professional engineering terminology, and zero-fluff token efficiency.
  Use whenever the user asks for code explanation or documentation:
  "이 코드 설명해줘", "코드 설명 md 만들어줘", "이거 문서화해줘", "코드 공부하게 설명서 써줘",
  "explain this code", "document this", or invokes /explain-code.
---

# Explain Code (코드 학습 & 유지보수 설명서 생성기)

AI가 작성한 코드 또는 기존 코드에 대해, **초보/주니어 개발자가 코드를 깊이 이해하고 스스로 유지보수·학습할 수 있도록 돕는 실무형 설명 마크다운 문서**를 생성합니다.

---

## 5대 작성 원칙 (Core Principles)

1. **구체성 (Concrete & Grounded)**:
   - 추상적 설명 금지. 실제 함수명, 변수명, 데이터 타입, 핵심 코드 줄 번호(`L12-25`)를 정확히 명시.
2. **시각적 가독성 (High Readability)**:
   - 긴 줄글 대신 **불릿 포인트**, **표(Table)**, **단계별 번호**를 활용해 한눈에 구조가 보이도록 정리.
3. **학습 가치 제공 (Educational / Study)**:
   - 단순 요약을 넘어 **"왜 이 기술/자료구조/패턴을 썼는가?"**를 실무 CS 관점에서 설명하여 개발 공부가 되도록 구성.
4. **실무 전문 용어 사용 (Engineering Terminology)**:
   - 실무 어휘력 향상을 위해 적절한 기술 용어(Thread-safe, Race Condition, Deadlock, Idempotency, Blueprint, Lazy Evaluation 등)를 적극 사용하고 핵심 개념을 짚어줌.
5. **토큰 효율화 & 고밀도 압축 (Zero Fluff)**:
   - 인사말, 불필요한 미사여구, 당연한 설명은 모두 제거. 핵심 정보만 밀도 높게 압축하여 작성.

---

## 생성 규칙 & 위치

- **단일 파일 대상**: 대상 코드와 동일한 디렉터리에 `<파일명>.explain.md`로 생성 (예: `auth.py` → `auth.py.explain.md`)
- **다중 파일/프로젝트 대상**: 해당 디렉터리 최상위에 단일 `EXPLAIN.md`로 통합 생성 (파일별로 파편화하지 않음)
- **기본 언어**: 한국어 (기술 용어는 영문 병기)

---

## 표준 문서 템플릿 구조

문서 작성 시 다음 5개 섹션 구조를 준수합니다:

```markdown
# <대상 파일명 또는 프로젝트명> 설명서

## 1. 목적 및 해결 과제 (Why)
- **목적**: 이 코드가 왜 존재하는지, 무엇을 해결하는지 1~2문장으로 압축.
- **핵심 입출력/역할 요약**: 무엇을 받아 무엇을 내놓는지 명시.

## 2. 핵심 동작 흐름 (How)
| 단계 | 함수 / 위치 | 역할 및 데이터 변환 |
| :--- | :--- | :--- |
| 1 | `func_name()` (L10) | ... |
| 2 | `process()` (L25) | ... |

- **세부 흐름 요약**: 각 단계별 필수 주의점 및 분기 처리(예외 상황) 간결 기술.

## 3. 💡 주니어 개발자를 위한 핵심 학습 포인트 (Study)
- **[핵심 개념/패턴]**: (예: Factory Pattern, RLock, Lazy Refill 등)
  - **개념 설명**: 이 개념이 무엇인지 실무 관점 요약.
  - **선택 이유 & 대안 비교**: 왜 단순 X 대신 Y를 선택했는지, 트레이드오프는 무엇인지.

## 4. 실전 사용법 (Usage)
```[언어]
# 즉시 복사해서 테스트할 수 있는 최소 실행 코드 스니펫
```

## 5. 실무 관점의 한계점 & 주의사항 (Caveats & Edge Cases)
- **병목 / 한계**: 대용량 트래픽, 분산 환경(멀티 프로세스/서버)에서의 제약사항.
- **잠재적 버그/엣지 케이스**: 놓치기 쉬운 예외 상황 및 향후 리팩토링 포인트.
```

---

## 완료 후 안내
문서 작성을 완료한 후에는 생성된 마크다운 파일의 상대/절대 경로를 간결하게 1줄로 안내합니다.
