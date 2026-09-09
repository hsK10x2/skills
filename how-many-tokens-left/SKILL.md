---
name: how-many-tokens-left
description: >-
  Pre-flight token gatekeeper. Use this skill when the user runs `/how-many-tokens-left`, or asks
  how much context budget is left, whether a task will fit in the remaining
  tokens, or says things like "토큰 얼마나 남았어", "이 작업 토큰 될까",
  "how many tokens left", "will this run out of context". Measures the current
  session's context usage, estimates what the requested task will consume, and
  STOPS to ask the user before starting work that is likely to run out mid-way.
triggers:
  - "/how-many-tokens-left"
  - "how many tokens left"
  - "토큰 얼마나 남았어"
  - "이 작업 토큰 될까"
  - "토큰 확인"
---

# how-many-tokens-left — Pre-flight Token Gatekeeper

큰 작업을 시작했다가 컨텍스트가 도중에 소진되어 반쯤 망가진 상태로 끝나는 상황을 방지한다.
**측정 → 예측 → 게이트** 3단계로 동작한다.

## Step 1 — 측정 (Measure)

[hmtl.py](./scripts/hmtl.py) 를 실행한다:

```bash
python ~/.claude/skills/how-many-tokens-left/scripts/hmtl.py --json
```

- `--source auto` (기본): Claude / Antigravity 세션 중 가장 최근에 갱신된 쪽을 자동 선택
- `--source antigravity` : Antigravity 세션 강제
- `--source claude` : Claude Code 세션 강제
- `--limit N` : 컨텍스트 한도 수동 지정

반환 필드: `source`, `accuracy`, `model`, `context_limit`, `total_context`,
`tokens_left`, `percent_used`, `breakdown`.

> [!IMPORTANT]
> **정확도 차이를 반드시 사용자에게 밝힐 것.**
> - `accuracy: "exact"` (Claude) — API `usage` 레코드 기반의 실측값.
> - `accuracy: "estimate"` (Antigravity) — Antigravity는 토큰 사용량을 로컬에
>   기록하지 않는다. 트랜스크립트 바이트 수(≈3.5 bytes/token)로 역산한
>   **추정치이며 오차 ±30%**다. 절대 실측값처럼 단정해서 보고하지 말 것.

검증: 스크립트가 0이 아닌 `total_context`를 반환하면 정상. 실패 시 실패 사실을
알리고, 추정만으로 경고한 뒤 사용자 확인을 받는다.

## Step 2 — 예측 (Complexity Matrix)

사용자가 요청한 작업의 범위를 아래 표에 대입해 `min_est ~ max_est`를 산출한다.

| 작업 유형 | 파일 수 | 도구 호출 | 예상 소모 (min ~ max) |
|---|---|---|---|
| 단일 파일 질문/설명 | 1 | 1~3 | 3,000 ~ 8,000 |
| 단일 파일 수정 | 1~2 | 3~6 | 8,000 ~ 20,000 |
| 기능 구현 (신규 모듈) | 3~6 | 8~15 | 25,000 ~ 60,000 |
| 디버깅 (원인 불명) | 5~15 | 15~40 | 40,000 ~ 120,000 |
| 전면 리팩터링 | 10+ | 30+ | 80,000 ~ 200,000+ |
| 테스트 작성 동반 | +대상 파일 수 | +파일당 3 | +10,000 ~ +40,000 |

가산 규칙:
- 파일 1개 읽기 = 1,000 ~ 5,000 (평균 2,500)
- 도구 호출 1회 = 2,000 ~ 6,000 (결과 + 재추론 누적)
- 코드 생성 응답 1회 = 1,500 ~ 4,000
- 미지의 코드베이스 탐색이 필요하면 max에 ×1.5

## Step 3 — 게이트 (Gate)

- **안전 마진**: `context_limit`의 5% 또는 10,000 tokens 중 큰 값
- **위험 조건**: `max_est > tokens_left` 또는 `tokens_left - max_est < 안전 마진`

### [경우 A] 위험 — 작업을 시작하지 말고 정지(Pause)

```text
============================================================
[TOKEN] 토큰 부족 경고 (Context Budget Alert)
============================================================
- 측정 방식      : {source} / {accuracy}
- 현재 잔여 토큰 : {tokens_left:,} tokens ({100-percent_used:.1f}% 남음)
- 예상 작업 소모량: {min_est:,} ~ {max_est:,} tokens
- 위험 판단      : 작업 완주 불가 위험 (Deficit: {deficit:,} tokens 부족 예상)
============================================================

"토큰을 다 사용하고도 작업을 못 끝낼 수도 있는데 그래도 작업을 계속 진행하시겠습니까?"

[선택지를 골라주세요]:
1. 그래도 계속 진행 (토큰 소진 시까지 가능한 곳까지 작업)
2. 컨텍스트 압축 후 진행 (Claude: /compact · Antigravity: 새 대화 + 요약 인계)
3. 작업을 작은 단위로 분할하여 진행 (예: 1단계 파일 분석/설계만 먼저)
4. 작업 취소
```

사용자가 번호나 지시를 입력하기 전까지 **반드시 대기**한다. 임의로 진행하지 않는다.

### [경우 B] 안전 — 2줄 브리핑 후 즉시 착수

```text
[TOKEN] 토큰 충분: 잔여 {tokens_left:,} tokens / 예상 소모 {est:,} tokens (안전 마진 확보)
작업을 시작합니다...
```

불필요한 추가 확인 질문을 하지 않는다.

## 참고

- 인자 없이 `/how-many-tokens-left`만 실행되면 토큰 현황만 출력하고 종료한다.
- 컨텍스트 한도 기본값: Claude 200,000 / Antigravity 1,000,000. 다르면 `--limit`으로 지정.
- 스크립트는 Python 표준 라이브러리만 사용하며 외부 의존성이 없다.
