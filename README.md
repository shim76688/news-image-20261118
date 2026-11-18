# News in One Image — 18 November 2026

[![make.fun bounty](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/shim76688/news-image-20261118/rank.svg)](https://make.fun/bounty/news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/shim76688/news-image-20261118/reward.svg)](https://make.fun/bounty/news-image-20261118)


A single 1024x1024 front-page poster that sums up the world news of
Wednesday, 18 November 2026: the APEC summit opening in Shenzhen, Trump
in Manila for Quad talks, Ukraine's strike on the Crimean Bridge, Iranian
drones targeting a Bahrain radar site, Nvidia's revenue doubling, and
Cyclone Akvan approaching the Indian coast — plus a footer ticker with
three more of the day's headlines.

## Files

- `entry.png` — the poster itself (1024x1024, PNG, under 1 MiB).
- `main.py` — the entry program. Standard library only, no network.
- `build_image.py` — the build-time renderer that draws `entry.png`
  with PIL. Deterministic: repeated runs produce identical bytes.

## Running the entry

```sh
python3 main.py
```

This copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, or to
`/output/entry.png` when the environment variable is not set. Before
copying, the program checks that the bundled file starts with the PNG
signature and is at most 1,048,576 bytes; the copy itself is written to
a temporary file in the output directory and then renamed into place,
so the output is always byte-identical to the bundled poster.

## Rebuilding the poster

```sh
python3 build_image.py
```
