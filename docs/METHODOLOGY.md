# Methodology

> _Scope note: this document describes the generation and QA pipeline. References to `harness/`, `agent.example.js`, and other scripts point to the separate **agent-reliability-eval** framework repository — they are not part of this dataset repo, which ships only the test units, fixtures, labels, and docs._

How the test units were built, where their ground truth comes from, and the known limitations to keep in mind when interpreting results.

## Test-unit construction

Each synthetic unit starts from a **seed** (`data/seeds.jsonl`) that pre-commits, before any text exists:

- a credibility **bucket** (e.g. `low-credibility`, `satire`, `gold-credible`),
- a list of **required attributes** the article must exhibit (e.g. *unnamed-sources*, *sensational-headline*, *anonymous-author*),
- the **expected labels** on all six rubric dimensions (`harness/adapters/rubric.js`) plus an overall band.

A generator model then writes a fictional article that must exhibit those attributes. Because the labels are fixed in the seed *before* generation, they are the **strongest available form of ground truth**: the article was written to instantiate exactly those properties, rather than being labeled after the fact.

Two generation tracks exist — a base model (`chat`) and a stronger reasoning variant (`pro`) — which together also form a generator-quality ablation. Generation enforces a hard guardrail (`harness/batch/generate.js`): **no real outlets and no real people** — all publishers, bylines, and figures are fictional.

## Ground-truth quality assurance

Seed-committed labels are only valid if the generated text actually earns them. Every unit was therefore audited by a **cross-model QA pipeline** using a different model family than the generator:

1. **Independent re-labeling** (`harness/batch/label.js`) — a fresh model blind-labels each article on the six rubric dimensions.
2. **Holistic review** (`harness/batch/review.js`) — a reviewer judges whether the text embodies its seed and earns its labels, returning `PASS`, `REVISE_TEXT` (the text drifted — rewrite it), or `FLAG_SEED` (the label itself looks wrong — a human decision).
3. **Triage + tie-break** (`harness/batch/triage.js`) — borderline and conflicting cases are escalated to a stronger adjudicator model.
4. **Rewrite** (`harness/batch/rewrite.js`) — units judged `REVISE_TEXT` are rewritten until they clearly earn their labels, preserving the seed's bucket and expected labels.

Result: of 44 synthetic units, 15 were rewritten and **all 44 now pass holistic review**; no seed labels were found to be wrong. The full run is in [REVIEW-REPORT.md](REVIEW-REPORT.md).

A key finding from this process: **raw label disagreement is a poor quality signal.** Independent labelers frequently choose a neighboring value (e.g. `ANONYMOUS` vs `SUSPICIOUS`), which is calibration adjacency, not a text defect. The holistic verdict — does the text embody the seed? — is the signal that matters.

## Known limitations & hazards

- **Shared-vendor circularity.** The synthetic units are generated, labeled, and reviewed by models from one vendor. That establishes internal consistency, not vendor-independent truth. The agent under test should be a *different* system; cross-checking a base model against a stronger one mitigates but does not remove this prior. A second-vendor labeling pass is a planned improvement (`TODO.md`).
- **Satire and the rubric.** *(Resolved 2026-05-25.)* Earlier, the rubric had no `SATIRE` value and satire was forced onto the credibility axis, which inflated label-disagreement on satire units regardless of text quality. The rubric now carries dedicated `SATIRE` and `ENTERTAINMENT_GOSSIP` enums on `source-format` and `consensus-format` (added when the reference agent itself began emitting them). Satire is treated as a *content* property: satire units are labeled `consensus-format=SATIRE` but `source-format=NEUTRAL`, because the publisher (these fixtures use `example.com`) is unknown — only a recognised satire *domain* would earn `source-format=SATIRE`. The baseline run confirmed the distinction: the agent emitted `consensus-format=SATIRE` on 9/12 satire trials but `source-format=NEUTRAL` on 11/12 (its publisher-reputation agent rates the domain, not the prose). Satire is now scored as its own off-axis category rather than mismeasured as unreliable news — though the *weighted overall* still lands mid-band (~56) against a `low` target, a real agent weakness the benchmark now surfaces cleanly.
- **Hebrew labeling.** The Hebrew half is model-labeled. Independent native-rater labeling with inter-rater agreement would make it publishable as a standalone Hebrew benchmark.
- **Live-web drift.** Agents that use web-search grounding will produce results that shift as the live web changes; this is inherent and not pinnable. Report per-unit variance across trials to quantify it.
- **Synthetic vs. real gap.** Synthetic units are clean, unambiguous test cases by design. The real-outlet set (`data/real-outlets/`) adds messier, real-world diversity but must be fetched locally because the HTML is copyrighted.

## What is intentionally not included

The reference agent's **verbatim prompts** are its own intellectual property and are not redistributed. The harness ships an agent-agnostic adapter template (`harness/adapters/agent.example.js`); you supply your own agent's prompts. The rating→score calibration in `harness/adapters/scoring.js` and the dimension weights are **examples** to be tuned per agent.
