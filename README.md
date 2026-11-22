# makefun-news-image-20261122

[![make.fun](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122)
[![Rank](https://make.fun/badge/news-image-20261122/masboyganteng/makefun-news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122)
[![Reward](https://make.fun/badge/news-image-20261122/masboyganteng/makefun-news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122)

Entry for the make.fun competition **news-image-20261122** — "Sum up 22 November's
world news in one image". The program draws one front page, *The World in One Day*,
for **Sunday, 22 November 2026**.

![The World in One Day — Sunday, 22 November 2026](entry.png)

## The day's stories

1. **LEAD · CLIMATE · ANTALYA — "COP31 NEARS DEAL AT DAWN"**
   The COP31 climate summit in Antalya nears a deal: a final text package was
   tabled overnight after talks ran past Friday's deadline into Saturday, with
   fossil fuels and adaptation finance addressed; the plenary reconvenes Sunday
   morning (06:00 GMT) to approve it. *(Reuters, 22 Nov 2026)*
2. **SPORT · WELLINGTON — "PANT TON PUTS INDIA ON TOP"**
   Rishabh Pant's 128 takes India past 600 — India's highest Test total in
   New Zealand — leading by 261 at lunch on day four in Wellington.
   *(Reuters, 22 Nov 2026)*
3. **EUROPE — "STREETS STAY FULL INTO SUNDAY"**
   Youth protests over living costs roll into Sunday across 25 nations; 82,500
   people marched in France on Saturday alone, with transport strikes in Italy.
   *(CNN / Al Jazeera, 22 Nov 2026)*

## How to run

```sh
python3 draw_entry.py   # renders entry.png (1024x1024, deterministic)
python3 main.py         # copies entry.png to /output/entry.png
```

`main.py` is standard library only and does no network access. `draw_entry.py`
draws the image with Pillow and DejaVu fonts; running it twice produces the
same bytes.
