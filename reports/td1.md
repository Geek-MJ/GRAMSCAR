# TD 1 — Comparing models on the same questions

**Date:** 21 October 2026  
**Repository:** [Geek-MJ/GRAMSCAR](https://github.com/Geek-MJ/GRAMSCAR)  
**Status:** Partial experiment; full five-model, twenty-question benchmark is not yet complete.

## Work completed

I checked the TD1 preparation evidence in `ready-for-td1.txt`. Python, the SQLite database and its CSV fingerprints matched the kit manifest, and all five required model access checks were successful.

I independently computed and cross-checked the reference SQL values for C05 and C08 and saved them in `reference-td1.csv`:

| Case | Question | Reference value (euro cents) |
|---|---|---:|
| C05 | Revenue for orders placed from 2026-06-01 00:00:00 (inclusive) to 2026-06-02 00:00:00 (exclusive) | 38480 |
| C08 | Revenue from all orders belonging to customers exactly 25 years old on 2026-09-24 | 605580 |

The values are expressed in euro cents, excluding VAT, following the TD1 conventions.

## Model experiments and results

I ran the same two reference-checked questions with the authorised skeleton script, using a three-second pause and separate state and trace files per model.

| Model / access route | C05 | C08 | Result on this two-case test |
|---|---:|---:|---:|
| `groq:openai/gpt-oss-120b` | 38480 — correct | 605580 — correct | 2/2 correct (100%) |
| `openrouter:cohere/north-mini-code:free` | 38480 — correct | 0 — incorrect | 1/2 correct (50%) |

Across these four model-question cells, three results matched the reference and one did not. These small-sample percentages describe only C05 and C08; they are not a ranking of the models or evidence of performance on the other eighteen questions.

### Observed failure: Cohere on C08

The recorded SQL in `traces-openrouter.csv` used this date filter:

```sql
WHERE c.birth_date <= '2026-09-24'
  AND c.birth_date > date('2026-09-24', '-26 years')
  AND date('2026-09-24') >= o.date
  AND date('2026-09-24') < date(o.date, '+1 day');
```

Two problems explain the mismatch:

1. The birth-date interval does not implement the completed-age convention correctly. For someone exactly 25 on 2026-09-24, the corresponding birth-date range is after 2000-09-24 and up to and including 2001-09-24.
2. The query restricts orders to the reference date. C08 asks for **all orders** belonging to eligible customers, so an order-date restriction should not be applied.

The reference-matching SQL logic is:

```sql
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers AS c
JOIN orders AS o ON o.customer_id = c.customer_id
JOIN product AS p ON p.product_id = o.product_id
WHERE c.birth_date > '2000-09-24'
  AND c.birth_date <= '2001-09-24';
```

This is an explanation of the failure, not a replacement for the model's original trace. The original model output and verdict are retained unchanged.

## Evidence files

The following files were generated locally by the runs:

- `reference-td1.csv` — checked reference queries and values for the assigned questions C05 and C08.
- `state-groq.jsonl` and `traces-groq.csv` — two real Groq attempts/results for GPT-OSS 120B.
- `state-openrouter.jsonl` and `traces-openrouter.csv` — two real OpenRouter attempts/results for Cohere North Mini Code.
- `ready-for-td1.txt` — saved prerequisite and model access-check output.

These trace/state files are currently local and are not part of this report commit unless added separately.

## Limitations

- Only C05 and C08 have reference values and model results recorded in the work described here.
- Only two of the five required models have been run, and only on these two questions.
- `model-question-comparison-en.csv` and `five-model-summary-en.csv` have not yet been completed from a consolidated set of all required traces.
- This run does not provide a full model portfolio ranking or measured benchmark-wide cost comparison.
- The original trace records one attempt per cell. No retries were needed for these four cells.

## Next steps

1. Coordinate with the subgroup to complete the remaining assigned question references and the model batches for all five required models, following the one-request-at-a-time, three-second pause and retry/state-file rules.
2. Preserve every model's raw CSV and JSONL trace files; consolidate raw CSV records under one header into `traces-td1.csv`.
3. Complete `model-question-comparison-en.csv` with one final row per model/question, accurate trace pointers and evidence-based failure explanations.
4. Complete `five-model-summary-en.csv` using the supplied portfolio sources and documented prices/index values; mark unavailable measurements as N/A or empty as the template/instructions require.
5. Review the final submission artefacts with the subgroup before submitting the repository URL, full commit hash and report link on Moodle.

## Contribution recorded in this report

I checked and cross-validated the C05 and C08 reference values, ran the two authorised models on both questions, retained their state and trace files, and analysed the Cohere C08 failure from the recorded SQL. The larger group benchmark and consolidation remain in progress.
