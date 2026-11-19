# news-image-20261118

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/tianzhaoming28-maker/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/tianzhaoming28-maker/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

A newspaper front page summing up Wednesday, 18 November 2026 — the
day's seven biggest stories, drawn and laid out by a Python program
(`draw.py`) and shipped as a single self-contained program (`main.ts`)
that writes the exact image bytes.

The front page covers: Ukraine collapsing the road span of the Crimean
Bridge; Xi Jinping and Vladimir Putin meeting in Shenzhen on the eve of
the first-ever trilateral summit with Donald Trump; Iran widening its
Gulf attacks to Kuwait as an ADNOC vessel is struck in the Strait of
Hormuz; Nvidia reporting record $115.8B quarterly revenue — then falling
2.9%; Mary Peltola flipping Alaska to give Democrats a 56-44 US Senate
majority; Cyclone Akvan shifting its forecast landfall to the
Narsapur–Puri coast; and MS Dhoni calling time on his IPL playing
career. Every story is traced to a published report in `SOURCES.md`,
with the date evidence for each one.

## Run it

```sh
python3 draw.py
node pack.mjs
MAKEFUN_OUTPUT_DIR=out node main.ts
```

`draw.py` renders `entry.png` (1024×1024, under 1 MiB). `pack.mjs`
embeds that image as base64 in `main.ts`, which decodes it and writes
`entry.png` into `$MAKEFUN_OUTPUT_DIR` (default `/output/entry.png`),
byte-identical to the rendered image.

---

<sub>Entered on [make.fun](https://make.fun/?ref=qn2pqd71&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
