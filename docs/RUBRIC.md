# Rubric — the six credibility dimensions

The `expected` labels on every unit (`data/units.jsonl`, `data/units-raw.jsonl`,
`data/real-outlets/urls.jsonl`) are drawn from this fixed vocabulary. It is a
**generic news-credibility taxonomy** — only the rating vocabulary and what each
rating means. It contains no agent-specific prompt text, so labels are
comparable across any credibility agent.

Each unit's `expected` object carries one rating from each of the six
dimensions below, plus an `overall_band`:

- **`overall_band`** — the target credibility band for the unit as a whole, on a
  0–100 axis: `high` ≥ 70 · `mid` 40–69 · `low` < 40.

Within each dimension, ratings are listed **best → worst** on the credibility axis.

## 1. `source-format`
Credibility of the publisher (parent organization) behind the domain. Based on
external reputation, funding transparency, and history of corrections.
`ENTERTAINMENT_GOSSIP` and `SATIRE` sit *off* the credibility axis — they
describe what the outlet *is* (a virality/celebrity content mill, or a parody
site) rather than how reliably it reports facts.

`HIGHLY_CREDIBLE` · `CREDIBLE` · `NEUTRAL` · `QUESTIONABLE` · `UNRELIABLE` · `ENTERTAINMENT_GOSSIP` · `SATIRE`

## 2. `author`
Credibility of the article author(s).

- `EXPERT` — recognized authority with credentials.
- `JOURNALIST` — verifiable staff/freelance writer at an established outlet.
- `CITIZEN_JOURNALIST` — independent contributor with traceable history.
- `ANONYMOUS` — no specific author (byline is "Staff"/"Admin"/absent).
- `UNVERIFIABLE` — a name is given but has no traceable digital footprint outside this domain (possibly fabricated).
- `SUSPICIOUS` — failed verification or known misinformation purveyor.

## 3. `consensus-format`
Whether the article's factual claims are corroborated by independent sources.

- `CORROBORATED` — multiple independent Tier-1 outlets confirm.
- `PLAUSIBLE` — secondary sources, no circular reporting.
- `UNIQUE_REPORTING` — breaking news / exclusive investigation.
- `UNVERIFIABLE` — no independent matches after both confirmation and refutation searches (a genuine evidence vacuum).
- `CONTRADICTS_CONSENSUS` — fact-checkers debunk the claim, or independent outlets report materially different facts.
- `ENTERTAINMENT_GOSSIP` / `SATIRE` — short-circuit fact-checking: virality-driven or parody content that makes no genuine factual claim to corroborate.

## 4. `headline`
Relationship between the headline and the body.

- `ACCURATE` — neutral factual summary.
- `SENSATIONAL` — factual but uses emotional language.
- `SOMEWHAT_MISLEADING` — technically true but framed to suggest a false conclusion.
- `CLICKBAIT` — curiosity-gap or mystery framing.
- `DECEPTIVE` — directly contradicts or invents claims not in the body.

## 5. `bias`
Bias in the article's language and framing.

- `BALANCED` — no detectable bias.
- `SLIGHT_BIAS` — minor framing choices.
- `MODERATE_BIAS` — clearly one-sided but with attribution.
- `STRONG_BIAS` — heavily partisan, one-sided, emotional.

## 6. `style`
Journalistic writing quality.

- `PROFESSIONAL` — neutral tone, clear attribution, good structure, no errors.
- `ADEQUATE` — readable, mostly neutral, minor flaws.
- `SENSATIONALIST` — highly emotional language, aggressive tone.
- `POOR_QUALITY` — riddled with errors, incoherent, or clearly AI-generated spam.

---

_This rubric is the data schema for the `expected` labels. It is reproduced from
the canonical machine-readable definition used by the (separate) evaluation
harness; this dataset repository ships the labels and their vocabulary, not the
harness._
