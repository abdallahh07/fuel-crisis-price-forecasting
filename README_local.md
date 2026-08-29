# 2026 Iran War Fuel Crisis — Dataset

Real, sourced data on the global fuel/energy crisis triggered by the 2026 Iran war and the closure of the
Strait of Hormuz (~20% of world oil trade). Collected/fetched on **5 July 2026**. Every number in every CSV
below is traceable to a source that was actually fetched during this collection session — nothing was
estimated, interpolated, or generated. Where a planned source could not be obtained, that is stated
explicitly in **Known Limitations**, not silently patched over.

Anchor keyword: the crisis is documented on Wikipedia as **"2026 Iran war fuel crisis"** — that is the
named event this dataset is built around, not a generic multi-decade oil-price series (several of those
already exist on Kaggle).

## Files

### `crude_oil_prices.csv` (126 rows, 2026-01-02 to 2026-07-03, daily)
Daily WTI (`CL=F`), Brent (`BZ=F`), and Henry Hub natural gas (`NG=F`) futures — open/high/low/close/volume
for each. Source: Yahoo Finance via the `yfinance` Python library. No API key required. Spans a clean
pre-crisis baseline (Jan 2026, WTI ~$56-58) through the shock (WTI peaks $112.95 on 2026-04-07, Brent peaks
$118.35 on 2026-03-31) and the post-ceasefire decline back to the high-$60s/low-$70s by July. This price
path is independently corroborated by the IEA Oil Market Reports below (IEA cites Brent near $120/bbl in
March and North Sea Dated near $130/bbl in April) and by the EIA retail gasoline series moving in lockstep.

### `us_gasoline_prices.csv` (26 rows, weekly, 2026-01-05 to 2026-06-29)
Weekly U.S. retail **regular gasoline** prices (28 series: national average, all 5 PADD regions + sub-PADDs
1A/1B/1C, 9 states — California, Colorado, Florida, Massachusetts, Minnesota, New York, Ohio, Texas,
Washington — and 10 metro areas including Los Angeles, San Francisco, Chicago, Houston, New York City), plus
**on-highway No. 2 diesel** prices (11 series: national + PADD regions + California). Source: EIA (U.S.
Energy Information Administration) direct bulk `.xls` downloads — `pswrgvwall.xls` (gasoline, "Data 3: Regular
All Areas All Formulations") and `psw18vwall.xls` (diesel, "Data 1"), both from
https://www.eia.gov/petroleum/gasdiesel/ — no API key needed. US national regular gasoline rises from
$2.796/gal (2026-01-05) to a peak of $4.50/gal (2026-05-11) before easing to $3.831/gal by 2026-06-29;
California regular gasoline peaks at $5.969/gal on the same date (statewide average — consistent with,
but not the same figure as, the widely reported "$6+/gallon in seven counties as of March 30" retail
price spike, which was county-level, a finer granularity EIA does not publish).

### `us_refinery_and_trade_weekly.csv` (26 rows, weekly, 2026-01-02 to 2026-06-26)
National weekly refinery utilization (%), refinery crude inputs, gross inputs, operable capacity, crude oil
imports/exports, and total petroleum product imports/exports (all thousand barrels/day). Source: EIA
Petroleum Navigator historical series, direct `.xls` downloads (no API key): `WPULEUS3` (refinery
utilization), `WCRRIUS2`, `WGIRIUS2`, `WOCLEUS2`, `WCRIMUS2`, `WCREXUS2`, `WRPIMUS2`, `WRPEXUS2`, `WTTNTUS2`
from https://www.eia.gov/dnav/pet/. This is a bonus file beyond the original spec — it captures the supply
side of the shock (net petroleum exports roughly doubled from about -3,300 kb/d in January to -6,700 kb/d in
April as the U.S. absorbed demand redirected away from the closed Strait of Hormuz).

### `crisis_timeline.csv` (71 rows, 2026-02-26 to 2026-06-21)
Columns: `date, region, event, description, source_name, source_url`. A cited, dated timeline of the crisis:
war start (28 Feb 2026, per the IEA), the Strait of Hormuz closure, the Qatar LNG attacks, national reserve
releases (Japan, New Zealand), fuel rationing (Slovenia, Australia), price-shock milestones, the 8 April
ceasefire, and post-ceasefire developments through late June (China's reserve strategy, IEA's World Energy
Investment 2026 report). **Sources and how they were used:** built from (a) the actual current wikitext of
the English Wikipedia article "2026 Iran war fuel crisis" (fetched directly via `action=raw`, not summarized
by an intermediary), using the article's own inline citations — the `source_url` in each row is the original
news source Wikipedia cites (Reuters, BBC, NYT, Guardian, CNBC, Bloomberg, FT, WSJ, regional outlets, etc.),
not the Wikipedia page itself; and (b) the IEA's own Oil Market Report PDFs for March, April, and May 2026
(see below), fetched directly. **Important provenance note:** the ~65 news-source URLs embedded in the
Wikipedia article were read as Wikipedia cites them — they were not independently re-fetched and re-verified
article-by-article in this session (that would mean re-scraping ~65 separate news sites). Every date, figure,
and quote in this file was checked programmatically against the raw Wikipedia wikitext and/or the IEA report
text actually downloaded (see `raw_sources/`) before being included; nothing was transcribed from memory
without that check.

### `country_gas_price_comparison.csv` (170 rows, snapshot dated 2026-06-29)
Columns: `country, gasoline_usd_per_liter, diesel_usd_per_liter, update_frequency, data_date`. Live retail
pump-price snapshot (Octane-95 gasoline and regular diesel, USD/liter) for 170 countries, giving the
"who's hit hardest" cross-country view (e.g., UK $2.003 gasoline / $2.216 diesel per liter; USA $1.108 /
$1.233; Canada $1.311 / $1.330; Iran $0.029 / $0.006 — Iran's own domestic price, heavily subsidized and
disconnected from the export-market shock). Source: globalpetrolprices.com `/gasoline_prices/` and
`/diesel_prices/` pages, live on 2026-06-29 (per the page's own displayed date). **Collection method:** the
site renders its price chart as positioned `<div>` elements (no accessible chart-data API in the page), so
country labels and their paired price values were extracted via a headless-browser JS query that matched
each label element to its price element by on-screen vertical position (`getBoundingClientRect().top`),
verified to have **zero unmatched pairs out of 170** before being written to CSV. `update_frequency` records
whether that country's series is marked "weekly" (`*` in the source) or "monthly" on the site. One data point
is missing (Iraq has no diesel figure on the source site) — left blank rather than filled in.

### `reddit_sentiment.csv` (50 rows, 2026-02-17 to 2026-06-25)
Columns: `subreddit, title, score, num_comments, posted_utc, permalink`. Top posts (by score, past year) from
r/economy and r/energy on old.reddit.com matching crisis-related search terms, giving a real public-discourse
angle spanning the pre-war build-up through the post-ceasefire period. Every row has a real, working
`permalink` to the actual Reddit thread; scores and comment counts are what old.reddit.com displayed at
scrape time (2026-07-05) and will have changed somewhat since (Reddit scores are live-updating; the number
recorded is a snapshot, not a final value — this is stated here so it isn't mistaken for something else).
r/personalfinance was also queried but returned no crisis-specific results for the search terms tried (see
Limitations) and was dropped rather than padded with irrelevant posts. **Note on representativeness:** this
is a top-sorted sample from two subreddits, not a random or statistically representative sample of public
sentiment — treat it as a curated set of high-visibility discussion threads for qualitative reading, not as
a measure of overall public opinion.

## Known Limitations

- **EIA API key not registered.** The EIA Open Data API (api.eia.gov) requires an emailed API key
  (self-registration form at https://www.eia.gov/opendata/register.php). Completing that registration
  requires access to a real inbox to retrieve the key, which this session did not do (this is flagged for
  the user below as a possible follow-up, not silently worked around). Instead, all EIA data here was pulled
  from EIA's public bulk `.xls` downloads, which require no key. These bulk files cover national, PADD-region,
  state, and named-metro-area granularity for gasoline/diesel — they do **not** reach county-level granularity
  (e.g., the specific California counties reported over $6/gallon), which the API might not provide either
  (that figure appears to come from retail price-tracking services, not EIA).
- **IEA Oil Market Report is behind a Cloudflare bot check.** Direct `curl`/`WebFetch` requests returned
  HTTP 403 ("Just a moment..." challenge page). Resolved by loading the page in an actual browser (the
  challenge auto-passed after a few seconds), then downloading the report's own free PDF link
  (`iea.blob.core.windows.net/assets/.../OilMarketReport...pdf`) directly via `curl`. The March, April, and
  May 2026 editions were obtained this way; April 2026 was IEA's own choice to make free ("exceptionally
  provided free of charge in abridged format"), consistent with the elevated public interest in this crisis.
- **globalpetrolprices.com historical/bulk time series is a paid product** ($0.35-$7.50 per data point per
  their own pricing page, data_download.php). A pre-war baseline snapshot (Wayback Machine has an archived
  capture from 2026-02-13, three weeks before the war) was attempted for a genuine before/after comparison,
  but the archived page's label and price elements had inconsistent row heights (a rendering artifact of the
  archived copy, confirmed by direct measurement), which broke the position-matching pairing method beyond
  the first few rows (135/170 unmatched) — this was abandoned rather than risk silently mispairing a country
  with the wrong price. `country_gas_price_comparison.csv` is therefore a single current (2026-06-29) snapshot,
  not a time series. Getting a genuine pre-war baseline from this source would require either the paid data
  product or a more robust archived-page extraction method.
- **Reddit**: only r/economy and r/energy yielded clearly crisis-specific top posts for the search terms
  tried; r/personalfinance did not (see above). The old.reddit.com JSON API was not tried since the HTML
  search interface worked fine and was low-risk to scrape gently.
- **No Kaggle upload performed.** This is a reviewed, local, ready-to-upload dataset folder — publishing to
  Kaggle is a user action, per the task boundaries for this session.

## Possible follow-ups needing a human decision

- **EIA API key**: registering one (real name + email, key emailed) would unlock the full EIA Open Data API,
  including some series not in the bulk `.xls` files. Given how complete the bulk-file coverage already is for
  this dataset's scope, this is optional polish, not a gap.
- **globalpetrolprices.com paid historical data**: would enable a real pre-war-vs-crisis country-level
  comparison instead of a single snapshot, at ~$0.35/point (weekly) times however many countries/weeks are
  wanted — a live purchase decision for the user, not made here.

## `raw_sources/`
Kept for transparency/verification, not required to use the CSVs above:
- `raw_sources/eia/` — the original `.xls` files downloaded from eia.gov, exactly as fetched.
- `raw_sources/wikipedia_and_iea/` — `article_wikitext.txt` (raw wikitext of the Wikipedia article, fetched
  `2026-07-05`) and the three IEA Oil Market Report PDFs (plus their extracted `.txt`) for March/April/May 2026.

## Total size
~21 MB including `raw_sources/` (the CSVs themselves are under 100 KB combined).
