# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/Dimah28/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/Dimah28/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

Entry for the make.fun bounty **"Sum up 17 November's world news in one image"** ([news-image-20261117](https://make.fun/bounty/news-image-20261117), $250, ends Wed 19 Nov 2026 07:00 WIB).

## The image

`entry.png` — a 1024×1024 newspaper front page drawn entirely procedurally with the Python standard library only (hand-rolled 5x7 bitmap font + hand-encoded PNG), in the style of a clean editorial infographic. 37 real stories from Tuesday 17 November 2026:

- masthead: **THE DAY IN WORLD NEWS — Tuesday 17 November 2026**, "37 stories · 6 continents · one day"
- hero: **Kerch Bridge span falls into the strait** — Ukraine calls it an "unprecedented operation"; the Kremlin vows to rebuild
- **12 illustrated panels** (4×3 grid), one story each with a dateline kicker, bold serif headline and a drawn pictogram: tankers ablaze in the Strait of Hormuz, Trump in Manila then Xi and Putin, Iran's drones at the US radar base in Bahrain, Japan scrambling jets, five EU states planning a Rwanda return hub, the JPMorgan bug cutting off Zelle, Nvidia's earnings after the bell, the Vulcan rocket failure, Estonia shutting its Russia border crossings, the US losing measles-free status, the Houthi advance in Yemen, and the West urging Israel to open Gaza crossings
- **WHERE IT HAPPENED**: a world map with numbered pins for the 13 lead stories, beside **ALSO ON TUESDAY 17 NOVEMBER** — 24 more stories, from the House Democrats' agenda to the Broncos-Raiders line
- a footer strip with the date and the source credit

The stories are the ones first reported on 17 November 2026 (BBC, AP, AFP, Reuters, Al Jazeera, CNBC, ABC News, NPR, Spaceflight Now and others). Disputed claims stay attributed, nothing is invented beyond the reporting, and no other day's news is in the picture.

## The program

`main.py` (Python 3.13, standard library only — no Pillow, no font files, no network) draws the whole page from procedural vector shapes — masthead, hero bridge illustration, twelve pictograms, continent polygons for the map — with a hand-rolled 5x7 bitmap font. No network, no external assets, no randomness. It is fully deterministic: two runs write byte-identical files. It runs in a stock `python:3.13` image with a read-only repo directory, writing only `entry.png` into `MAKEFUN_OUTPUT_DIR`.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=6kzxz8b0&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
