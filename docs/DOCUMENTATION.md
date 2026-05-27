# Documentation — agent-reliability-eval-data

An itemized reference to the **test units** in this dataset. For the project
overview see [../README.md](../README.md); for the label schema see
[RUBRIC.md](RUBRIC.md); for per-asset language/model provenance see
[ASSETS.md](ASSETS.md); for ground-truth provenance see
[METHODOLOGY.md](METHODOLOGY.md); for the fixture QA pass see
[REVIEW-REPORT.md](REVIEW-REPORT.md).

## Repository map

```
data/
  units.jsonl          canonical benchmark (44 synthetic units, each QA-passed)
  units-raw.jsonl      full transparency set: all 68 tracks incl. superseded + handwritten
  seeds.jsonl          the 26 generation seeds the synthetic units derive from
  assets.csv           flat per-asset manifest (id, language, generator model, bucket, …)
  fixtures/*.html      frozen HTML for every synthetic unit (referenced by html_path)
  real-outlets/        9 real articles as URL + labels (HTML not redistributed)
docs/                  this file + asset manifest + rubric + methodology + the QA review
```

## Test units

The benchmark ships **44 synthetic test units** in `data/units.jsonl`. Each is a
fictional news article with committed ground-truth labels across the six
credibility dimensions (see [RUBRIC.md](RUBRIC.md)) plus an `overall_band`.
Labels are **seed-committed** — fixed before generation — and every unit has been
QA-verified to earn them (15 were rewritten until they passed; see
[REVIEW-REPORT.md](REVIEW-REPORT.md)).

`data/units-raw.jsonl` is the full transparency set of **68 tracks**: it adds the
superseded originals of the rewritten units, parallel chat/pro variants, and 9
handwritten parity fixtures. Use it for ablation; use `units.jsonl` for scoring.

### Canonical-44 breakdown

By bucket:

| Bucket | count |
|---|---|
| low-credibility | 10 |
| mainstream-israeli-news | 8 |
| credible-but-opinionated | 7 |
| tabloid-clickbait | 7 |
| gold-credible | 6 |
| satire | 6 |

By language: **en 23 · he 21.** By generation track: **pro 26 · chat 18.** By
review status: **pass 29 · rewritten 15.** (Full per-asset language + model table
in [ASSETS.md](ASSETS.md).)

### Bucket glossary

- **gold-credible** — Straight, well-sourced reporting from a reputable-style outlet. Expected to score high.
- **credible-but-opinionated** — Factual but clearly opinion/editorial framing — credible source, visible stance.
- **mainstream-israeli-news** — Mainstream Israeli-news-style reporting (Hebrew-heavy), ordinary credibility.
- **tabloid-clickbait** — Sensational/clickbait framing over thin substance.
- **low-credibility** — Unreliable: unsourced claims, anonymous authorship, conspiratorial or contradicts-consensus framing. Expected to score low.
- **satire** — Satirical/absurdist news parody. The rubric has a dedicated `SATIRE` enum on both `source-format` and `consensus-format`. Satire is a *content* property, so these synthetic units are labeled `consensus-format=SATIRE` but `source-format=NEUTRAL` — the fixtures publish on `example.com`, an unknown publisher; only a recognised satire *domain* (e.g. The Onion) would earn `source-format=SATIRE`.

### Unit record schema

```json
{
  "id": "string",                 // unique unit id; "-r" suffix = QA-rewritten variant
  "lang": "en | he",
  "bucket": "one of the buckets above",
  "expected": {                   // committed ground truth (see RUBRIC.md)
    "source-format": "...", "author": "...", "consensus-format": "...",
    "headline": "...", "bias": "...", "style": "...",
    "overall_band": "high | mid | low"
  },
  "track": "chat | pro",          // generator track (gpt-5.4 vs gpt-5.4-pro)
  "review_status": "pass | rewritten",
  "original_id": "string?",       // present when review_status == rewritten
  "generator_model": "string",
  "html_path": "data/fixtures/<id>.html"
}
```

### All 44 canonical units

| id | bucket | lang | track | review_status | overall_band | html_path |
|---|---|---|---|---|---|---|
| `gen-unreliable-en-02-r` | low-credibility | en | chat | rewritten | low | `data/fixtures/gen-unreliable-en-02-r.html` |
| `gen-unreliable-en-03-r` | low-credibility | en | chat | rewritten | low | `data/fixtures/gen-unreliable-en-03-r.html` |
| `gen-unreliable-he-02` | low-credibility | he | chat | pass | low | `data/fixtures/gen-unreliable-he-02.html` |
| `gen-unreliable-he-03-r` | low-credibility | he | chat | rewritten | low | `data/fixtures/gen-unreliable-he-03-r.html` |
| `gen-n12like-en-01` | mainstream-israeli-news | en | chat | pass | high | `data/fixtures/gen-n12like-en-01.html` |
| `gen-n12like-en-02` | mainstream-israeli-news | en | chat | pass | high | `data/fixtures/gen-n12like-en-02.html` |
| `gen-n12like-he-01` | mainstream-israeli-news | he | chat | pass | high | `data/fixtures/gen-n12like-he-01.html` |
| `gen-n12like-he-02` | mainstream-israeli-news | he | chat | pass | high | `data/fixtures/gen-n12like-he-02.html` |
| `gen-opinion-en-01` | credible-but-opinionated | en | chat | pass | mid | `data/fixtures/gen-opinion-en-01.html` |
| `gen-opinion-en-02-r` | credible-but-opinionated | en | chat | rewritten | mid | `data/fixtures/gen-opinion-en-02-r.html` |
| `gen-opinion-he-02` | credible-but-opinionated | he | chat | pass | mid | `data/fixtures/gen-opinion-he-02.html` |
| `gen-tabloid-en-01` | tabloid-clickbait | en | chat | pass | mid | `data/fixtures/gen-tabloid-en-01.html` |
| `gen-tabloid-en-02` | tabloid-clickbait | en | chat | pass | mid | `data/fixtures/gen-tabloid-en-02.html` |
| `gen-tabloid-he-02` | tabloid-clickbait | he | chat | pass | mid | `data/fixtures/gen-tabloid-he-02.html` |
| `gen-gold-en-02` | gold-credible | en | chat | pass | high | `data/fixtures/gen-gold-en-02.html` |
| `gen-gold-he-02` | gold-credible | he | chat | pass | high | `data/fixtures/gen-gold-he-02.html` |
| `gen-satire-en-02-r` | satire | en | chat | rewritten | low | `data/fixtures/gen-satire-en-02-r.html` |
| `gen-satire-he-01-r` | satire | he | chat | rewritten | low | `data/fixtures/gen-satire-he-01-r.html` |
| `gen-unreliable-en-01-pro` | low-credibility | en | pro | pass | low | `data/fixtures/gen-unreliable-en-01-pro.html` |
| `gen-unreliable-en-02-pro-r` | low-credibility | en | pro | rewritten | low | `data/fixtures/gen-unreliable-en-02-pro-r.html` |
| `gen-unreliable-en-03-pro-r` | low-credibility | en | pro | rewritten | low | `data/fixtures/gen-unreliable-en-03-pro-r.html` |
| `gen-unreliable-he-03-pro-r` | low-credibility | he | pro | rewritten | low | `data/fixtures/gen-unreliable-he-03-pro-r.html` |
| `gen-n12like-en-01-pro` | mainstream-israeli-news | en | pro | pass | high | `data/fixtures/gen-n12like-en-01-pro.html` |
| `gen-n12like-en-02-pro` | mainstream-israeli-news | en | pro | pass | high | `data/fixtures/gen-n12like-en-02-pro.html` |
| `gen-n12like-he-01-pro` | mainstream-israeli-news | he | pro | pass | high | `data/fixtures/gen-n12like-he-01-pro.html` |
| `gen-n12like-he-02-pro` | mainstream-israeli-news | he | pro | pass | high | `data/fixtures/gen-n12like-he-02-pro.html` |
| `gen-opinion-en-01-pro` | credible-but-opinionated | en | pro | pass | mid | `data/fixtures/gen-opinion-en-01-pro.html` |
| `gen-opinion-en-02-pro-r` | credible-but-opinionated | en | pro | rewritten | mid | `data/fixtures/gen-opinion-en-02-pro-r.html` |
| `gen-opinion-he-01-pro` | credible-but-opinionated | he | pro | pass | mid | `data/fixtures/gen-opinion-he-01-pro.html` |
| `gen-opinion-he-02-pro` | credible-but-opinionated | he | pro | pass | mid | `data/fixtures/gen-opinion-he-02-pro.html` |
| `gen-tabloid-en-01-pro` | tabloid-clickbait | en | pro | pass | mid | `data/fixtures/gen-tabloid-en-01-pro.html` |
| `gen-tabloid-en-02-pro` | tabloid-clickbait | en | pro | pass | mid | `data/fixtures/gen-tabloid-en-02-pro.html` |
| `gen-tabloid-he-02-pro` | tabloid-clickbait | he | pro | pass | mid | `data/fixtures/gen-tabloid-he-02-pro.html` |
| `gen-gold-en-01-pro` | gold-credible | en | pro | pass | high | `data/fixtures/gen-gold-en-01-pro.html` |
| `gen-gold-en-02-pro` | gold-credible | en | pro | pass | high | `data/fixtures/gen-gold-en-02-pro.html` |
| `gen-gold-he-01-pro` | gold-credible | he | pro | pass | high | `data/fixtures/gen-gold-he-01-pro.html` |
| `gen-gold-he-02-pro` | gold-credible | he | pro | pass | high | `data/fixtures/gen-gold-he-02-pro.html` |
| `gen-satire-en-01-pro-r` | satire | en | pro | rewritten | low | `data/fixtures/gen-satire-en-01-pro-r.html` |
| `gen-satire-en-02-pro-r` | satire | en | pro | rewritten | low | `data/fixtures/gen-satire-en-02-pro-r.html` |
| `gen-satire-he-01-pro-r` | satire | he | pro | rewritten | low | `data/fixtures/gen-satire-he-01-pro-r.html` |
| `gen-satire-he-02-pro-r` | satire | he | pro | rewritten | low | `data/fixtures/gen-satire-he-02-pro-r.html` |
| `gen-unreliable-he-01-pro-r` | low-credibility | he | pro | rewritten | low | `data/fixtures/gen-unreliable-he-01-pro-r.html` |
| `gen-unreliable-he-02-pro` | low-credibility | he | pro | pass | low | `data/fixtures/gen-unreliable-he-02-pro.html` |
| `gen-tabloid-he-01-pro` | tabloid-clickbait | he | pro | pass | mid | `data/fixtures/gen-tabloid-he-01-pro.html` |

### Real-outlet units (HTML not redistributed)

Real news HTML is copyrighted, so `data/real-outlets/urls.jsonl` ships the URLs +
labels only (9 articles: BBC, Haaretz, The Onion, Ynet, Mako). See
[ASSETS.md](ASSETS.md#real-outlet-references-html-not-redistributed) for the full
list with languages.

### Seeds

`data/seeds.jsonl` holds the 26 seeds (bucket, language, topic, required
attributes, committed expected labels) the synthetic units were generated from.
