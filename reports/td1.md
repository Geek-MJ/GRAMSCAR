# TD 1 — Comparing models on the same questions

**Date:** 21 October 2026  
**Repository:** [Geek-MJ/GRAMSCAR](https://github.com/Geek-MJ/GRAMSCAR)  
**Status:** Five required models tested on C05 and C08; the full twenty-question benchmark is not complete.

## Work completed

I checked the TD1 preparation evidence in `ready-for-td1.txt`. Python, the SQLite database and its CSV fingerprints matched the kit manifest, and all five required model access checks were successful.

I independently computed and cross-checked reference SQL values for C05 and C08 and saved them in `reference-td1.csv`:

| Case | Question | Reference value (euro cents) |
|---|---|---:|
| C05 | Revenue for orders placed from 2026-06-01 00:00:00 (inclusive) to 2026-06-02 00:00:00 (exclusive) | 38480 |
| C08 | Revenue from all orders belonging to customers exactly 25 years old on 2026-09-24 | 605580 |

The values are expressed in euro cents, excluding VAT, following the TD1 conventions.

## Model experiments and results

I ran the same reference-checked questions with all five authorised models using the provided skeleton. Each model was run with a three-second pause and a separate state and trace file.

| Model / access route | C05 | C08 | Results on these two cases |
|---|---:|---:|---:|
| `groq:openai/gpt-oss-120b` | 38480 — correct | 605580 — correct | 2/2 correct (100%) |
| `groq:openai/gpt-oss-20b` | 38480 — correct | 605580 — correct | 2/2 correct (100%) |
| `openrouter:cohere/north-mini-code:free` | 38480 — correct | 0 — incorrect | 1/2 correct (50%) |
| `groq:qwen/qwen3.8-27b` | 38480 — correct | 605580 — correct | 2/2 correct (100%) |
| `openrouter:dots-studio/dots-3-note-preview:free` | 38480 — correct | 25920 — incorrect | 1/2 correct (50%) |

Across the ten model-question cells, eight results matched the reference (80%). All five models answered C05 correctly. Three of the five models answered C08 correctly. These percentages describe only C05 and C08; they are not a ranking or evidence of performance on the other eighteen questions.

The comparison records are in [`model-question-comparison-en.csv`](../model-question-comparison-en.csv). Each row records the case, model ID, source trace filename, cell ID, nature, status, returned value, reference value and explanation.

## Observed failure: Cohere on C08

The recorded SQL in `traces-openrouter.csv` used this filter:

```sql
WHERE c.birth_date <= '2026-09-24'
  AND c.birth_date > date('2026-09-24', '-26 years')
  AND date('2026-09-24') >= o.date
  AND date('2026-09-24') < date(o.date, '+1 day');
```

Two problems explain the mismatch:

1. The birth-date interval does not implement the completed-age convention correctly. For someone exactly 25 on 2026-09-24, the birth-date range is after 2000-09-24 and up to and including 2001-09-24.
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

This explains the failure; it does not replace the model's original SQL or result. The original trace is retained.

## Observed failure: Dots on C08

Dots returned 25920 against the reference value 605580. This row is marked incorrect in the comparison CSV. The SQL should be inspected in `traces-dots.csv` before assigning a more specific cause; the cause has not been confirmed in this report.

## Evidence files

The run produced these local evidence files:

- `reference-td1.csv` — reference queries and values for C05 and C08.
- `state-groq.jsonl` and `traces-groq.csv` — GPT-OSS 120B state and trace.
- `state-gptoss20b.jsonl` and `traces-gptoss20b.csv` — GPT-OSS 20B state and trace.
- `state-openrouter.jsonl` and `traces-openrouter.csv` — Cohere state and trace.
- `state-qwen.jsonl` and `traces-qwen.csv` — Qwen state and trace.
- `state-dots.jsonl` and `traces-dots.csv` — Dots state and trace.
- `ready-for-td1.txt` — saved prerequisite and access-check output.
- [`model-question-comparison-en.csv`](../model-question-comparison-en.csv) — committed comparison rows for all ten model-question cells.

**Note:** the JSONL state files and raw trace CSVs listed above are currently on the local machine; they have not been committed to this repository yet. The comparison CSV points to their filenames. Keep the files unchanged so the raw evidence is preserved.

## Limitations

- Only C05 and C08 have been evaluated across all five models. The other eighteen questions have not been tested in this batch.
- The comparison CSV is a ten-row partial comparison, not the full required twenty-question matrix.
- `five-model-summary-en.csv` has not yet been completed from the full benchmark and documented portfolio data.
- Dots' C08 failure is confirmed by the returned value, but its precise SQL-level cause still needs trace inspection.
- Each of the ten cells completed in one attempt; no retries were needed.
- This two-question sample does not support a general model ranking or a benchmark-wide cost conclusion.

## Next steps

1. Inspect `traces-dots.csv` and record a SQL-grounded cause for Dots' C08 mismatch.
2. Complete and cross-check the references and model runs for the remaining questions with the subgroup, following the one-request-at-a-time, three-second pause and retry/state-file rules.
3. Preserve raw trace CSVs and JSONL states; consolidate all raw CSV records under one header into `traces-td1.csv`, retaining every attempt and keeping real, replayed and simulated rows distinct.
4. Extend `model-question-comparison-en.csv` to one final row per model/question using the last attempt and accurate trace pointers.
5. Complete `five-model-summary-en.csv` using the supplied portfolio and documented index/price sources, with missing measurements recorded as instructed.
6. Submit the repository URL, full commit hash and report link on Moodle as specified by the course.

## Contribution recorded in this report

I checked and cross-validated the C05 and C08 reference values, ran all five authorised models on both questions, retained separate state and trace files per model, compared the outputs against the references, and analysed Cohere's C08 failure from the recorded SQL.
