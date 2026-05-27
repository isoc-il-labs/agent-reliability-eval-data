# GPT-5.5 review & revision of the 44 synthetic fixtures

> _Scope note: references to `harness/`, `run.js`, `report.js`, and similar scripts point to the separate **agent-reliability-eval** framework repository, not to files in this dataset repo._

**Date:** 2026-05-25
**Scope:** the 44 LLM-generated synthetic articles used as eval units in M3 — 18 from the `gpt-5.4` chat track (`articles-m3-generated.jsonl`) + 26 from the `gpt-5.4-pro` track (`articles-m3-generated-pro.jsonl`), all derived from the 26 seeds in `dataset/seeds/m3-seeds.jsonl`.
**Models:** `gpt-5.5` (bulk labeling + holistic review + re-validation) and `gpt-5.5-pro` (disagreement tie-break + rewrites). Both confirmed batch-compatible on 2026-05-25 (the `-pro = completions-only` restriction of the 5.2/5.4 generation no longer applies).

## Headline result

- **15 of 44 fixtures (34%) were found to not yet earn their seed-committed labels** and were auto-rewritten by `gpt-5.5-pro`.
- **All 15 rewrites now pass holistic review (15/15 REVISE_TEXT → PASS).**
- The other **29 fixtures were confirmed PASS** — including by a `gpt-5.5-pro` tie-break that cleared every PASS-with-label-disagreement case.
- **Zero seed labels were judged wrong** (0 FLAG_SEED). The seeds' ground truth held up; only some texts had drifted from it.
- Originals are byte-for-byte untouched; revisions live in a parallel track.

## Why this was worth doing

The whole M3 benchmark rests on one assumption: that each synthetic article *actually exhibits* the attributes its seed pre-committed, so the seed's `expected` labels are valid ground truth. If a fixture is weak or off-bucket, the ground truth is silently contaminated. This pass audits that assumption with a different model family than the one that generated the texts.

A representative real defect that was caught and fixed:

| | `gen-satire-en-02` |
|---|---|
| Expected `author` | **ANONYMOUS** |
| Original byline | "By Eliza Vane" — a *named* author, contradicting the label |
| Rewritten byline | "Staff Report" — supports ANONYMOUS, satire content preserved |

This is exactly the kind of quiet fixture/label mismatch that an accuracy benchmark cannot afford.

## Method — 5 stages

| Stage | What | Model | Output |
|---|---|---|---|
| 0 | Probe batch compatibility | gpt-5.5 + gpt-5.5-pro | `.model-id-5.5*` |
| 1 | Independent blind re-labeling on the 6-agent rubric | gpt-5.5 | `results/relabel-5.5/labels.jsonl` |
| 2 | Holistic faithfulness review (PASS / REVISE_TEXT / FLAG_SEED) | gpt-5.5 | `results/review-5.5/review.jsonl` |
| 3 | Flag logic + tie-break of borderline/conflicting cases | gpt-5.5-pro | `results/triage-5.5pro/triage.jsonl` |
| 4 | Auto-rewrite flagged fixtures into new variants | gpt-5.5-pro | `dataset/html/<id>-r.html`, `dataset/articles-m3-reviewed.jsonl` |
| 5 | Re-validate rewrites (re-label + re-review) | gpt-5.5 | `results/revalidate-5.5/`, `results/rereview-5.5/` |

**Flag logic (Stage 3).** A fixture is a clear PASS only if the holistic verdict is PASS *and* its independent labels exactly match the seed. A fixture is a clear rewrite only if the verdict is REVISE_TEXT *and* ≥2 of its 6 labels disagree. Everything else — every PASS that carried even one label disagreement — was sent to `gpt-5.5-pro` to adjudicate. The rewriter only fires on a final REVISE_TEXT verdict; a FLAG_SEED would have been surfaced for a human decision rather than auto-changed.

## Stage 2 review — flags by bucket

| Bucket | Fixtures | REVISE_TEXT | Pattern |
|---|---|---|---|
| satire | 8 | **8** | Hardest class. Synthetic satire that must avoid real outlets/figures rarely reads *unmistakably* as satire; some also carried label mismatches (e.g. named byline vs ANONYMOUS). |
| low-credibility | 10 | 7 | Often not *unreliable enough* — too measured to earn UNRELIABLE / CONTRADICTS_CONSENSUS. |
| credible-but-opinionated | 7 | 2 | A couple read closer to straight news than opinion. |
| gold-credible | 6 | 0 | All clean. |
| mainstream-israeli-news | 8 | 0 | All clean. |
| tabloid-clickbait | 7 | 0 | All clean. |

## Stage 3 tie-break — calibration vs defects

Raw label disagreement between the independent `gpt-5.5` labeling and the seed labels ran at **47% (124/264 agent labels)**. That number is misleading on its own: most disagreements are *calibration adjacency* — neighboring values like `author: SUSPICIOUS` vs expected `ANONYMOUS`, or `consensus: UNVERIFIABLE` vs `CONTRADICTS_CONSENSUS`. `gpt-5.5-pro` adjudicated all 29 PASS-with-disagreement fixtures and confirmed **every one as PASS**, with no seed labels flagged as wrong. Conclusion: raw label-diff is not a fixture-quality signal; the holistic verdict is.

## Stage 5 re-validation — did the rewrites work?

- **Holistic re-review (the decisive metric): 15/15 rewrites → PASS.**
- Re-labeling disagreement (secondary metric): **54 → 37 (−31%)** over 14 re-labeled variants. The low-credibility/unreliable rewrites improved sharply (several 3→0/3→1); satire stayed ~4 because the rubric has **no SATIRE enum** and forces satire → `source-format: UNRELIABLE`, so even a perfect satire fixture registers as "disagreeing." This is a rubric-representation gap, not a text defect — confirmed by the unanimous PASS on re-review.
- One re-label call returned empty JSON (`gen-opinion-en-02-pro-r`); moot, since its holistic re-review passed. Re-runnable via `replay`-style single call if a clean re-label is wanted.

## The 15 rewritten fixtures

`gen-unreliable-en-02`, `gen-unreliable-en-03`, `gen-unreliable-he-03`, `gen-opinion-en-02`, `gen-satire-en-02`, `gen-satire-he-01`, `gen-unreliable-en-02-pro`, `gen-unreliable-en-03-pro`, `gen-unreliable-he-03-pro`, `gen-opinion-en-02-pro`, `gen-satire-en-01-pro`, `gen-satire-en-02-pro`, `gen-satire-he-01-pro`, `gen-satire-he-02-pro`, `gen-unreliable-he-01-pro`

Each is saved as `dataset/html/<id>-r.html` with a `dataset/articles-m3-reviewed.jsonl` line carrying `original_id`, `reviewer_model`, `rewriter_model`, and the unchanged seed-committed `expected` labels.

## Caveats (carry into `methodology_note.md`)

1. **Reproducibility.** Originals are untouched. The revised set is a parallel **m3-reviewed** track. Any prior Gemini M3 numbers were computed on the originals; to use the revised fixtures, the Gemini benchmark must be **re-run on the m3-reviewed set** and reported as a delta — not silently swapped.
2. **Circularity.** OpenAI generated → OpenAI reviewed → OpenAI labeled is *internal consistency*, not independent ground truth. Gemini remains the system under test; the seed-committed labels remain primary truth. Cross-checking `gpt-5.5` against `gpt-5.5-pro` mitigates single-model bias but does not eliminate the shared-vendor prior.
3. **Rubric gap on satire.** *(Resolved 2026-05-25 — see Addendum below.)* At the time of this QA pass the Legit rubric had no SATIRE enum and satire was mapped to `UNRELIABLE`, which systematically inflated label-disagreement on satire fixtures regardless of text quality, so the holistic verdict was the correct quality signal for that bucket. The rubric now carries a `SATIRE` enum and the satire units are relabeled `consensus-format=SATIRE`.

## Cost

162 batch requests across 6 stages, **~417K tokens** (254K in / 163K out), batch-discounted — a few dollars.

## Addendum — satire rubric gap closed (2026-05-25)

The "rubric gap on satire" flagged throughout this report (satire forced onto the credibility axis, inflating label-disagreement) has since been **closed**. Reviewing the reference agent's current build (as of 2026-05-25) showed the agent now emits dedicated `SATIRE` and `ENTERTAINMENT_GOSSIP` ratings (with a satire short-circuit in both the source-verify and consensus-verify prompts), plus `UNVERIFIABLE` on the author axis. The eval was lagging that change. The iteration:

- added `SATIRE` + `ENTERTAINMENT_GOSSIP` to `source-format`/`consensus-format` and `UNVERIFIABLE` to `author` in `rubric.js`, with scores in `scoring.js` (`SATIRE`=25, `ENTERTAINMENT_GOSSIP`=40) and ordinal axes in `report.js`;
- relabeled the 6 satire units (and their raw-track variants) to `consensus-format=SATIRE` while keeping `source-format=NEUTRAL` — satire is a content property, and the example.com fixtures have no identifiable satire *publisher*. The baseline run validated this: the agent returned `consensus-format=SATIRE` 9/12 but `source-format=NEUTRAL` 11/12;
- fixed `run.js` to read each unit's `html_path` (it had hardcoded the pre-reorg `dataset/html/<id>.html` path) and to auto-prefer a local `adapters/agent.js`.

Net effect: satire is now measured as its own off-axis category, so a correct satire call scores as an exact match instead of a forced "disagreement." The historical Stage-5 figure (satire disagreement stuck ~4) reflects the pre-fix rubric and is left intact above as a record.

## Artifacts

- Scripts: `harness/batch/{probe_55,review,triage,rewrite}.js` (Stage 1 + re-validate reuse the existing `label.js`).
- Raw batch outputs + parsed results under `results/{relabel-5.5,review-5.5,triage-5.5pro,revalidate-5.5,rereview-5.5}/`.
- Revised fixtures: `dataset/html/*-r.html` + `dataset/articles-m3-reviewed.jsonl`.
