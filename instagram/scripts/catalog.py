"""Build course links, a relative schedule, and contact previews from finished PNGs."""
from pathlib import Path
import csv,html,json
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[2];IG=ROOT/'instagram'
font=ImageFont.truetype(str(ROOT/'ap-calculus-ab/assets/fonts/NotoSansCJKkr-Regular.otf'),22)
course=json.loads((IG/'course.json').read_text());rows=course['lessons']
with (IG/'schedule.csv').open('w',newline='') as f:
 w=csv.writer(f,lineterminator='\n');w.writerow(['week','day','lesson','unit','title_en','title_ko','status'])
 for d in rows:w.writerow([d['week'],d['day'],d['id'],d['unit'],d['title']['en'],d['title']['ko'],d['status']])
md=['# 60강 카드 강의 목록 / Course catalog','','월·수·금 3회 × 20주. 날짜와 자동 게시 설정은 포함하지 않습니다. / Relative weeks only.','','[전체 편집 원본](lessons/) · [CSV 편성표](schedule.csv) · [브라우저 갤러리](exports/index.html) · [실제 게시 기록](publishing/README.md)','','| 강의 | 주/요일 | 주제 | 카드 미리보기 | 게시 자료 |','|---|---|---|---|---|']
gallery=[]
for d in rows:
 id=d['id'];folder=IG/'exports'/id
 sheet=Image.new('RGB',(1440,948),'#e2e7eb');draw=ImageDraw.Draw(sheet)
 for i in range(8):
  with Image.open(folder/f'{i+1:02d}.png') as im:
   im=im.convert('RGB');im.thumbnail((348,435));x=(i%4)*360+6;y=(i//4)*474+32
   sheet.paste(im,(x,y));draw.text((x,y-28),f'{id} · {i+1:02d}/08',font=font,fill='#17243b')
 sheet.save(folder/'preview.jpg',quality=90)
 md.append(f"| [{id}](lessons/{id}.json) | {d['week']} / {d['day']} | {d['title']['en']}<br>{d['title']['ko']} | [8장](exports/{id}/preview.jpg) | [PNG 폴더](exports/{id}/) · [캡션](exports/{id}/caption.txt) · [대체텍스트](exports/{id}/alt-text.json) |")
 gallery.append(f'<article><h2>{id} · {html.escape(d["title"]["en"])}</h2><p lang="ko">{html.escape(d["title"]["ko"])}</p><a href="{id}/lesson.html"><img loading="lazy" src="{id}/preview.jpg" alt="{id} eight bilingual cards"></a><p><a href="{id}/caption.txt">Caption / 캡션</a> · <a href="{id}/alt-text.json">Alt text / 대체텍스트</a> · <a href="../lessons/{id}.json">JSON source</a></p></article>')
(IG/'CATALOG.md').write_text('\n'.join(md)+'\n')
(IG/'exports/index.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AP Calculus AB · 60 bilingual lessons</title><style>body{font-family:system-ui,sans-serif;background:#fafbf8;color:#17243b;max-width:1440px;margin:0 auto;padding:24px}article{margin:48px 0}img{width:100%;height:auto}a{color:#2463eb}</style><h1>AP Calculus AB · 60 bilingual lessons</h1><p lang="ko">기초부터 배우는 한영 미적분 강의 · 60강 / 480장</p>'+''.join(gallery)+'</html>')
print('60 previews, catalog, browser gallery and relative schedule generated')
