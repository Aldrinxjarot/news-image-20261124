# The World in One Day — Tuesday, 24 November 2026

Entry for make.fun **news-image-20261124**: one 1024×1024 image that
sums up the world news of Tuesday, 24 November 2026.

## What it shows

A newspaper front page, drawn entirely by code:

- **Hero — markets:** the relief rally over Jensen Huang's shock
  return as Nvidia's chief executive fades on Tuesday: Nvidia slides
  6%, the Nasdaq falls 1.5%, and Congress prepares to question the
  boss who quit on 12 November and was brought back after President
  Trump intervened. A chart box shows Tuesday's closing moves
  (Reuters).
- **China / courts:** a U.S. federal jury convicts Huawei of
  deceiving banks about its Iran business and stealing trade
  secrets (Reuters).
- **Business:** Sanofi agrees to buy U.S. biotech Insmed for
  $41 billion in cash — the year's biggest pharma deal — announced
  in Paris on Tuesday.
- **Israel:** Eisenkot's Yashar party signs its first coalition
  pact, with Lieberman's Israel Our Home; he has until 6 December
  to form a government (Reuters).
- **Ukraine:** an overnight Russian attack on Zaporizhzhia kills
  two and wounds dozens, four of them children, the regional
  governor says on Tuesday.
- An "Also today" ticker: U.S. consumer confidence at a near
  two-year high, Israeli strikes in Gaza, Bangladesh garment
  workers' clashes, and 175 migrants missing off Senegal.

`NOTES.md` lists every story with its date/source justification,
plus the prominent stories that were checked and dropped as earlier
days' news (the ICJ's Myanmar judgment of 19 Nov, Rutte's Monday
space remarks, Monday's Grok lawsuits, and others).

## Files

- `entry.png` — the submitted image (1024×1024, drawn by `draw.py`).
- `draw.py` — the Pillow program that draws the front page
  (build-time only; all text and the chart are drawn by the
  program).
- `main.py` — the entrypoint: standard-library only, copies
  `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`) and checks
  the delivered size, so both graded runs produce byte-identical
  output.

## Run

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To redraw the image from source: `python3 draw.py` (requires Pillow).
