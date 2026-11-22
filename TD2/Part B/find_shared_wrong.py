#!/usr/bin/env python3
"""TD 2 - Part B: find a shared wrong value and check Pair A's vote offline.

Run from the kit: python find_shared_wrong.py
Optional: --case C02 --reference reference-td1.csv --output c02-check.json
No API call. SQL execution remains in Part 2C's diagnostic script.
"""

import argparse
import ast
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent
PANEL_3 = [
    ("groq", "openai/gpt-oss-120b"),
    ("openrouter", "cohere/north-mini-code:free"),
    ("groq", "qwen/qwen3.8-27b"),
]
PANEL_5 = PANEL_3 + [
    ("groq", "openai/gpt-oss-20b"),
    ("openrouter", "dots-studio/dots-3-note-preview:free"),
]


def read_traces(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = {"case_id", "provider", "model_requested", "value", "sql",
                    "verdict", "reference", "date_utc", "attempts", "nature"}
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError("Missing CSV columns: " + ", ".join(sorted(missing)))
        rows = list(reader)
    real = [row for row in rows if row["nature"] == "real"]
    if not real:
        raise ValueError("No real traces found; replay and simulation rows are excluded.")
    latest = {}
    for index, row in enumerate(real):
        key = (row["case_id"], row["provider"], row["model_requested"])
        rank = (row["date_utc"], int(row["attempts"] or 0), index)
        if key not in latest or rank > latest[key][0]:
            latest[key] = (rank, row)
    return rows, real, {key: pair[1] for key, pair in latest.items()}


def shared_wrong(rows):
    groups = defaultdict(set)
    for row in rows:
        if row["verdict"] == "incorrect" and row["value"].strip():
            key = (row["case_id"], int(row["value"]))
            groups[key].add((row["provider"], row["model_requested"]))
    return [
        {"case_id": case, "wrong_value": value,
         "models": [provider + ":" + model for provider, model in sorted(models)]}
        for (case, value), models in sorted(groups.items()) if len(models) >= 2
    ]


def load_shared_vote(path):
    # Execute the exact submitted method, without importing API/SQLite helpers.
    # This is a source-method check in isolation, not a full atelier-vote run.
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    owner = next((node for node in tree.body if isinstance(node, ast.ClassDef)
                  and node.name == "Orchestrateur"), None)
    method = next((node for node in owner.body if isinstance(node, ast.FunctionDef)
                   and node.name == "vote_k_sur_n"), None) if owner else None
    if method is None:
        raise ValueError("Orchestrateur.vote_k_sur_n was not found in " + str(path))
    tree = ast.fix_missing_locations(ast.Module(body=[method], type_ignores=[]))
    namespace = {"Counter": Counter}
    exec(compile(tree, str(path), "exec"), namespace)
    return namespace["vote_k_sur_n"]


def ballot(provider, model, row):
    value = None
    if (row is not None and row["verdict"] in {"correct", "incorrect"}
            and row["sql"].strip() and not row.get("error", "").strip()):
        try:
            value = int(row["value"])
        except (ValueError, TypeError):
            pass
    return {"provider": provider, "model_requested": model, "value": value,
            "verdict": "executed" if value is not None else "error"}


def check_case(latest, case, vote, reference_path=None):
    selected = {(provider, model): row for (q, provider, model), row in latest.items()
                if q == case and (provider, model) in PANEL_5}
    if not selected:
        raise ValueError("No panel trace for " + case)
    proposals = [ballot(provider, model, selected.get((provider, model)))
                 for provider, model in PANEL_5]
    results = {"2-of-3": vote(None, proposals[:3], 2),
               "3-of-5": vote(None, proposals, 3)}

    # Reference checking happens after voting, never inside the ballot.
    references = {int(row["reference"]) for row in selected.values()
                  if row["reference"].strip()}
    if len(references) != 1:
        raise ValueError("Missing or inconsistent trace reference for " + case)
    reference = references.pop()
    source = "reference column of traces-td1.csv"
    if reference_path is not None:
        with reference_path.open(encoding="utf-8-sig", newline="") as stream:
            matches = [row for row in csv.DictReader(stream)
                       if row.get("case_id", "").strip() == case]
        if len(matches) != 1 or int(matches[0]["revenue_cents"]) != reference:
            raise ValueError("Reference file missing, duplicated or different for " + case)
        source = reference_path.name + " (compared with the trace reference)"
    for result in results.values():
        result["matches_reference"] = (result["value"] == reference
                                       if result["consensus"] else None)
    return {"case_id": case, "reference": reference, "reference_source": source,
            "ballots": proposals, "results": results,
            "faulty_queries": [
                {"provider": row["provider"], "model": row["model_requested"],
                 "value": int(row["value"]), "sql": row["sql"]}
                for row in selected.values()
                if row["verdict"] == "incorrect" and row["value"].strip()
            ]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--traces", type=Path, default=HERE / "traces-td1.csv")
    parser.add_argument("--skeleton", type=Path,
                        default=HERE / "skeleton-multi-llm-en.py")
    parser.add_argument("--case", help="Default: first shared wrong case in the real traces")
    parser.add_argument("--reference", type=Path,
                        help="Optional TD 1 reference CSV (case_id, revenue_cents)")
    parser.add_argument("--output", type=Path, help="Save the evidence as JSON")
    args = parser.parse_args()
    try:
        rows, real, latest = read_traces(args.traces)
        candidates = shared_wrong(real)
        if not candidates:
            print("No shared wrong value in the real traces: use DEMO-SQL-C11.")
            return
        for group in candidates:
            print(group["case_id"], "value", group["wrong_value"], "models", group["models"])
        case = args.case or candidates[0]["case_id"]
        vote = load_shared_vote(args.skeleton)
        result = check_case(latest, case, vote, args.reference)
        result.update({
            "trace_rows": len(rows), "real_rows": len(real), "latest_cells": len(latest),
            "search_all_attempts": candidates,
            "search_latest_attempts": shared_wrong(latest.values()),
            "mode": "real traces; Pair A source method executed in isolation",
            "trace_sha256": hashlib.sha256(args.traces.read_bytes()).hexdigest(),
            "vote_source_sha256": hashlib.sha256(args.skeleton.read_bytes()).hexdigest(),
        })
        text = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(text, encoding="utf-8")
        print(text, end="")
    except (OSError, ValueError, KeyError, SyntaxError, NotImplementedError) as error:
        parser.exit(1, "Part 2 check failed: " + str(error) + "\n")


if __name__ == "__main__":
    main()
