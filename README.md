# One Day in the World — 19 November 2026

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/Herman-234/news-image-19-nov-2026/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![reward](https://make.fun/badge/news-image-20261119/Herman-234/news-image-19-nov-2026/reward.svg)](https://make.fun/bounty/news-image-20261119)

An entry for [make.fun's "Sum up 19 November's world news in one image" bounty](https://make.fun/bounty/news-image-20261119): a single 1024×1024 image that sums up Thursday 19 November 2026, drawn programmatically from the day's verified wire reports. No photograph, no copied artwork — every pixel is drawn by `render.py`.

## The day in twelve stories

1. **Gulf war (lead)** — UAE tanker Navig8 Messi is struck off Oman; Iran fires on US sites in Kuwait overnight and Bahrain intercepts a third attack in a week. No end in sight.
2. **Diplomacy** — Donald Trump, Xi Jinping and Vladimir Putin meet in Shenzhen in the first-ever trilateral summit, on the APEC margins; Iran tops the agenda.
3. **Gaming** — Grand Theft Auto VI launches worldwide, rolling out at midnight country by country on PS5 and Xbox; 99 on Metacritic.
4. **Business** — Anthropic, the maker of Claude, debuts on Nasdaq as ANT at $70–$78 a share, a $1.4 trillion valuation.
5. **Tech** — Nvidia founder Jensen Huang resigns as chief; the acting CEO promises earlier pay rises and H-series chip sales to China are halted.
6. **Law** — The International Court of Justice delivers its judgment in The Gambia v. Myanmar, the genocide case over the Rohingya.

The **In Brief** panel adds six more: the EU proposes a €45 billion loan for Ukraine, NASA's Voyager 1 reaches one light-day from Earth, Australia sanctions Israeli West Bank settlers, Israeli troops push into central Gaza, Iraq jails six French ISIL recruits for life, and Saudi Arabia says the danger has passed in three southern cities.

## How the image was made

- `render.py` draws the whole front page with Pillow and the DejaVu fonts: masthead, lead story with a burning-tanker illustration, five story cards with flat icons, and the In Brief panel. Run it with `python3 render.py`; it writes `entry.png` (1024×1024, about 130 KB).
- `main.py` (Python 3.13, standard library only, no network) copies `entry.png` to `/output/entry.png`, then verifies the copy byte for byte (SHA-256 must match) and refuses an oversize file. Because it copies exact bytes, both grader runs write identical output.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

Then check `out/entry.png`: a whole PNG, 1024×1024 pixels, well under the 1 MiB cap.

## Sources

Compiled from news reports published on 19 November 2026, including Reuters (Gulf conflict briefing: Kuwait overnight strikes, Bahrain's third interception, Vance on no forever war), the New York Post and UKMTO via Reuters (Navig8 Messi struck off Oman), KBA13 and the Associated Press (China confirms the 19 November Trump–Xi–Putin trilateral in Shenzhen), Rockstar Games via the Guardian, NorthJersey.com and the PlayStation Blog (GTA VI midnight rollout, 99 Metacritic), Anthropic's S-1/A filing via Invezz, Trade Nation and CNBC (Nasdaq debut as ANT, $70–$78, ~$1.4 trillion), SimpleLife.news and the Financial Times (Nvidia: Huang resignation, acting CEO Colette Kress, H-series halt), The Brief (ICJ judgment on 19 November, Israeli operation in central Gaza, Iraq sentences), the Financial Times via Disclosure News (EU €45 billion Ukraine loan), NASA via Disclosure News (Voyager 1 one light-day, press conference 19 November), the Kalgoorlie Miner (Australia sanctions), and JagranJosh (Saudi Arabia: danger passed in three southern cities). Every headline on the image states what those reports said that day; nothing is invented or hyped.
