# TD2 — Person 3: Routing simulator implementation

## Status
This simulator has been **adapted to Person 2's WhatsApp routing decisions**. The professor's original `atelier-routage.py` is **not included** in the supplied GRAMSCAR ZIP, so this is a standalone substitute, not an edit of the professor's code. Its seven scenarios, capacity numbers, refill times, and subscription route examples are synthetic. It makes no API calls. Do **not** label these as the original professor's before/after outputs.

## How to run
Extract this folder with `GRAMSCAR-main` alongside the script and run:

```bash
python3 atelier-routage-person3.py
python3 atelier-routage-person3.py --scenario deferrable
python3 atelier-routage-person3.py --scenario deferrable --prefer-wait
```

## Person 2 routing choices implemented
- F1: GPT-OSS-20B, 6/6 (100%).
- F2: GPT-OSS-120B, 4/4 (100%).
- F2b: GPT-OSS-20B, 2/2 (100%), provisionally selected among tied models.
- F3: GPT-OSS-20B, 4/4 (100%).
- Combinations: GPT-OSS-20B, 4/4 (100%).

The source `five-model-summary-en.csv` combines F2 and F2b as `age_results`. The separate F2/F2b figures are taken from Person 2's message and should be cross-checked with Person 1's exact question IDs before submission. Other candidates for F2/F2b are **not** assigned invented family scores.

## RESOURCES
`load_models()` loads five real model identities and TD1 summary evidence from the GRAMSCAR CSVs. It adds Person 2's family scores and preference. `configure()` creates illustrative quota, refill and subscription capacity conditions. The simulation's `route='subscription'` flags are hypothetical: they are not proof that the corresponding exact-model subscription is available or purchased. No actual prices or quota balances are inferred.

## choose()
1. Consider only models with supported TD1 accuracy evidence for the requested family.
2. Prefer Person 2's family model; use eligible alternatives as fallback.
3. Internal dashboard: `none` only for an available **free** route with 100% observed accuracy on that family; otherwise 3-of-5 quorum or deterministic validation.
4. Customer-facing: 3-of-5 quorum or deterministic validation regardless of accuracy.
5. Payout: deterministic SQL validation or human review regardless of accuracy.
6. Use eligible free allocation now; otherwise default to available included subscription capacity now; otherwise defer to eligible free refill within deadline; otherwise abstain.
7. `--prefer-wait` reverses subscription-before-defer when a task can wait and conserving subscription allocation is valuable.

**Important:** `run` only selects a route; it does not perform quorum, SQL validation or review. The verification requirement must be enforced by a real downstream service before returning consequential results.

## Seven illustrative scenario outcomes
See `scenario-results.txt` for exact locally executed results. The cases are: free_ready, subscription_ready, deferrable, deadline_too_soon, customer_checked, payout_checked, all_unavailable. The `deferrable` example demonstrates the priority reversal; see `wait-priority-example.txt`.

## Why subscription before deferral?
An included subscription route with `cash == 0` and `allocation > 0` can run immediately, while a free route with `allocation == 0` must wait for refill. The supplied priority favors latency and immediate completion. If the task is nonurgent, its deadline exceeds the free refill time, and subscription allocation is scarce, waiting for free quota can be preferable. Neither route should be selected if it is ineligible for the family or cannot satisfy the required verification.

## Remaining requirements for official hand-in
- Obtain original `atelier-routage.py`, capture its seven **unaltered** outputs, then transplant this policy into its `RESOURCES` and `choose()` preserving its interface.
- Verify F2/F2b question IDs and per-model scores against Person 1's table.
- Confirm F2b price tie and any actual paid/subscription routes with the dated portfolio.
- Capture the instructor simulator's seven **modified** outputs and compare them to the original.
