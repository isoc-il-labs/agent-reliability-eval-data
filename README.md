# agent-reliability-eval-data

The **dataset** behind `agent-reliability-eval` — a benchmark for measuring how
accurately and reliably **credibility-scoring agents** rate the trustworthiness
of news articles. This repository ships the **test units** and their **generated
assets** only: QA'd synthetic news articles with committed ground-truth labels,
the seeds they came from, and the documentation that describes them. The
evaluation harness and the reference agent's prompts are **not** included here.

All synthetic article text, bylines, outlets, and people are **entirely
fictional**; the articles publish on the placeholder domain `example.com`.

## What's in here

```
data/
  units.jsonl            # canonical benchmark: 44 synthetic units, each QA-passed
  units-raw.jsonl        # all 68 generated tracks incl. superseded + handwritten (for ablation)
  seeds.jsonl            # the 26 seeds the synthetic units were generated from
  assets.csv             # flat per-asset manifest: language + generator model for every fixture
  fixtures/*.html        # frozen HTML for every synthetic unit (referenced by html_path)
  real-outlets/
    urls.jsonl           # real news articles as URL + labels (HTML NOT redistributed)
docs/
  ASSETS.md              # authoritative language + model provenance for every asset
  RUBRIC.md              # the 6 credibility dimensions + rating enums (the label schema)
  DOCUMENTATION.md       # itemized catalog of the test units
  METHODOLOGY.md         # ground-truth provenance + known hazards
  REVIEW-REPORT.md       # the GPT-5.5 fixture QA pass
```

## The test units

Each line of `data/units.jsonl`:

```json
{
  "id": "gen-unreliable-en-03-r",
  "lang": "en",
  "bucket": "low-credibility",
  "expected": {
    "source-format": "UNRELIABLE", "author": "ANONYMOUS",
    "consensus-format": "CONTRADICTS_CONSENSUS", "headline": "DECEPTIVE",
    "bias": "STRONG_BIAS", "style": "SENSATIONALIST", "overall_band": "low"
  },
  "track": "chat", "review_status": "rewritten", "original_id": "gen-unreliable-en-03",
  "generator_model": "gpt-5.4", "html_path": "data/fixtures/gen-unreliable-en-03-r.html"
}
```

- **`bucket`** ∈ `gold-credible`, `credible-but-opinionated`, `mainstream-israeli-news`, `tabloid-clickbait`, `low-credibility`, `satire`.
- **`expected`** holds the committed ground-truth rating per dimension (full schema in [`docs/RUBRIC.md`](docs/RUBRIC.md)) plus an `overall_band` (`high` ≥ 70 / `mid` 40–69 / `low` < 40).
- **`expected` labels are seed-committed** — fixed in the seed *before* the article was generated — which is the strongest form of ground truth: the article was written to exhibit exactly those properties.
- **`generator_model`** records which model produced the fixture; **`lang`** records its language. The complete provenance index is [`docs/ASSETS.md`](docs/ASSETS.md) (and `data/assets.csv`).

## Languages & models at a glance

The canonical 44 are balanced **English (23) + Hebrew (21)**. Across all 68
generated fixtures:

| Language | Fixtures | Canonical-44 |
|---|---|---|
| English | 37 | 23 |
| Hebrew | 31 | 21 |

| Generator model | Fixtures | Canonical-44 |
|---|---|---|
| `gpt-5.4` (chat-completions batch) | 28 | 21 |
| `gpt-5.4-pro` (responses batch) | 31 | 23 |
| `handwritten` (no model) | 9 | 0 |

Per-asset detail — every fixture's language and generating model — is in
[`docs/ASSETS.md`](docs/ASSETS.md).

## Why the units are trustworthy

Every synthetic unit was independently QA'd: an LLM from a *different* family
than the generator re-labeled each article, a holistic reviewer judged whether
the text actually earns its committed labels, and borderline cases were
adjudicated by a stronger model. 15 of the 44 canonical units were found to
drift from their labels and were rewritten until they passed; all 44 now pass.
Full write-up in [`docs/REVIEW-REPORT.md`](docs/REVIEW-REPORT.md); provenance and
hazards in [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md).

## Real-outlet references

Real news HTML is copyrighted and **not redistributed**.
`data/real-outlets/urls.jsonl` lists 9 original article URLs (BBC, Haaretz, The
Onion, Ynet, Mako) with their labels, for real-world diversity on top of the
synthetic core. Fetch them yourself to reproduce locally.

## Loading the data

```python
import json
units = [json.loads(l) for l in open("data/units.jsonl")]
print(len(units), "canonical units")
# each unit: id, lang, bucket, expected{6 dims + overall_band}, generator_model, html_path
html = open(units[0]["html_path"], encoding="utf-8").read()
```

## Validation

`tools/validate.py` runs an integrity + consistency check over the whole dataset
(enum validity, fixture↔record mapping, doc↔data agreement, manifest accuracy,
link hygiene, and a content-safety scan). Run it after any edit:

```bash
python3 tools/validate.py    # exits non-zero on any failure
```

## Scope & attribution

This dataset measures credibility agents in general. It was built around the
**Legit** Chrome extension as the reference agent, but Legit's verbatim prompts
are intellectual property of that project and are **not** part of this
repository — only the agent-agnostic label taxonomy ([`docs/RUBRIC.md`](docs/RUBRIC.md)).
The evaluation harness lives in the separate `agent-reliability-eval` project.

## License

Data and documentation: [CC-BY-4.0](LICENSE). Attribution: *ISOC-IL Labs,
agent-reliability-eval-data*. Synthetic content is fictional; real-outlet URLs
point to third-party copyrighted material not redistributed here.
