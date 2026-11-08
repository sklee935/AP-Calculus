# Manual publication log / 수동 게시 기록

The user requested the profile launch and first post, then separately requested **one more** post. On 2026-11-08 (America/New_York), these two publications were completed on [@logoscrest.math](https://www.instagram.com/logoscrest.math/).

| Lesson | Published content | Location | Record |
|---|---|---|---|
| L01 · 극한의 뜻 / What a limit means | [Eight-card Instagram carousel](https://www.instagram.com/p/DfftFgOGyO5/) | [Suwanee, Georgia](https://www.instagram.com/explore/locations/229850873/suwanee-georgia/) | [Post manifest](L01-post.json) · [Actual caption](L01-caption.txt) |
| L02 · 좌우극한 / One-sided limits | [Eight-card Instagram carousel](https://www.instagram.com/p/DffuwIvm9b1/) | [Suwanee, Georgia](https://www.instagram.com/explore/locations/229850873/suwanee-georgia/) | [Post manifest](L02-post.json) · [Actual caption](L02-caption.txt) |

For **L01**, the original eight PNGs were uploaded in `01.png`–`08.png` order with **4:5** selected and the original filter retained. The branded caption adds the public academy name, city and five topic/location hashtags to the validated bilingual lesson. All eight alt texts came from the lesson export, joined as `English | 한국어` because Instagram's single-line fields remove newlines. The caption, original function restriction `x≠3`, check restriction `x≠4`, and answers 6 and 8 were retained. No Facebook cross-post was enabled.

Instagram showed “Your post has been shared.” The public profile then showed one post, the new crest avatar, Suwanee bio and this carousel. The live post displayed its city link and bilingual caption; advancing through the carousel reached `img_index=8` and the L01 · 08/08 self-check. Final images 1 and 8 were visually inspected in the live post. This does not claim a separate second visual review of every middle card.

For **L02**, the same 8-card order, 4:5 ratio, original filter, bilingual alt-text join and city tag were used. The caption is 888 characters, including brand introduction and five hashtags, and retains the validated English/Korean teaching text. The main example has left limit 2 and right limit 5; the check on `|x|/x` has left limit −1 and right limit 1. Both two-sided limits do not exist. The local contact sheet was reviewed; read-only validation passed 8 cards, 3 math checks and 8 PNGs. Instagram confirmed sharing, the profile showed **two posts**, and the live L02 carousel reached all eight indices. Cards 1, 3 (the graph) and 8 were visually inspected in the published post. No Facebook cross-post was enabled.

## Continue safely

- `../lessons/Lxx.json` remains the editable teaching-script and answer authority. `Lxx-caption.txt` records the published branded caption, not a competing math source. If a lesson changes, update the generated assets and explicitly record any later post correction.
- `Lxx-post.json` records actual publication status, public URL and selected city. All asset paths are relative to that manifest's directory.
- Future posting, editing, cross-posting and dated scheduling require a separate user request. L03–L60 remain prepared assets; do not post them just because they are ready.
- The 20-week course schedule remains relative. There is no posting daemon, login token or account password in this repository.
