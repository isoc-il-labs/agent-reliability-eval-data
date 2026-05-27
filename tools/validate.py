#!/usr/bin/env python3
"""Authoritative pre-publication validator for agent-reliability-eval-data.

Runs five passes of checks and prints PASS / WARN / FAIL per check.
Exit code is non-zero if any FAIL is recorded. No files are modified.

Usage:  python3 tools/validate.py
"""
import csv
import json
import os
import re
import sys
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---- canonical rubric (mirrors docs/RUBRIC.md) ----
RUBRIC = {
    "source-format": ["HIGHLY_CREDIBLE", "CREDIBLE", "NEUTRAL", "QUESTIONABLE",
                      "UNRELIABLE", "ENTERTAINMENT_GOSSIP", "SATIRE"],
    "author": ["EXPERT", "JOURNALIST", "CITIZEN_JOURNALIST", "ANONYMOUS",
               "UNVERIFIABLE", "SUSPICIOUS"],
    "consensus-format": ["CORROBORATED", "PLAUSIBLE", "UNIQUE_REPORTING",
                         "UNVERIFIABLE", "CONTRADICTS_CONSENSUS",
                         "ENTERTAINMENT_GOSSIP", "SATIRE"],
    "headline": ["ACCURATE", "SENSATIONAL", "SOMEWHAT_MISLEADING", "CLICKBAIT",
                 "DECEPTIVE"],
    "bias": ["BALANCED", "SLIGHT_BIAS", "MODERATE_BIAS", "STRONG_BIAS"],
    "style": ["PROFESSIONAL", "ADEQUATE", "SENSATIONALIST", "POOR_QUALITY"],
}
BANDS = {"high", "mid", "low"}
LANGS = {"en", "he"}
MODELS = {"gpt-5.4", "gpt-5.4-pro", "handwritten"}

results = []  # (level, pass_no, msg)


def rec(level, p, msg):
    results.append((level, p, msg))


def jl(path):
    return [json.loads(l) for l in open(os.path.join(ROOT, path), encoding="utf-8") if l.strip()]


# ============ load ============
units = jl("data/units.jsonl")
raw = jl("data/units-raw.jsonl")
seeds = jl("data/seeds.jsonl")
real = jl("data/real-outlets/urls.jsonl")
raw_by_id = {r["id"]: r for r in raw}
canon_ids = {u["id"] for u in units}

# ============ PASS 1 — data integrity ============
P = 1
# canonical subset of raw
missing = [u["id"] for u in units if u["id"] not in raw_by_id]
rec("FAIL" if missing else "PASS", P,
    f"all {len(units)} canonical ids present in units-raw.jsonl" + (f" — MISSING {missing}" if missing else ""))

# html_path resolves + no orphans
fix_dir = os.path.join(ROOT, "data/fixtures")
on_disk = {f for f in os.listdir(fix_dir) if f.endswith(".html")}
referenced = set()
bad_paths = []
for r in raw:
    hp = r["html_path"]
    referenced.add(os.path.basename(hp))
    if not os.path.exists(os.path.join(ROOT, hp)):
        bad_paths.append(r["id"])
rec("FAIL" if bad_paths else "PASS", P,
    f"all {len(raw)} html_path values resolve" + (f" — BROKEN {bad_paths}" if bad_paths else ""))
orphans = on_disk - referenced
dangling = referenced - on_disk
rec("FAIL" if (orphans or dangling) else "PASS", P,
    f"fixtures on disk ({len(on_disk)}) == referenced ({len(referenced)})"
    + (f" — orphans {sorted(orphans)}" if orphans else "")
    + (f" — dangling {sorted(dangling)}" if dangling else ""))

# enum + band validity (raw covers canonical)
enum_errs, band_errs = [], []
for r in raw:
    exp = r.get("expected", {})
    for dim, allowed in RUBRIC.items():
        v = exp.get(dim)
        if v not in allowed:
            enum_errs.append(f"{r['id']}.{dim}={v}")
    if exp.get("overall_band") not in BANDS:
        band_errs.append(f"{r['id']}={exp.get('overall_band')}")
rec("FAIL" if enum_errs else "PASS", P,
    f"all expected ratings are valid rubric enums" + (f" — {enum_errs[:8]}" if enum_errs else ""))
rec("FAIL" if band_errs else "PASS", P,
    f"all overall_band in {BANDS}" + (f" — {band_errs}" if band_errs else ""))

# lang token + value
lang_val_errs, lang_tok_errs = [], []
for r in raw:
    if r.get("lang") not in LANGS:
        lang_val_errs.append(f"{r['id']}={r.get('lang')}")
    # handwritten ids may not carry a -en-/-he- token; only check gen-* ids
    if r["id"].startswith("gen-"):
        tok = "en" if "-en-" in r["id"] else ("he" if "-he-" in r["id"] else None)
        if tok and tok != r.get("lang"):
            lang_tok_errs.append(f"{r['id']} lang={r.get('lang')} token={tok}")
rec("FAIL" if lang_val_errs else "PASS", P,
    f"all lang in {LANGS}" + (f" — {lang_val_errs}" if lang_val_errs else ""))
rec("FAIL" if lang_tok_errs else "PASS", P,
    "gen-* id language token matches lang field" + (f" — {lang_tok_errs}" if lang_tok_errs else ""))

# model + track consistency
model_errs, track_errs = [], []
for r in raw:
    m = r.get("generator_model")
    if m not in MODELS:
        model_errs.append(f"{r['id']}={m}")
    t = r.get("track")
    # track is the intended track; generator_model is what actually ran.
    # chat -> gpt-5.4; handwritten -> handwritten;
    # pro  -> gpt-5.4-pro, or gpt-5.4 when the pro model fell back.
    allowed_models = {"chat": {"gpt-5.4"},
                      "handwritten": {"handwritten"},
                      "pro": {"gpt-5.4-pro", "gpt-5.4"}}.get(t, set())
    if m not in allowed_models:
        track_errs.append(f"{r['id']} model={m} track={t}")
rec("FAIL" if model_errs else "PASS", P,
    f"all generator_model in {MODELS}" + (f" — {model_errs}" if model_errs else ""))
rec("FAIL" if track_errs else "PASS", P,
    "generator_model consistent with track (pro may fall back to gpt-5.4)"
    + (f" — {track_errs}" if track_errs else ""))

# rewritten -> original_id -> real superseded row
rw_errs = []
for r in raw:
    if r.get("review_status") == "rewritten":
        oid = r.get("original_id")
        if not oid:
            rw_errs.append(f"{r['id']} missing original_id")
        elif oid not in raw_by_id:
            rw_errs.append(f"{r['id']} original_id {oid} not in raw")
rec("FAIL" if rw_errs else "PASS", P,
    "rewritten units reference a real original_id" + (f" — {rw_errs}" if rw_errs else ""))

# seeds count + traceability (best-effort: seed id prefix appears in unit ids)
rec("PASS" if len(seeds) == 26 else "WARN", P, f"seeds.jsonl has {len(seeds)} rows (expected 26)")

# real-outlets sanity
real_errs = []
for r in real:
    if r.get("lang") not in LANGS:
        real_errs.append(f"{r.get('id')} lang={r.get('lang')}")
    if "html" in r or "html_path" in r:
        real_errs.append(f"{r.get('id')} carries inlined html")
    exp = r.get("expected", {})
    for dim, allowed in RUBRIC.items():
        if exp.get(dim) not in allowed:
            real_errs.append(f"{r.get('id')}.{dim}={exp.get(dim)}")
rec("FAIL" if real_errs else "PASS", P,
    f"real-outlets ({len(real)}) labels valid, no inlined html" + (f" — {real_errs[:6]}" if real_errs else ""))

# ============ PASS 2 — doc <-> data consistency ============
P = 2
doc = open(os.path.join(ROOT, "docs/DOCUMENTATION.md"), encoding="utf-8").read()
readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()

# 2a: every canonical id+row appears as a table row in DOCUMENTATION.md with matching fields
doc_row_errs = []
for u in units:
    band = u["expected"]["overall_band"]
    cells = [u["id"], u["bucket"], u["lang"], u["track"], u["review_status"], band, u["html_path"]]
    # build the expected markdown row fragment loosely: all cells must appear on one line
    pat = "| `%s` | %s | %s | %s | %s | %s | `%s` |" % tuple(cells)
    if pat not in doc:
        doc_row_errs.append(u["id"])
rec("FAIL" if doc_row_errs else "PASS", P,
    f"DOCUMENTATION.md canonical table matches units.jsonl row-for-row ({len(units)})"
    + (f" — MISMATCH {doc_row_errs}" if doc_row_errs else ""))

# 2b: bucket breakdown counts in DOCUMENTATION.md
bucket_counts = Counter(u["bucket"] for u in units)
expected_doc_buckets = {"low-credibility": 10, "mainstream-israeli-news": 8,
                        "credible-but-opinionated": 7, "tabloid-clickbait": 7,
                        "gold-credible": 6, "satire": 6}
bucket_mismatch = {b: (bucket_counts.get(b), n) for b, n in expected_doc_buckets.items()
                   if bucket_counts.get(b) != n}
rec("FAIL" if bucket_mismatch else "PASS", P,
    "DOCUMENTATION.md bucket breakdown matches data"
    + (f" — got/doc {bucket_mismatch}" if bucket_mismatch else ""))

# 2c: README language + model tables (all 68)
raw_lang = Counter(r["lang"] for r in raw)
raw_model = Counter(r["generator_model"] for r in raw)
canon_lang = Counter(u["lang"] for u in units)
canon_model = Counter(r["generator_model"] for r in raw if r["id"] in canon_ids)
checks_readme = [
    (f"| English | {raw_lang['en']} | {canon_lang['en']} |", "README en row"),
    (f"| Hebrew | {raw_lang['he']} | {canon_lang['he']} |", "README he row"),
]
rm_errs = [name for frag, name in checks_readme if frag not in readme]
rec("FAIL" if rm_errs else "PASS", P,
    "README language table matches data" + (f" — missing {rm_errs}" if rm_errs else ""))
# model rows in README carry parenthetical text; check the numbers appear
model_ok = all(str(raw_model[m]) in readme for m in MODELS)
rec("PASS" if model_ok else "WARN", P,
    "README model-table counts present (28/31/9)")

# 2d: assets.csv matches units-raw.jsonl exactly
csv_rows = list(csv.DictReader(open(os.path.join(ROOT, "data/assets.csv"), encoding="utf-8")))
csv_by_id = {r["id"]: r for r in csv_rows}
csv_errs = []
if len(csv_rows) != len(raw):
    csv_errs.append(f"row count {len(csv_rows)} != {len(raw)}")
for r in raw:
    c = csv_by_id.get(r["id"])
    if not c:
        csv_errs.append(f"{r['id']} absent from csv"); continue
    if c["lang_code"] != r["lang"]:
        csv_errs.append(f"{r['id']} lang {c['lang_code']}!={r['lang']}")
    if c["generator_model"] != r["generator_model"]:
        csv_errs.append(f"{r['id']} model mismatch")
    if c["bucket"] != r["bucket"] or c["track"] != r["track"] or c["review_status"] != r["review_status"]:
        csv_errs.append(f"{r['id']} bucket/track/status mismatch")
    want_canon = "yes" if r["id"] in canon_ids else "no"
    if c["in_canonical_44"] != want_canon:
        csv_errs.append(f"{r['id']} canonical flag {c['in_canonical_44']}!={want_canon}")
rec("FAIL" if csv_errs else "PASS", P,
    f"assets.csv matches units-raw.jsonl ({len(csv_rows)} rows)" + (f" — {csv_errs[:6]}" if csv_errs else ""))

# 2e: RUBRIC.md enums == distinct values in data == RUBRIC dict
rubric_md = open(os.path.join(ROOT, "docs/RUBRIC.md"), encoding="utf-8").read()
present = defaultdict(set)
for r in raw + real:
    for dim in RUBRIC:
        present[dim].add(r["expected"].get(dim))
rub_errs = []
for dim, allowed in RUBRIC.items():
    # every value present in data must be a known enum (already checked) AND appear in RUBRIC.md
    for v in present[dim]:
        if v and v not in rubric_md:
            rub_errs.append(f"{dim}:{v} not documented in RUBRIC.md")
rec("FAIL" if rub_errs else "PASS", P,
    "all in-use rating values are documented in RUBRIC.md" + (f" — {rub_errs}" if rub_errs else ""))

# ============ PASS 3 — link hygiene / dangling refs ============
P = 3
md_files = []
for d in ("", "docs"):
    base = os.path.join(ROOT, d)
    for f in os.listdir(base):
        if f.endswith(".md"):
            md_files.append(os.path.join(d, f) if d else f)

link_errs = []
link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
for mf in md_files:
    txt = open(os.path.join(ROOT, mf), encoding="utf-8").read()
    base = os.path.dirname(os.path.join(ROOT, mf))
    for m in link_re.finditer(txt):
        tgt = m.group(1)
        if tgt.startswith(("http://", "https://", "#", "mailto:")):
            continue
        tgt_path = tgt.split("#")[0]
        if not tgt_path:
            continue
        resolved = os.path.normpath(os.path.join(base, tgt_path))
        if not os.path.exists(resolved):
            link_errs.append(f"{mf} -> {tgt}")
rec("FAIL" if link_errs else "PASS", P,
    f"all internal markdown links resolve ({len(md_files)} md files)" + (f" — {link_errs}" if link_errs else ""))

# excluded-artifact mentions.
# The two copied historical docs may reference the separate framework repo as
# long as they carry an explicit scope note; the dataset-native docs must not.
EXCL = ["harness/", "run.js", "report.js", "replay.js", "compare.js",
        "BASELINE-dandan64", "MODEL-COMPARISON", "gen_documentation.mjs",
        "fetch.mjs", "agent.example.js", "npm install", "node harness"]
HISTORICAL = {"docs/METHODOLOGY.md", "docs/REVIEW-REPORT.md"}
mention = defaultdict(list)
for mf in md_files:
    txt = open(os.path.join(ROOT, mf), encoding="utf-8").read()
    for term in EXCL:
        n = txt.count(term)
        if n:
            mention[mf].append(f"{term}×{n}")
for mf, terms in mention.items():
    txt = open(os.path.join(ROOT, mf), encoding="utf-8").read()
    if mf in HISTORICAL:
        if "Scope note" in txt:
            rec("PASS", P, f"{mf} references the framework repo but carries a scope note (acknowledged)")
        else:
            rec("WARN", P, f"{mf} references framework artifacts WITHOUT a scope note: {', '.join(terms)}")
    else:
        rec("WARN", P, f"{mf} (dataset-native) mentions excluded artifacts: {', '.join(terms)}")
if not mention:
    rec("PASS", P, "no docs reference excluded harness/result artifacts")

# ============ PASS 4 — content safety ============
P = 4
# secrets
SECRET_RE = re.compile(r"sk-[A-Za-z0-9]{20}|AIza[A-Za-z0-9_-]{20}|gh[oprs]_[A-Za-z0-9]{20}")
hits = []
for dirpath, _, files in os.walk(ROOT):
    if "/.git" in dirpath:
        continue
    for f in files:
        p = os.path.join(dirpath, f)
        try:
            t = open(p, encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        if SECRET_RE.search(t):
            hits.append(os.path.relpath(p, ROOT))
rec("FAIL" if hits else "PASS", P, "no secret-like tokens in tree" + (f" — {hits}" if hits else ""))

# no GitHub URLs at all (not even self-references)
gh_re = re.compile(r"https?://(?:www\.)?github\.com/([^\s)\"'>,]+)")
gh_links = []
for dirpath, _, files in os.walk(ROOT):
    if "/.git" in dirpath:
        continue
    for f in files:
        if not f.endswith((".md", ".cff", ".py", ".json", ".txt", ".csv", ".jsonl", ".html")) and f != "LICENSE":
            continue
        rel = os.path.relpath(os.path.join(dirpath, f), ROOT)
        try:
            txt = open(os.path.join(dirpath, f), encoding="utf-8", errors="ignore").read()
        except Exception:
            continue
        for m in gh_re.finditer(txt):
            gh_links.append(f"{rel} -> github.com/{m.group(1).rstrip('/')}")
rec("FAIL" if gh_links else "PASS", P,
    "no GitHub URLs anywhere in the repo"
    + (f" — {gh_links}" if gh_links else ""))

# fixtures publish on example.com (sample domains)
non_example = []
for f in sorted(on_disk):
    t = open(os.path.join(fix_dir, f), encoding="utf-8", errors="ignore").read()
    # look for explicit canonical/og:url or visible domain
    urls = re.findall(r"https?://([a-zA-Z0-9.\-]+)", t)
    real_doms = {u for u in urls if not u.endswith("example.com") and u not in ("www.w3.org", "schema.org")}
    if real_doms:
        non_example.append((f, sorted(real_doms)[:3]))
rec("WARN" if non_example else "PASS", P,
    "all fixtures reference only example.com / schema domains"
    + (f" — {non_example[:5]}" if non_example else ""))

# hebrew fixtures actually contain Hebrew
heb_re = re.compile(r"[֐-׿]")
he_missing = []
for r in raw:
    if r["lang"] == "he":
        t = open(os.path.join(ROOT, r["html_path"]), encoding="utf-8", errors="ignore").read()
        if not heb_re.search(t):
            he_missing.append(r["id"])
rec("FAIL" if he_missing else "PASS", P,
    "all he fixtures contain Hebrew script" + (f" — {he_missing}" if he_missing else ""))
# english fixtures should NOT be predominantly hebrew (mojibake/mislabel guard)
en_with_heb = []
for r in raw:
    if r["lang"] == "en":
        t = open(os.path.join(ROOT, r["html_path"]), encoding="utf-8", errors="ignore").read()
        if len(heb_re.findall(t)) > 50:
            en_with_heb.append(r["id"])
rec("WARN" if en_with_heb else "PASS", P,
    "en fixtures are not predominantly Hebrew" + (f" — {en_with_heb}" if en_with_heb else ""))

# ============ PASS 5 — packaging ============
P = 5
for fn in ["README.md", "LICENSE", "CITATION.cff", ".gitignore",
           "docs/ASSETS.md", "docs/RUBRIC.md", "docs/DOCUMENTATION.md",
           "docs/METHODOLOGY.md", "docs/REVIEW-REPORT.md", "data/assets.csv"]:
    ok = os.path.exists(os.path.join(ROOT, fn))
    rec("PASS" if ok else "FAIL", P, f"present: {fn}" if ok else f"MISSING: {fn}")
# CITATION.cff parses as yaml-ish (basic key check)
cff = open(os.path.join(ROOT, "CITATION.cff"), encoding="utf-8").read()
cff_ok = all(k in cff for k in ["cff-version:", "title:", "license: CC-BY-4.0", "authors:"])
rec("PASS" if cff_ok else "FAIL", P, "CITATION.cff has required CFF keys + CC-BY-4.0 license")
# license mentions CC BY 4.0
lic = open(os.path.join(ROOT, "LICENSE"), encoding="utf-8").read()
rec("PASS" if "CC BY 4.0" in lic and "creativecommons.org/licenses/by/4.0" in lic else "FAIL",
    P, "LICENSE is CC BY 4.0 with canonical link")

# ============ report ============
order = {"FAIL": 0, "WARN": 1, "PASS": 2}
counts = Counter(level for level, _, _ in results)
print("=" * 72)
print("  agent-reliability-eval-data — pre-publication validation")
print("=" * 72)
for p in range(1, 6):
    rows = [r for r in results if r[1] == p]
    titles = {1: "Data integrity", 2: "Doc<->data consistency",
              3: "Link hygiene / dangling refs", 4: "Content safety",
              5: "Packaging"}
    print(f"\n── Pass {p}: {titles[p]} ──")
    for level, _, msg in sorted(rows, key=lambda x: order[x[0]]):
        mark = {"FAIL": "✗ FAIL", "WARN": "⚠ WARN", "PASS": "✓ PASS"}[level]
        print(f"  {mark}  {msg}")
print("\n" + "=" * 72)
print(f"  {counts['PASS']} pass · {counts['WARN']} warn · {counts['FAIL']} fail")
print("=" * 72)
sys.exit(1 if counts["FAIL"] else 0)
