"""Part 2B - k-of-n vote on one TD 1 question, using each model's last attempt.

Usage: python3 vote_2b.py traces-td1.csv C02

Rules:
- one ballot per model = its last attempt on the question (highest `attempts`)
- a model with an error / empty value stays in n but casts no vote
- a value wins if it gets at least k votes; otherwise there is no decision
"""
import csv
import sys
from collections import Counter

PANEL = ["openai/gpt-oss-120b", "cohere/north-mini-code:free", "qwen/qwen3.8-27b"]
ALL5 = PANEL + ["openai/gpt-oss-20b", "dots-studio/dots-3-note-preview:free"]


def norm(v):
    v = (v or "").strip()
    try:
        f = float(v)
        return str(int(f)) if f == int(f) else str(f)
    except ValueError:
        return v


def last_attempts(path, case_id):
    last = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["case_id"] != case_id:
                continue
            m = r["model_requested"]
            if m not in last or int(r["attempts"] or 0) >= int(last[m]["attempts"] or 0):
                last[m] = r
    return last


def vote_k_sur_n(ballots, members, k):
    """ballots: {model: value or None}. Returns (winner or None, Counter, n)."""
    votes = Counter(ballots[m] for m in members if ballots.get(m) not in (None, ""))
    n = len(members)
    winners = [v for v, c in votes.items() if c >= k]
    return (winners[0] if len(winners) == 1 else None), votes, n


def main(path, case_id):
    last = last_attempts(path, case_id)
    ballots = {}
    print(f"Ballots for {case_id} (last attempt per model)")
    for m in ALL5:
        r = last.get(m)
        if r is None:
            ballots[m] = None
            print(f"  {m:40s} MISSING (counts in n, no vote)")
            continue
        val = norm(r["value"]) if r["verdict"] in ("correct", "incorrect") else None
        ballots[m] = val
        print(f"  {m:40s} value={val!s:10s} verdict={r['verdict']:10s} "
              f"attempts={r['attempts']} ref={r['reference']}")
    ref = norm(next(iter(last.values()))["reference"])
    for label, members, k in (("2-of-3 panel", PANEL, 2), ("3-of-5 quorum", ALL5, 3)):
        winner, votes, n = vote_k_sur_n(ballots, members, k)
        verdict = ("no decision" if winner is None
                   else "CORRECT" if winner == ref else "WRONG")
        print(f"\n{label}: k={k}, n={n}, votes={dict(votes)} -> "
              f"{winner if winner is not None else 'none'} ({verdict}; reference {ref})")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])