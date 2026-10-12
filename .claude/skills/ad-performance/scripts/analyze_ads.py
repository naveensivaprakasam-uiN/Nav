#!/usr/bin/env python3
"""Compute ad KPIs from a Meta / Google / LinkedIn / TikTok CSV export.

Stdlib only. Normalises common column names, groups by a dimension, and
prints totals plus a ranked table with CTR, CPC, CPM, CPA, ROAS and CVR.

Usage:
    analyze_ads.py FILE.csv [--by COLUMN] [--target-cpa N] [--target-roas N]
                   [--min-spend N] [--map metric="Header"] [--top N] [--json]
"""
import argparse
import csv
import json
import re
import sys
from collections import OrderedDict

# Canonical metric -> header aliases (lowercased, currency suffix stripped).
ALIASES = {
    "spend": ["amount spent", "spend", "cost", "total spent", "amount spent (usd)", "total cost"],
    "impressions": ["impressions", "impr.", "impr"],
    "clicks": ["link clicks", "clicks", "clicks (all)", "outbound clicks"],
    "conversions": ["results", "conversions", "purchases", "leads", "website purchases",
                    "all conv.", "complete payment", "registrations", "app installs"],
    "revenue": ["purchase conversion value", "conversion value", "conv. value",
                "website purchase conversion value", "revenue", "total conversion value",
                "all conv. value"],
    "reach": ["reach"],
    "frequency": ["frequency"],
}
DIMENSIONS = ["ad name", "ad", "ad set name", "ad group", "ad group name", "campaign name",
              "campaign", "creative", "placement", "day", "date", "reporting starts", "week"]


def norm(h):
    h = h.strip().lower()
    h = re.sub(r"\s*\((?:[a-z]{3}|₹|\$|€|£)\)$", "", h)  # drop "(INR)" etc.
    return h


def num(v):
    if v is None:
        return 0.0
    v = re.sub(r"[^\d.\-]", "", str(v))
    try:
        return float(v) if v not in ("", "-", ".") else 0.0
    except ValueError:
        return 0.0


def div(a, b):
    return a / b if b else None


def kpis(r):
    return {
        "ctr": div(r["clicks"], r["impressions"]),
        "cpc": div(r["spend"], r["clicks"]),
        "cpm": div(r["spend"] * 1000, r["impressions"]),
        "cvr": div(r["conversions"], r["clicks"]),
        "cpa": div(r["spend"], r["conversions"]),
        "roas": div(r["revenue"], r["spend"]),
    }


def verdict(row, args):
    if row["spend"] < args.min_spend:
        return "low data"
    k = row["kpi"]
    if args.target_roas and k["roas"] is not None:
        if k["roas"] >= args.target_roas:
            return "SCALE"
        return "CUT" if k["roas"] < args.target_roas * 0.67 else "WATCH"
    if args.target_cpa:
        if k["cpa"] is None:
            return "CUT" if row["spend"] >= 2 * args.target_cpa else "WATCH"
        if k["cpa"] <= args.target_cpa:
            return "SCALE"
        return "CUT" if k["cpa"] > args.target_cpa * 1.5 else "WATCH"
    return ""


def fmt(v, kind):
    if v is None:
        return "—"
    if kind in ("ctr", "cvr"):
        return f"{v * 100:.2f}%"
    if kind == "roas":
        return f"{v:.2f}x"
    if kind in ("spend", "revenue", "cpc", "cpm", "cpa"):
        return f"{v:,.2f}"
    return f"{v:,.0f}"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("file")
    p.add_argument("--by")
    p.add_argument("--target-cpa", type=float)
    p.add_argument("--target-roas", type=float)
    p.add_argument("--min-spend", type=float, default=0)
    p.add_argument("--map", action="append", default=[], help='metric="Header name"')
    p.add_argument("--top", type=int, default=10)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    with open(args.file, newline="", encoding="utf-8-sig") as f:
        sample = f.read(4096)
        f.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel
        rows = list(csv.DictReader(f, dialect=dialect))
    if not rows:
        sys.exit("No rows found.")

    headers = list(rows[0].keys())
    by_norm = {norm(h): h for h in headers}
    colmap = {}
    for metric, names in ALIASES.items():
        for n in names:
            if n in by_norm:
                colmap[metric] = by_norm[n]
                break
    for m in args.map:
        k, _, v = m.partition("=")
        colmap[k.strip()] = v.strip().strip('"')

    if "spend" not in colmap:
        sys.exit(f"Could not find a spend column. Headers: {headers}\n"
                 'Re-run with --map spend="<header>".')

    dim = args.by
    if dim and dim not in headers:
        dim = by_norm.get(norm(dim))
        if not dim:
            sys.exit(f"--by column not found. Headers: {headers}")
    if not dim:
        dim = next((by_norm[d] for d in DIMENSIONS if d in by_norm), None)

    metrics = ["spend", "impressions", "clicks", "conversions", "revenue"]
    groups = OrderedDict()
    total = {m: 0.0 for m in metrics}
    for r in rows:
        # Skip summary rows that exports append (label can sit in any column).
        if any(str(v).strip().lower() in ("total", "totals", "grand total") for v in r.values()):
            continue
        key = (r.get(dim) or "(blank)").strip() if dim else "All"
        g = groups.setdefault(key, {m: 0.0 for m in metrics})
        for m in metrics:
            v = num(r.get(colmap[m])) if m in colmap else 0.0
            g[m] += v
            total[m] += v

    out = []
    for key, g in groups.items():
        row = {"name": key, **g, "kpi": kpis(g)}
        row["spend_share"] = div(g["spend"], total["spend"])
        row["verdict"] = verdict(row, args)
        out.append(row)

    has_rev = "revenue" in colmap and total["revenue"] > 0
    has_conv = "conversions" in colmap and total["conversions"] > 0
    if has_rev:
        sort_key = lambda r: -(r["kpi"]["roas"] or 0)
        rank_by = "ROAS (desc)"
    elif has_conv:
        sort_key = lambda r: r["kpi"]["cpa"] if r["kpi"]["cpa"] is not None else float("inf")
        rank_by = "CPA (asc)"
    else:
        sort_key = lambda r: -(r["kpi"]["ctr"] or 0)
        rank_by = "CTR (desc)"
    judged = sorted([r for r in out if r["spend"] >= args.min_spend], key=sort_key)
    low = [r for r in out if r["spend"] < args.min_spend]

    totals = {**total, "kpi": kpis(total), "rows": len(rows), "groups": len(out)}
    top_spend = sorted(out, key=lambda r: -r["spend"])
    n20 = max(1, round(len(out) * 0.2))
    totals["top20pct_spend_share"] = div(sum(r["spend"] for r in top_spend[:n20]), total["spend"])

    if args.json:
        json.dump({"columns": colmap, "dimension": dim, "rank_by": rank_by,
                   "totals": totals, "rows": judged + low}, sys.stdout, indent=2, default=str)
        print()
        return

    print(f"Columns used: {colmap}")
    print(f"Grouped by: {dim or '(none)'}   Ranked by: {rank_by}   Rows: {len(rows)} -> {len(out)} groups\n")
    print("TOTALS")
    for m in metrics:
        if m in colmap:
            print(f"  {m:<12}{fmt(total[m], m)}")
    needs = {"ctr": ["clicks", "impressions"], "cpc": ["clicks"], "cpm": ["impressions"],
             "cvr": ["conversions", "clicks"], "cpa": ["conversions"], "roas": ["revenue"]}
    for k, v in totals["kpi"].items():
        if all(n in colmap for n in needs[k]):
            print(f"  {k:<12}{fmt(v, k)}")
    print(f"  top 20% of {dim or 'rows'} take {fmt(totals['top20pct_spend_share'], 'ctr')} of spend\n")

    cols = ["spend", "conversions", "ctr", "cpc", "cpm", "cvr", "cpa", "roas"]
    if not has_rev:
        cols.remove("roas")
    if not has_conv:
        cols = [c for c in cols if c not in ("conversions", "cvr", "cpa")]
    show_verdict = bool(args.target_cpa or args.target_roas)

    def table(title, rs):
        print(title)
        hdr = ["name"] + cols + ["share"] + (["verdict"] if show_verdict else [])
        lines = [hdr]
        for r in rs:
            vals = [r["name"][:40]]
            for c in cols:
                vals.append(fmt(r[c] if c in r else r["kpi"][c], c))
            vals.append(fmt(r["spend_share"], "ctr"))
            if show_verdict:
                vals.append(r["verdict"])
            lines.append(vals)
        widths = [max(len(str(l[i])) for l in lines) for i in range(len(hdr))]
        for i, l in enumerate(lines):
            print("  " + "  ".join(str(v).ljust(widths[j]) if j == 0 else str(v).rjust(widths[j])
                                   for j, v in enumerate(l)))
            if i == 0:
                print("  " + "  ".join("-" * w for w in widths))
        print()

    if len(judged) <= args.top * 2:
        table(f"ALL ({len(judged)})", judged)
    else:
        table(f"TOP {args.top}", judged[:args.top])
        table(f"BOTTOM {args.top}", judged[-args.top:])
    if low:
        print(f"{len(low)} group(s) under --min-spend {args.min_spend:g} not judged: "
              + ", ".join(r["name"][:30] for r in low[:10]) + (" …" if len(low) > 10 else ""))


if __name__ == "__main__":
    main()
