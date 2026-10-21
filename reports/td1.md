# TD 1 — Comparing five models on the same SQL questions

**Group:** DIA2_3 (GRAMSCAR)  
**Class:** DIA2  
**Date:** 21 October 2026  
**Pack:** `2026-10-18-students-1`

## What we did

We calculated SQL references for the same 20 revenue questions, using the course database and its conventions: prices in euro cents excluding VAT, periods inclusive at the start and exclusive at the end, and completed age on the specified date. The 20 answers in [`reference-td1.csv`](../reference-td1.csv) match the course answer key. Independent checks by another member still need to be attributed in the final submission.

We ran the five proposed models with the common prompts from the course skeleton. We kept the SQL they produced and the associated verdicts, latencies, token counts and errors. The current trace files hold 98 real API attempts covering 96 distinct model/question cells. Two attempts received HTTP 429 and were followed by successful requests; no simulated or replayed responses are included.

## Experiment results

| Model | Recorded | Correct | Incorrect | Invalid SQL | Accuracy on recorded cells |
|---|---:|---:|---:|---:|---:|
| A — `groq:openai/gpt-oss-120b` | 20/20 | 19 | 1 | 0 | 95% |
| B — `groq:openai/gpt-oss-20b` | 16/20 | 14 | 2 | 0 | 87.5% |
| C — `openrouter:cohere/north-mini-code:free` | 20/20 | 12 | 8 | 0 | 60% |
| D — `groq:qwen/qwen3.8-27b` | 20/20 | 16 | 4 | 0 | 80% |
| E — `openrouter:dots-studio/dots-3-note-preview:free` | 20/20 | 13 | 6 | 1 | 65% |

**Coverage:** 96 of the planned 100 model/question cells, from 98 real recorded attempts. The latest result per cell gives 74 correct answers, 21 incorrect numerical results and one invalid SQL query. There were also two HTTP 429 events before one permitted retry each (D, C19 and C20). These earlier attempts are kept in the raw traces.

**Missing:** Model B on C05–C08. These four cells remain `not_executed` in the comparison; they are not counted as wrong answers.

## Models × questions — view of the comparison CSV

✓ correct · × incorrect value · SQL invalid query · — not executed. Each cell is the latest recorded verdict, not a second manually maintained result.

| Model | C01 | C02 | C03 | C04 | C05 | C06 | C07 | C08 | C09 | C10 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| B | ✓ | × | ✓ | ✓ | — | — | — | — | ✓ | ✓ |
| C | ✓ | × | ✓ | ✓ | ✓ | ✓ | ✓ | × | × | × |
| D | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| E | ✓ | × | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | × | × |

| Model | C11 | C12 | C13 | C14 | C15 | C16 | C17 | C18 | C19 | C20 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| A | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | × | ✓ |
| B | × | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| C | × | ✓ | ✓ | ✓ | ✓ | ✓ | × | × | × | ✓ |
| D | ✓ | ✓ | ✓ | ✓ | × | × | × | ✓ | × | ✓ |
| E | ✓ | ✓ | ✓ | ✓ | × | × | SQL | × | ✓ | ✓ |


## What the traces show

The simplest period-only calculations generally worked. The most frequent failures came from the age condition, especially the requirement to be **exactly** 25 on a reference date or on the order date.

- **A:** C19 selects only one birth date instead of the full interval of customers who are 25 on 25 September 2026.
- **B:** C02 uses a 2025–2026 birth-date interval, and C11 includes birth years outside the exact-age range.
- **C:** C02 adds an unwanted order-date filter. C08–C11, C17–C19 contain different mistakes in birth-year, birthday, or completed-age calculations. C15 and C16 nevertheless work.
- **D:** The first ten results are correct. C15–C17 and C19 returned incorrect values because of age filtering; C19 and C20 each had an earlier HTTP 429 event, followed by a permitted second attempt.
- **E:** The wrong values in C02, C09, C10, C15, C16 and C18 relate to age filtering. C17 has invalid SQL (`syntax error near "AS"`), unlike an incorrect numerical result.

These explanations are based on the generated SQL and the error fields, not a claim that the model always behaves this way. Each individual case is linked in [`model-question-comparison-en.csv`](../model-question-comparison-en.csv) to its original trace.

## Part 3 — Selected trace analysis

The cases below were selected from the group's recorded results to show the different outcomes in the TD 1 protocol. They are not claimed to be an instructor-selected set. We examined the actual generated SQL, reference value, HTTP status, prompt hash and available token/latency measurements.

| Model / case | Observed outcome | Technical explanation |
|---|---|---|
| B / C02 | HTTP 200, incorrect: **0** instead of **590,320** cents | The SQL filters birthdays between September 2025 and September 2026 rather than the correct 25-year-old birth-date range. This is a semantic SQL error, not a provider failure. |
| C / C08 | HTTP 200, incorrect: **2,826,250** instead of **605,580** cents | The generated age condition compares birthday month and day without enforcing the correct birth year; it includes customers outside the intended age group. |
| E / C17 | HTTP 200, **`sql_invalid`** (SQLite syntax error near `AS`) | The generated `CAST` expression has misplaced parentheses. The API response succeeded, but SQLite could not execute the SQL. There is no numerical result to compare with **258,180** cents. |
| D / C19 | First attempt **HTTP 429**, then HTTP 200 with incorrect **83,580** instead of **1,990** cents | The first call hit the Groq output-token rate limit and has no SQL or reported token counts. The retry produced runnable SQL but used a faulty exact-age filter. |
| D / C20 | First attempt **HTTP 429**, then HTTP 200, correct **1,106,090** cents | A second attempt after the temporary provider limit generated SQL matching the reference. Both attempts are retained; only the later result is the final result for this model/question. |

**Measurements and missing fields:** B/C02 took 863.5 ms, with 632 prompt and 378 completion tokens recorded. C/C08 took 4,472.3 ms (551 prompt, 415 completion tokens). E/C17 took 3,547.2 ms (626 prompt, 227 completion tokens), despite the invalid SQL. For D/C19 the rate-limited first attempt took 64.3 ms, and its prompt/completion token fields are empty; the second attempt took 903.5 ms (659 prompt, 251 completion tokens). D/C20 similarly had an 81.8 ms HTTP 429 response without token measurements and a 355 ms successful second attempt (630 prompt, 95 completion tokens). An empty measurement is not the same as zero.

**Common prompt fingerprint:** The TD 1 skeleton hashes the exact system and user messages for each question using SHA-256. For C19, both A and D recorded the same `prompt_sha256` (`e5396619f946e273f11d2baf48666f84d8a817fde9f7189579c96ce2c2a14119`). The C19 retry kept that same fingerprint. Across the available data, each question's fingerprint is consistent between models. The request wording was therefore held constant; differences arise from model output and access conditions, not from deliberately changing the prompt.

The original source records for these examples can be found in [`state-B.jsonl`](../state-B.jsonl), [`state-C.jsonl`](../state-C.jsonl), [`state-E-C11-20.jsonl`](../state-E-C11-20.jsonl) and [`state-D-C11-C20.jsonl`](../state-D-C11-C20.jsonl). The matching CSVs keep the generated SQL and identifiers. C19 and C20 are examples of the allowed single retry; there is no evidence here of a permanent authentication or access denial.

## Files and reproducibility evidence

- [`reference-td1.csv`](../reference-td1.csv): our 20 SQL reference queries and values.
- [`traces-td1.csv`](../traces-td1.csv) and [`traces-td1.jsonl`](../traces-td1.jsonl): all 98 real API attempts (96 latest results plus two retained HTTP 429 first attempts). Missing measurements remain blank.
- [`model-question-comparison-en.csv`](../model-question-comparison-en.csv): one latest-result row for each of the 100 planned cells, including missing cases and trace pointers.
- [`five-model-summary-en.csv`](../five-model-summary-en.csv): observed results by overlapping period, age, product and combined families, with access routes, dated public indices and documented exact-model paid prices when available. Where not documented, values are N/A with reasons.
- [`prompts-en.md`](../prompts-en.md): the unchanged system prompt and user template from the course skeleton. Recorded prompt SHA-256 hashes agree across models for a given question.
- [`modeles-autorises.json`](../modeles-autorises.json): the authorized provider/model pairs and their parameters from the course kit.
- Original source CSVs and state JSONL files are kept in the repository, so the merged file is not the only evidence.

The model-family scores overlap because some questions use several types of filter. For comparison, the price figures are the paid route of the exact model, *not* the cost paid by this sub-group: all recorded runs used free access. Sources and access dates are in the five-model CSV.

## Limitations and decisions

We used the latest observed result per available model/question cell, so these results describe this small dataset and prompt rather than the general quality of a model. Two D cells had an HTTP 429 response before the second attempt; their first attempts remain in the original and merged traces. Measurements unavailable on rate-limited attempts remain blank. The original orchestration script is now tracked in the repository. The SHA-256-checked `bootstrap_td1.py` restores the official runtime from the student pack, and offline replay was locally verified on the 20 Model C records (12/20 correct, matching the original score). Another member should still run the README commands from a fresh clone.

The missing four B cells (C05–C08) must be supplied as original traces by the assigned operator, or clearly identified as instructor-provided historical/replayed data if the instructor authorizes that route. They cannot be silently substituted with generated results.

## Contributions

Cyril Ibrahim ran Model C on C01–C20 and recorded the original CSV and JSONL results. The shared repository contains contributions for the SQL references and models A, B, D and E. The final report still needs the group to confirm who performed each allocation and who independently checked each SQL reference; these roles cannot be determined reliably from the filenames.

AI assistance was used to consolidate the existing experiment data, prepare the comparative tables and draft this report. The original model outputs were not altered to improve scores. The sub-group remains responsible for reviewing the files and explanations.

## Next steps

Complete and upload B's C05–C08 traces, then refresh the merged trace files and both summaries. Confirm individual contributions and independent reference checks, and test reproduction from a fresh clone. Then update the README with the commands, verify the public repository, and submit its final commit hash and this report's commit-specific link on Moodle before **25 October 2026, 23:59 (Paris time)**.
