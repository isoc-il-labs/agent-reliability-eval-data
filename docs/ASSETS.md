# Asset manifest — language & model provenance

Every generated asset in this repository, with its **language** and the **model that produced it**. This is the authoritative provenance index; `data/assets.csv` is the same data in flat form for scripting.

All synthetic article text, bylines, outlets, and people are **entirely fictional**. Articles publish on the placeholder domain `example.com`.

## Models used

| Model id | API endpoint | Fixtures generated |
|---|---|---|
| `gpt-5.4` | OpenAI chat-completions batch | 28 — all 24 **chat**-track fixtures, plus 4 **pro**-track Hebrew fixtures (fallback, see note) |
| `gpt-5.4-pro` | OpenAI responses batch | 31 — **pro**-track fixtures |
| `handwritten` | — (no model) | 9 — hand-authored seed/parity fixtures |

> **`track` vs. `generator_model`.** `track` is the *intended* generation track; `generator_model` is the model that *actually* produced the fixture. They diverge on 4 `pro`-track Hebrew fixtures (`gen-unreliable-he-01-pro`, `gen-unreliable-he-01-pro-r`, `gen-unreliable-he-02-pro`, `gen-tabloid-he-01-pro`): the pro generator tried `gpt-5.4-pro` first and fell back to `gpt-5.4` when it was unavailable. The per-asset table below records the real model for each.

> Quality-assurance of the labels used a *different* model family from the generators (independent re-labeling + holistic review by GPT-5.5 / GPT-5.5-pro, and earlier Gemini cross-checks). See [`docs/METHODOLOGY.md`](METHODOLOGY.md) and [`docs/REVIEW-REPORT.md`](REVIEW-REPORT.md).

## Synthetic fixtures — totals

**68 generated fixtures** total (`data/units-raw.jsonl`); **44** are promoted to the canonical benchmark (`data/units.jsonl`).

### By language (all 68 fixtures)

| Language | Code | Fixtures | Canonical-44 |
|---|---|---|---|
| English | en | 37 | 23 |
| Hebrew | he | 31 | 21 |

### By generator model (all 68 fixtures)

| Model | Fixtures | Canonical-44 |
|---|---|---|
| gpt-5.4 | 28 | 21 |
| gpt-5.4-pro | 31 | 23 |
| handwritten | 9 | 0 |

### Language × model crosstab (all 68 fixtures)

| Language | Model | Fixtures |
|---|---|---|
| English | gpt-5.4 | 14 |
| English | gpt-5.4-pro | 18 |
| English | handwritten | 5 |
| Hebrew | gpt-5.4 | 14 |
| Hebrew | gpt-5.4-pro | 13 |
| Hebrew | handwritten | 4 |

## Per-asset table (all 68 fixtures)

`★` = part of the canonical 44-unit benchmark. `-r` suffix = QA-rewritten variant of an earlier draft.

| Asset | Lang | Generator model | Bucket | Track | Review status | Canonical |
|---|---|---|---|---|---|---|
| `gen-opinion-en-01.html` | en | `gpt-5.4` | credible-but-opinionated | chat | pass | ★ |
| `gen-opinion-en-01-pro.html` | en | `gpt-5.4-pro` | credible-but-opinionated | pro | pass | ★ |
| `gen-opinion-en-02.html` | en | `gpt-5.4` | credible-but-opinionated | chat | superseded |  |
| `gen-opinion-en-02-pro.html` | en | `gpt-5.4-pro` | credible-but-opinionated | pro | superseded |  |
| `gen-opinion-en-02-pro-r.html` | en | `gpt-5.4-pro` | credible-but-opinionated | pro | rewritten | ★ |
| `gen-opinion-en-02-r.html` | en | `gpt-5.4` | credible-but-opinionated | chat | rewritten | ★ |
| `conspiracy-en.html` | en | `handwritten` | fact-checked-false | handwritten | handwritten |  |
| `gen-gold-en-01-pro.html` | en | `gpt-5.4-pro` | gold-credible | pro | pass | ★ |
| `gen-gold-en-02.html` | en | `gpt-5.4` | gold-credible | chat | pass | ★ |
| `gen-gold-en-02-pro.html` | en | `gpt-5.4-pro` | gold-credible | pro | pass | ★ |
| `gold-en.html` | en | `handwritten` | gold-credible | handwritten | handwritten |  |
| `synthetic-en-001.html` | en | `handwritten` | gold-credible | handwritten | handwritten |  |
| `gen-unreliable-en-01-pro.html` | en | `gpt-5.4-pro` | low-credibility | pro | pass | ★ |
| `gen-unreliable-en-02.html` | en | `gpt-5.4` | low-credibility | chat | superseded |  |
| `gen-unreliable-en-02-pro.html` | en | `gpt-5.4-pro` | low-credibility | pro | superseded |  |
| `gen-unreliable-en-02-pro-r.html` | en | `gpt-5.4-pro` | low-credibility | pro | rewritten | ★ |
| `gen-unreliable-en-02-r.html` | en | `gpt-5.4` | low-credibility | chat | rewritten | ★ |
| `gen-unreliable-en-03.html` | en | `gpt-5.4` | low-credibility | chat | superseded |  |
| `gen-unreliable-en-03-pro.html` | en | `gpt-5.4-pro` | low-credibility | pro | superseded |  |
| `gen-unreliable-en-03-pro-r.html` | en | `gpt-5.4-pro` | low-credibility | pro | rewritten | ★ |
| `gen-unreliable-en-03-r.html` | en | `gpt-5.4` | low-credibility | chat | rewritten | ★ |
| `gen-n12like-en-01.html` | en | `gpt-5.4` | mainstream-israeli-news | chat | pass | ★ |
| `gen-n12like-en-01-pro.html` | en | `gpt-5.4-pro` | mainstream-israeli-news | pro | pass | ★ |
| `gen-n12like-en-02.html` | en | `gpt-5.4` | mainstream-israeli-news | chat | pass | ★ |
| `gen-n12like-en-02-pro.html` | en | `gpt-5.4-pro` | mainstream-israeli-news | pro | pass | ★ |
| `gen-satire-en-01-pro.html` | en | `gpt-5.4-pro` | satire | pro | superseded |  |
| `gen-satire-en-01-pro-r.html` | en | `gpt-5.4-pro` | satire | pro | rewritten | ★ |
| `gen-satire-en-02.html` | en | `gpt-5.4` | satire | chat | superseded |  |
| `gen-satire-en-02-pro.html` | en | `gpt-5.4-pro` | satire | pro | superseded |  |
| `gen-satire-en-02-pro-r.html` | en | `gpt-5.4-pro` | satire | pro | rewritten | ★ |
| `gen-satire-en-02-r.html` | en | `gpt-5.4` | satire | chat | rewritten | ★ |
| `satire-en.html` | en | `handwritten` | satire | handwritten | handwritten |  |
| `clickbait-en.html` | en | `handwritten` | tabloid-clickbait | handwritten | handwritten |  |
| `gen-tabloid-en-01.html` | en | `gpt-5.4` | tabloid-clickbait | chat | pass | ★ |
| `gen-tabloid-en-01-pro.html` | en | `gpt-5.4-pro` | tabloid-clickbait | pro | pass | ★ |
| `gen-tabloid-en-02.html` | en | `gpt-5.4` | tabloid-clickbait | chat | pass | ★ |
| `gen-tabloid-en-02-pro.html` | en | `gpt-5.4-pro` | tabloid-clickbait | pro | pass | ★ |
| `gen-opinion-he-01-pro.html` | he | `gpt-5.4-pro` | credible-but-opinionated | pro | pass | ★ |
| `gen-opinion-he-02.html` | he | `gpt-5.4` | credible-but-opinionated | chat | pass | ★ |
| `gen-opinion-he-02-pro.html` | he | `gpt-5.4-pro` | credible-but-opinionated | pro | pass | ★ |
| `conspiracy-he.html` | he | `handwritten` | fact-checked-false | handwritten | handwritten |  |
| `gen-gold-he-01-pro.html` | he | `gpt-5.4-pro` | gold-credible | pro | pass | ★ |
| `gen-gold-he-02.html` | he | `gpt-5.4` | gold-credible | chat | pass | ★ |
| `gen-gold-he-02-pro.html` | he | `gpt-5.4-pro` | gold-credible | pro | pass | ★ |
| `gold-he.html` | he | `handwritten` | gold-credible | handwritten | handwritten |  |
| `gen-unreliable-he-01-pro.html` | he | `gpt-5.4` | low-credibility | pro | superseded |  |
| `gen-unreliable-he-01-pro-r.html` | he | `gpt-5.4` | low-credibility | pro | rewritten | ★ |
| `gen-unreliable-he-02.html` | he | `gpt-5.4` | low-credibility | chat | pass | ★ |
| `gen-unreliable-he-02-pro.html` | he | `gpt-5.4` | low-credibility | pro | pass | ★ |
| `gen-unreliable-he-03.html` | he | `gpt-5.4` | low-credibility | chat | superseded |  |
| `gen-unreliable-he-03-pro.html` | he | `gpt-5.4-pro` | low-credibility | pro | superseded |  |
| `gen-unreliable-he-03-pro-r.html` | he | `gpt-5.4-pro` | low-credibility | pro | rewritten | ★ |
| `gen-unreliable-he-03-r.html` | he | `gpt-5.4` | low-credibility | chat | rewritten | ★ |
| `gen-n12like-he-01.html` | he | `gpt-5.4` | mainstream-israeli-news | chat | pass | ★ |
| `gen-n12like-he-01-pro.html` | he | `gpt-5.4-pro` | mainstream-israeli-news | pro | pass | ★ |
| `gen-n12like-he-02.html` | he | `gpt-5.4` | mainstream-israeli-news | chat | pass | ★ |
| `gen-n12like-he-02-pro.html` | he | `gpt-5.4-pro` | mainstream-israeli-news | pro | pass | ★ |
| `gen-satire-he-01.html` | he | `gpt-5.4` | satire | chat | superseded |  |
| `gen-satire-he-01-pro.html` | he | `gpt-5.4-pro` | satire | pro | superseded |  |
| `gen-satire-he-01-pro-r.html` | he | `gpt-5.4-pro` | satire | pro | rewritten | ★ |
| `gen-satire-he-01-r.html` | he | `gpt-5.4` | satire | chat | rewritten | ★ |
| `gen-satire-he-02-pro.html` | he | `gpt-5.4-pro` | satire | pro | superseded |  |
| `gen-satire-he-02-pro-r.html` | he | `gpt-5.4-pro` | satire | pro | rewritten | ★ |
| `satire-he.html` | he | `handwritten` | satire | handwritten | handwritten |  |
| `clickbait-he.html` | he | `handwritten` | tabloid-clickbait | handwritten | handwritten |  |
| `gen-tabloid-he-01-pro.html` | he | `gpt-5.4` | tabloid-clickbait | pro | pass | ★ |
| `gen-tabloid-he-02.html` | he | `gpt-5.4` | tabloid-clickbait | chat | pass | ★ |
| `gen-tabloid-he-02-pro.html` | he | `gpt-5.4-pro` | tabloid-clickbait | pro | pass | ★ |

## Real-outlet references (HTML not redistributed)

Real news is copyrighted, so only **URLs + labels** ship (`data/real-outlets/urls.jsonl`). No model generated these — they are real published articles. Language is the article language.

| id | Language | Outlet | URL |
|---|---|---|---|
| `bbc-louisiana-shooting` | English | BBC | https://www.bbc.com/news/articles/c0q9v1p2dd2o |
| `bbc-chernobyl-wedding` | English | BBC | https://www.bbc.com/news/articles/c0q92lx8q75o |
| `haaretz-memorial-day` | English | Haaretz | https://www.haaretz.com/israel-news/israel-security/2026-04-20/ty-article/.premium/memorial-day-2026-174-idf-soldiers-79-israeli-civilians-killed-in-past-year/0000019d-a74e-d4a9-adff-b7dffd9a0000 |
| `haaretz-tel-aviv-buildings` | English | Haaretz | https://www.haaretz.com/israel-news/2026-04-16/ty-article-magazine/.premium/hundreds-of-tel-aviv-houses-on-brink-of-collapse-israels-homes-are-crumbling/0000019d-8fc9-d8e8-a1dd-ffe921eb0000 |
| `onion-mcconnell` | English | The Onion | https://theonion.com/mitch-mcconnell-wont-seek-reelection-in-2026/ |
| `ynet-budget-2026` | Hebrew | Ynet | https://www.ynet.co.il/news/article/b1z9qadobe |
| `ynet-year-2026` | Hebrew | Ynet | https://www.ynet.co.il/news/article/rywx002dvbx |
| `mako-rihanna` | Hebrew | Mako | https://www.mako.co.il/entertainment-celebs/world-2026/Article-fa6cb84267f9d91027.htm |
| `mako-adi-etzmi` | Hebrew | Mako | https://www.mako.co.il/entertainment-celebs/local-2026/Article-82c635e0b409d91027.htm |
