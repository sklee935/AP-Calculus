# AP Calculus AB 한영 수업 교재

Calculus AB 수업을 위한 독립 제작 초판이다. 개념 요약과 예제, 단원 연습, 실전 모의고사와 교사용 해설을 함께 제공한다. 공식 교육과정과 2027년 시험 형식은 2026년 10월 28일 College Board 자료로 확인했다.

## 교재 파일

`deliverables/`에 다음 세 권의 Word와 PDF가 있다.

- `AP_Calculus_AB_학생용_한글`: 한글 개념과 예제, 진단, 단원 연습과 모의고사
- `AP_Calculus_AB_Student_English`: 같은 문항 ID를 사용하는 영문판
- `AP_Calculus_AB_교사용_해설`: 한영 해설, 객관식 정답표, 서술형 부분점수 기준

학생용 교재에는 정답을 넣지 않았다. 교사용 파일의 같은 문항 ID로 해설을 찾을 수 있다. Word의 수식은 기본적으로 편집 가능한 Office 수식이며 한글 글꼴을 내장했다.

## 구성

| 구분 | 객관식 | 서술형 | 합계 |
|---|---:|---:|---:|
| 선수학습 진단 | 12 | 0 | 12 |
| 8개 단원 연습 | 48 | 16 | 64 |
| 실전 모의고사 | 42 | 6 | 48 |
| 전체 | 102 | 22 | 124 |

별도로 해설 예제 16개와 직접 작성한 그래프 8개를 포함한다. 개념 본문은 첫 수업에 사용할 수 있는 압축 설명이며, 학생별 숙련을 위한 추가 문항이나 여러 회차의 모의고사까지 갖춘 대규모 문제은행은 아니다.

모의고사는 2027년 형식에 맞춰 객관식 A 29문항 62분, B 13문항 38분, 서술형 A 2문항 30분, B 4문항 60분으로 구성했다. 객관식의 여덟 단원 비율도 공식 공개 범위 안에 들어간다. 계산기 구간이 표시되어 있고 수치답은 중간 반올림 없이 마지막에 소수 셋째 자리까지 반올림하도록 안내한다.

## 내용 원본과 검증

- `content/question_bank.json`: 한영 문항, 선택지, 정답, 해설과 문항별 검산 명세
- `content/curriculum.json`: 8개 단원, 개념 본문, 예제, 공식 참고 링크와 BC 확장 계획
- `content/student_ko.md`, `content/student_en.md`: 브라우저에서 읽는 학생용 본문
- `content/teacher_solutions.md`: 교사용 한영 해설
- `content/teacher_blueprint.csv`: 문항별 단원, 유형, 계산기 정책과 정답
- `content/validation_report.json`: 수학 내용 검산 결과
- `content/layout_report.json`: 최종 PDF의 페이지 수와 구조 검증 결과

객관식 88개는 기호 또는 고정밀 수치 계산으로 정답과 오답 선택지를 비교했다. 서술형에서 37개의 수치 또는 등식과 예제 16개의 계산도 확인한다. 수치적분은 별도의 합성 Simpson 계산과 교차 검증하고, 방정식의 수치해는 원래 식의 잔차를 확인한다. 나머지 개념 판단, 논증, 단위와 서술형 채점기준은 편집 검토 대상이며, 계산 도구가 모든 문장 논증을 검증하는 것은 아니다.

채점기준은 수업용 자체 기준이다. 모의고사 100점 지표는 객관식 50점과 서술형 50점을 합산하며 공식 AP 1~5등급을 예측하거나 환산하지 않는다. 공식 기출문제를 복제하지 않았고 College Board 승인·제휴 교재가 아니다.

## 다시 만들기

저장소 루트의 [설치·생성 안내](../README.md)를 따릅니다. Python 3.12, Node/Chromium은 카드 제작에, LibreOffice와 Poppler는 교재 PDF 변환과 페이지 검수에 사용합니다. 특정 개발 앱의 설치 경로에 의존하지 않습니다.

저장소 루트에서 실행합니다.

```bash
# 원본을 변경하지 않는 내용 검사
python ap-calculus-ab/scripts/validate_content.py --check
# 교재 원본에서 게시 데이터와 Word 재생성
python ap-calculus-ab/scripts/build_books.py
# LibreOffice PDF 변환 + Poppler 페이지 렌더링
python scripts/render_documents.py --pages
python ap-calculus-ab/scripts/validate_artifacts.py
```

마지막 구조 검사는 모든 교재의 페이지 PNG가 `tmp/qa/final-korean`, `final-english`, `final-teacher`에 있어야 실행됩니다. 새 PDF의 페이지 화면도 확인합니다. CI는 `--check`를 사용하며 원본/게시 데이터를 갱신하지 않습니다. 생성 명령과 구조 검사는 출력 및 보고서를 갱신합니다.

수정 시 정답을 PDF나 게시 JSON에서 직접 고치지 말고 `scripts/curriculum.py`, `scripts/questions.py`, `scripts/unit_frq.py`, `scripts/exam.py` 원본을 고친 뒤 검증하고 생성합니다. `tmp/`는 렌더링·검수용이며 Git에서 제외합니다.

한글 글꼴 Noto Sans CJK KR의 전체 원본·부분 글꼴·SIL Open Font License는 `assets/fonts/`에 있습니다. Word 변환 전 운영체제에 전체 OTF 글꼴을 설치하세요. 원본 제공처는 [Noto CJK](https://github.com/notofonts/noto-cjk)입니다.

## BC 확장

AB의 8개 단원을 유지하고 BC 추가 적분법, 오일러 방법과 로지스틱 모형, 매개변수·벡터·극좌표, 수열과 급수를 추가하는 계획을 원본과 교재 말미에 기록했다. 이번 배포에는 AB 교재가 완성되어 있으며 BC 본문과 BC 모의고사는 포함되지 않는다.
