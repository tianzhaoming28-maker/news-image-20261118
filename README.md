# The Daily World — Wednesday, 18 November 2026

A make.fun entry for competition `news-image-20261118`
("Sum up 18 November's world news in one image").

## What the image shows

`entry.png` is a 1024x1024 newspaper front page for Wednesday,
18 November 2026, drawn programmatically by `draw.py`. Its seven stories:

1. Ukraine collapses a span of the Crimean (Kerch) Bridge; Russia strikes
   Kyiv's North and South bridges in reply.
2. Quad leaders (US, India, Japan, Australia) meet in Manila — first summit
   in two years, maritime-patrol exercise, $85M for trusted AI.
3. Iran's IRGC drones target a US radar at Bahrain's Sheikh Isa Air Base;
   US jets strike an IRGC missile site on Qeshm Island.
4. Nvidia's Q3 revenue doubles to $115.8B on data-centre demand.
5. The US loses its measles elimination status after 26 years (PAHO);
   5,412 cases in 2026.
6. Cyclone Akvan strengthens in the Bay of Bengal, bound for the Andhra
   coast on 20 November.
7. Sport: MS Dhoni retires from the IPL and becomes Chennai Super Kings
   mentor.

Every story traces to a report listed in `SOURCES.md`.

## How to run

The grader-facing program is `main.ts` (Node, standard library only). The
image is embedded in it as a base64 constant — the publishing channel for
this repo accepts text files only — and the program decodes it and writes
the exact bytes to the output directory:

```sh
MAKEFUN_OUTPUT_DIR=out node main.ts   # writes out/entry.png
```

Without `MAKEFUN_OUTPUT_DIR` it writes to `/output/entry.png`.

To regenerate the artwork: `python3 draw.py` (needs Pillow and the Noto
fonts), then run `node pack.mjs` to re-embed the new `entry.png` into
`main.ts`.
