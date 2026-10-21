# TD 1 — Model C experimental results

**Subgroup:** GRAMSCAR  
**Course pack:** `2026-10-18-students-1`  
**Session:** 21 October 2026  
**Provider:** OpenRouter  
**Model requested and returned:** `cohere/north-mini-code:free`  
**Run:** 21 October 2026, 13:47:45–13:50:55 UTC  
**Nature:** Real API calls (no simulation or replay in these 20 results)

## Evidence

- [Raw state: `state-C.jsonl`](../state-C.jsonl)
- [Exported traces: `traces-C.csv`](../traces-C.csv)
- [SQL reference key: `reference-td1.csv`](../reference-td1.csv)

All 20 questions C01–C20 were run exactly once for Model C in this exported state (the `attempts` field is 1 for every case). All returned HTTP 200. The generated SQL was evaluated and compared with the course database's reference values. The model's numerical outputs are **not** used as independent references.

## Observed results

| Metric | Result |
|---|---:|
| Questions attempted | 20 / 20 |
| Correct | 12 |
| Incorrect numerical result | 8 |
| API/request errors | 0 |
| SQL rejections | 0 |
| Accuracy across all questions | **12/20 (60%)** |
| Mean recorded latency | 2,393 ms |
| Median recorded latency | 2,319 ms |
| Prompt tokens (recorded) | 11,194 |
| Completion tokens (recorded) | 2,885 |
| Sum of recorded prompt + completion tokens | 14,079 |
| Provider-reported native cost field | 0 for each result |

**Correct:** C01, C03, C04, C05, C06, C07, C12, C13, C14, C15, C16, C20.  
**Incorrect:** C02, C08, C09, C10, C11, C17, C18, C19.

A notable pattern in this run: **all 10 questions without a customer-age filter were correct**, while **only 2 of 10 age-related questions (C15 and C16) were correct**. This is an observed association for this specific run, not a claim that age is the only cause of failure.

## Incorrect cases and inspection of generated SQL

| Case | Model value (cents) | Reference (cents) | Observation from the saved SQL |
|---|---:|---:|---|
| C02 | 0 | 590,320 | Adds an order-date filter restricting sales to 25 September, despite the question asking for all orders of customers aged 25 on that reference date |
| C08 | 2,826,250 | 605,580 | Age logic compares birthday month/day to the reference date without properly restricting birth year |
| C09 | 1,901,780 | 487,980 | Age logic allows customers aged at least 25, rather than exactly 25 |
| C10 | 0 | 558,980 | The calculation adds the birth year to a birthday adjustment instead of subtracting it from the order year |
| C11 | 0 | 446,690 | Contradictory birth-date boundaries (`<= '2026-11-01'` and `> '2026-12-02'`) exclude everyone |
| C17 | 197,080 | 258,180 | The birthday comparison concatenates a birth month with a birth **year**, producing a malformed month-day expression |
| C18 | 147,810 | 62,480 | Age filter lacks a matching upper age bound and can include orders from older customers |
| C19 | 71,640 | 1,990 | Age calculation uses incomplete birth-year logic and includes customers outside the exact-25-year age range |

The observations in the last column are based on the actual generated SQL in `traces-C.csv`; detailed causal explanations should be reviewed against the database before using them as definitive claims about every affected row.

## Limits and next steps

- This is one run of one model on this fixed course dataset; it does not establish general model accuracy.
- All responses in this file are genuine recorded outputs, including mistakes. No unsuccessful cases were silently corrected or re-run.
- Other operators' model results should be combined in the subgroup's `model-question-comparison-en.csv` and `five-model-summary-en.csv`.
- Incorporate these observations, division of work, independent reference checks, and any provider-access limitations in the final `reports/td1.md`. The group's full hand-in is **not** completed by this Model C report alone.
