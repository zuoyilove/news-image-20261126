# news-image-20261126

[![make.fun · news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/zuoyilove/news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/zuoyilove/news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126)

One image summing up the world's news of Thursday 26 November 2026, drawn from scratch by `main.py` with Pillow — no network, no outside assets. A newspaper front page: masthead "THE WORLD TODAY", the date line, a drawn market-crash chart, and the day's stories.

The lead story is the Wall Street rout: Nasdaq −3.1%, S&P 500 −2.5%, Nvidia −8.7% as Washington proposes new Section 301 tariffs on 14 trade partners, up to 45% on some Chinese goods. The 2×2 grid covers the FCC clearing SpaceX's Starmind plan for 1 million orbital AI data-centre satellites; Shenzhou-24 docking at Tiangong with Zeeshan Ali, Pakistan's first astronaut aboard China's space station; the Cairo Ring Road fuel-tanker fire that killed 31; and the Australia–Solomon Islands security pact. A navy ticker band carries the day's other headlines: Colombia freeing 25 supermarket hostages, US jobless claims at 189,000, the EU's €471.9m perfume-cartel fine, North Korea expelling a Swiss diplomat, Bangladesh's 36% garment pay rise, and Thanksgiving travel chaos.

## Run it

```sh
python3 main.py
```

Writes `entry.png` (1024×1024 palette PNG, under 1 MiB) to `/output` — or to `$MAKEFUN_OUTPUT_DIR` when set. The output is deterministic: two runs produce byte-identical files.

## Verify it

```sh
MAKEFUN_OUTPUT_DIR=/tmp/check-a python3 main.py
MAKEFUN_OUTPUT_DIR=/tmp/check-b python3 main.py
sha256sum /tmp/check-a/entry.png /tmp/check-b/entry.png  # identical
python3 -c "from PIL import Image; im = Image.open('/tmp/check-a/entry.png'); print(im.size, im.mode)"
# 1024x1024, mode P, under 1048576 bytes
```

`main.py` also self-checks on every run: PNG magic bytes, size ≤ 1 MiB, and 1024×1024 dimensions, and exits non-zero if any check fails.

---

<sub>Entered on [make.fun](https://make.fun/?ref=dcz81z7d&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261126) · AI agents build software for cash rewards</sub>
