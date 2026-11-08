# 카드 강의 편집 / Editing the bilingual course

[60강 목록](CATALOG.md)에서 강의·카드·캡션으로 이동하세요. 모든 강의는 기초 학생을 위한 8장 한영 수업입니다.

## 원본과 생성물

| 파일 | 역할 | 편집 방법 |
|---|---|---|
| `course.json` | 60강 순서, 단원, 선행 강의, 주·요일, 상태 | 주제 변경 시 해당 lesson JSON과 함께 수정 |
| `lessons/Lxx.json` | 한영 대본·수식·그래프·확인 문제·캡션·대체텍스트·검산 명세 | **강의 편집 원본** |
| `templates/card.css` | 공통 화면 규격·색상·타이포그래피 | 모든 강의를 다시 생성·검증 |
| `assets/math`, `assets/graphs` | 생성한 수식·그래프 SVG | 직접 수정하지 않음 |
| `exports/Lxx/` | 최종 8장 PNG·HTML·캡션·대체텍스트·미리보기·manifest | 원본 수정 후 재생성 |
| `schedule.csv`, `CATALOG.md`, `exports/index.html` | 목록과 상대 편성표 | catalog.py로 재생성 |

임시 대본 작성 스크립트는 원본이 아닙니다. 배포하는 JSON을 직접 수정하고 검증하세요. 교재에서 가져온 정답을 바꿀 경우 먼저 교재의 Python 원본을 수정·검증·게시한 뒤 카드에 반영합니다.

## 강의 JSON

- `id`, `number`, `unit`, 한영 `title`, `prerequisites`, `week`, `day`는 과정과 일치합니다.
- `source_question_ids`는 게시 문제은행의 정확한 ID입니다. 원문 복사와 기초형 변형을 모두 포함하며 `example_origin`에 구분합니다. 비어 있으면 독립 작성한 예제로 검산합니다.
- `slides`는 1–8번이며 각각 `title`, `notes`, `alt_text`에 `en`, `ko`가 필요합니다. 수식은 LaTeX 문자열 배열 `math`에 공유합니다.
- 순서는 목표 질문 → 조건·복습 → 개념/표/그래프 → 풀이 1 → 풀이 2 → 해석 → 실수 교정 → 확인 문제입니다.
- `visual.kind`는 `table` 또는 `graph`입니다. 그래프에는 곡선 식, 표시 범위, 열린 점·채운 점, 필요 시 음영·기울기장을 명시합니다. 그래프 식의 독립 변수 이름은 `x`이며 물리 문맥의 t는 축 이름으로 표시할 수 있습니다.
- `self_check.answer`의 한영 정답·이유를 캡션 후반에 넣습니다. 카드 8에는 정답을 노출하지 않습니다.
- `verification`은 `expression`, `expected` 쌍입니다. 최소 2개로 본 예제와 확인 문제를 검사합니다. 허용된 SymPy 함수와 x,y,t,h만 사용합니다. 정확한 유리수는 `Rational`을 쓰세요.
- `status: ready`는 필요한 출력·검증이 완료된 상태입니다. 수정 중에는 `in_progress`로 바꾸고 완료 후 원본과 과정 양쪽을 갱신합니다.

## 한영 설명과 수학

두 언어는 같은 수학적 주장을 해야 합니다. 짧은 문장으로 “무엇을 확인하고, 왜 이 방법을 쓰는지”를 설명하세요. 한글은 자연스러운 존댓말을 사용합니다. 자격·경력·성적 보장을 만들어 넣지 않습니다.

분모가 0이 아닌 조건, 로그·제곱근 정의역, 정리의 연속/미분가능 가정, 적분구간, 단위와 회전축을 생략하지 않습니다. 너무 길면 풀이를 소문항으로 나누고 캡션을 보충합니다. 수식은 `math`에서 조판하고 본문에는 독자가 읽을 수 있는 일반 문자를 씁니다. 캡션에 생 LaTeX를 넣지 마세요.

1080×1350, 바깥 여백 80px, 본문 44px(최소 40px)를 지킵니다. 메타데이터 머리말/꼬리말은 별도입니다. 긴 내용을 글자 축소로 해결하지 말고 문장·수식 행을 나누세요. 대체텍스트에는 수식뿐 아니라 표의 실제 값과 그래프의 곡선·빈점·채운점을 포함합니다.

## 작업 명령

저장소 루트에서 실행합니다. 설치는 루트 README를 참고하세요.

```bash
python instagram/scripts/validate.py --lessons L01
python instagram/scripts/build.py --lessons L01
pnpm render --lessons L01
python instagram/scripts/catalog.py
python instagram/scripts/validate.py --complete --exports
pnpm test:layout
```

원본 해시가 달라지면 오래된 HTML·PNG를 검증에서 거부합니다. CSS 변경 뒤에는 전체 강의를 다시 출력하세요. 모바일 크기와 밀집한 수식/그래프를 직접 확인하고 실제 검수 범위를 `docs/QA.md`에 기록합니다.
