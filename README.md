# AP Calculus AB Bilingual Teaching Studio

기초 학생을 위한 **60강 × 한영 카드 8장 = 480장**과 AP Calculus AB 교재입니다. 개념의 이유, 조건 확인, 단계별 풀이, 실수 교정, 확인 문제를 차분하게 설명합니다.

## 바로 보기 / Start here

- **[60강 전체 목록과 카드](instagram/CATALOG.md)** · [첫 강의 8장 미리보기](instagram/exports/L01/preview.jpg)
- [20주 월·수·금 편성표 CSV](instagram/schedule.csv) · [과정 메타데이터](instagram/course.json)
- [작업 재개와 검증 결과](docs/HANDOFF.md) · [콘텐츠 작성 규칙](instagram/README.md)
- **[Logos Crest Math Academy | Suwanee](https://www.instagram.com/logoscrest.math/)** · [첫 게시물](https://www.instagram.com/p/DfftFgOGyO5/) · [게시 기록](instagram/publishing/README.md) · [로고와 브랜드 원본](branding/logos-crest/README.md)
- [공통 작업 지침](AGENTS.md) · [Claude Code 안내](CLAUDE.md) · [승인된 계획](docs/PLAN.md)

카드는 1080×1350px이며 모두 영어와 한국어를 함께 제공합니다. 각 강의 폴더에는 `01.png`–`08.png`, 정답·풀이가 포함된 한영 `caption.txt`, 카드별 `alt-text.json`, `preview.jpg`, 편집 가능한 `lesson.html`, 검증용 `manifest.json`이 있습니다. 사용자 요청에 따라 2026-11-08에 L01–L04를 각 8장씩 수동 게시했습니다. 최근 게시물: [L03 표·그래프의 극한](https://www.instagram.com/p/DffwVVDmwZf/) · [L04 인수분해와 켤레식](https://www.instagram.com/p/DffwrPmGwgb/). 전체 편성표는 상대 주차를 유지하며 자동 게시는 설정하지 않았습니다.

HTML 갤러리는 저장소를 복제한 뒤 `python -m http.server 8000`을 실행하고 `http://localhost:8000/instagram/exports/`에서 열 수 있습니다. GitHub에서는 위 목록의 이미지 링크를 사용하세요.

## 교재 / Textbooks

- [한글 학생 PDF](ap-calculus-ab/deliverables/AP_Calculus_AB_학생용_한글.pdf) · [Word](ap-calculus-ab/deliverables/AP_Calculus_AB_학생용_한글.docx) — 81쪽
- [English student PDF](ap-calculus-ab/deliverables/AP_Calculus_AB_Student_English.pdf) · [Word](ap-calculus-ab/deliverables/AP_Calculus_AB_Student_English.docx) — 81 pages
- [교사용 한영 해설 PDF](ap-calculus-ab/deliverables/AP_Calculus_AB_교사용_해설.pdf) · [Word](ap-calculus-ab/deliverables/AP_Calculus_AB_교사용_해설.docx) — 56쪽
- [교재 원본 안내](ap-calculus-ab/README.md) · [124문항 게시 JSON](ap-calculus-ab/content/question_bank.json)

기존 교재는 102 MCQ, 22 FRQ, 별도 해설 예제 16개를 포함합니다. 기존 검수 보고서의 실제 검수일은 유지했습니다.

## 설치 / Setup

Python 3.12, Node.js 24, pnpm 11.25.0을 사용합니다. 수식은 Matplotlib SVG로 조판하므로 별도 TeX 설치가 필요 없습니다. 한글 글꼴과 SIL OFL 라이선스는 저장소에 포함되어 있습니다.

```bash
git clone https://github.com/sklee935/AP-Calculus.git
cd AP-Calculus
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
npm install -g pnpm@11.25.0
pnpm install --frozen-lockfile
pnpm exec playwright install chromium
```

Windows에서는 `source` 대신 `.venv\Scripts\activate`를 사용합니다. Linux에서 Chromium의 시스템 라이브러리가 없으면 `pnpm exec playwright install --with-deps chromium`을 실행하세요.

## 생성 / Generate

```bash
# 첫 강의를 재생성 / Rebuild the first lesson
python instagram/scripts/build.py --lessons L01
pnpm render --lessons L01
python instagram/scripts/validate.py --lessons L01 --exports

# 전체 60강 / Rebuild all 60 lessons
python instagram/scripts/build.py
pnpm render
python instagram/scripts/catalog.py
```

여러 강의는 `--lessons L01,L02`처럼 지정합니다. `build.py`는 SVG·HTML·캡션·대체텍스트를, `render.mjs`는 PNG와 출처 해시를 생성합니다. `catalog.py`는 최종 PNG로 미리보기와 목록·편성표를 생성합니다.

## 원본을 수정하지 않는 검증 / Read-only validation

```bash
python ap-calculus-ab/scripts/validate_content.py --check
python instagram/scripts/validate.py --complete --exports
python -m unittest discover -s tests -v
pnpm test:layout
```

60개 ID, 480장 구성, 출처·선행 강의, 한영 항목, 캡션 정답, 기호 계산 130개, PNG 크기와 해시, 원본·CSS 변경 후 오래된 출력, 화면 경계를 확인합니다. CI는 이 검증을 실행하고 별도 임시 복사본에서 L01을 다시 만듭니다. 자동 검사가 모든 서술 논증이나 수업 적합성을 증명하지는 않습니다. [실제 검수 범위](docs/QA.md)를 참고하세요.

## 교재 PDF 재생성 / Portable PDF workflow

교재 수정은 Python 원본에서 합니다. PDF/Word나 게시 JSON의 정답만 따로 바꾸지 마세요. 추가로 LibreOffice와 Poppler가 필요합니다.

```bash
# macOS (Homebrew)
brew install --cask libreoffice
brew install poppler
# Ubuntu/Debian: sudo apt-get install libreoffice poppler-utils fontconfig
```

LibreOffice의 `soffice`를 PATH에 넣거나 `--soffice /path/to/soffice`로 지정합니다. macOS 기본 설치 경로는 `/Applications/LibreOffice.app/Contents/MacOS/soffice`입니다. Word 변환 전 `ap-calculus-ab/assets/fonts/NotoSansCJKkr-Regular.otf`를 운영체제에 설치하세요. Linux에서는 `~/.local/share/fonts`에 복사한 뒤 `fc-cache -f`를 실행할 수 있습니다.

```bash
python ap-calculus-ab/scripts/build_books.py
python scripts/render_documents.py --pages
python ap-calculus-ab/scripts/validate_artifacts.py
```

`render_documents.py`는 각 DOCX를 독립 LibreOffice 프로필로 PDF 변환합니다. `--pages`는 Poppler로 모든 페이지를 무시되는 `ap-calculus-ab/tmp/qa`에 렌더링합니다. 변환 뒤 구조 검사와 페이지 화면 검수를 하세요. 교재 생성·변환은 출력 파일과 보고서를 갱신하는 명령이며 CI의 읽기 전용 검사와 구분됩니다.

## 작성과 인수인계 / Editing and handoff

교재의 답은 `ap-calculus-ab/scripts/`의 Python이 원본입니다. `content/question_bank.json`은 교재에서 생성한 게시 데이터입니다. 카드의 대본·수식·그래프·캡션은 `instagram/lessons/Lxx.json`이 원본이며 HTML/PNG를 직접 고치지 않습니다. 새 문항은 정의역·조건·단위와 계산 검증을 함께 작성합니다.

검증한 단위로 변경을 커밋·푸시하고 `docs/HANDOFF.md`에 실제 완료 상태와 다음 작업을 기록하세요. BC 확장 로드맵은 기존 교재에 있으며 BC 본문은 이번 AB 과정에 포함되지 않습니다.

[College Board의 AB 8개 단원](https://apcentral.collegeboard.org/courses/ap-calculus-ab)과 기존 교재를 기준으로 독립 제작했습니다. 2026–27 공식 명확화 자료도 확인했으며, 시험 시간과 문항 수는 기존 교재의 2027 형식과 일치합니다. 공식 기출 복제나 College Board의 승인·제휴를 의미하지 않습니다. 글꼴에는 동봉 OFL이 적용되며, 교재와 강의 콘텐츠에 별도의 오픈 라이선스를 부여하지는 않았습니다.
