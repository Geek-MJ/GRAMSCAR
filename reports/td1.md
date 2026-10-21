# TD 1 — Comparing five models on the same SQL questions

**Group:** DIA2_3 (GRAMSCAR)  
**Class:** DIA2  
**Date:** 21 October 2026  
**Pack:** `2026-10-18-students-1`

## What we did

We calculated SQL references for the same 20 revenue questions, using the course database and its conventions: prices in euro cents excluding VAT, periods inclusive at the start and exclusive at the end, and completed age on the specified date. The 20 answers in [`reference-td1.csv`](../reference-td1.csv) match the course answer key. Independent checks by another member still need to be attributed in the final submission.

We ran the five proposed models with the common prompts from the course skeleton. We kept the SQL they produced and the associated verdicts, latencies, token counts and errors. All 86 recorded answers are real API calls; there are no simulated or replayed responses in these files.

## Experiment results

| Model | Recorded | Correct | Incorrect | Invalid SQL | Accuracy on recorded cells |
|---|---:|---:|---:|---:|---:|
| A — `groq:openai/gpt-oss-120b` | 20/20 | 19 | 1 | 0 | 95% |
| B — `groq:openai/gpt-oss-20b` | 16/20 | 14 | 2 | 0 | 87.5% |
| C — `openrouter:cohere/north-mini-code:free` | 20/20 | 12 | 8 | 0 | 60% |
| D — `groq:qwen/qwen3.8-27b` | 10/20 | 10 | 0 | 0 | 100.0% |
| E — `openrouter:dots-studio/dots-3-note-preview:free` | 20/20 | 13 | 6 | 1 | 65% |

**Coverage:** 86 of the planned 100 model/question cells. Among the recorded calls, 68 were correct, 17 returned a wrong value and one generated invalid SQL. All 86 are labelled `nature=real`; no access failures are recorded.

**Missing:** Model B on C05–C08 and Model D on C11–C20. These 14 cells are marked `not_executed` in the comparison, not treated as wrong answers. We must not interpret D's 10/10 as a final result for all 20 questions.

## What the traces show

The simplest period-only calculations generally worked. The most frequent failures came from the age condition, especially the requirement to be **exactly** 25 on a reference date or on the order date.

- **A:** C19 selects only one birth date instead of the full interval of customers who are 25 on 25 September 2026.
- **B:** C02 uses a 2025–2026 birth-date interval, and C11 includes birth years outside the exact-age range.
- **C:** C02 adds an unwanted order-date filter. C08–C11, C17–C19 contain different mistakes in birth-year, birthday, or completed-age calculations. C15 and C16 nevertheless work.
- **D:** All 10 recorded questions are correct, but half the assigned batch is missing.
- **E:** The wrong values in C02, C09, C10, C15, C16 and C18 relate to age filtering. C17 has invalid SQL (`syntax error near "AS"`), unlike an incorrect numerical result.

These explanations are based on the generated SQL and the error fields, not a claim that the model always behaves this way. Each individual case is linked in [`model-question-comparison-en.csv`](../model-question-comparison-en.csv) to its original trace.

## Files and reproducibility evidence

- [`reference-td1.csv`](../reference-td1.csv): our 20 SQL reference queries and values.
- [`traces-td1.csv`](../traces-td1.csv) and [`traces-td1.jsonl`](../traces-td1.jsonl): all 86 recorded real calls, with missing measurements left blank.
- [`model-question-comparison-en.csv`](../model-question-comparison-en.csv): one latest-result row for each of the 100 planned cells, including missing cases and trace pointers.
- [`five-model-summary-en.csv`](../five-model-summary-en.csv): observed results by overlapping period, age, product and combined families, with access routes, dated public indices and documented exact-model paid prices when available. Where not documented, values are N/A with reasons.
- [`prompts-en.md`](../prompts-en.md): the unchanged system prompt and user template from the course skeleton. Recorded prompt SHA-256 hashes agree across models for a given question.
- [`modeles-autorises.json`](../modeles-autorises.json): the authorized provider/model pairs and their parameters from the course kit.
- Original source CSVs and state JSONL files are kept in the repository, so the merged file is not the only evidence.

The model-family scores overlap because some questions use several types of filter. For comparison, the price figures are the paid route of the exact model, *not* the cost paid by this sub-group: all recorded runs used free access. Sources and access dates are in the five-model CSV.

## Limitations and decisions

We used one recorded run per available model/question cell, so these results describe this small dataset and prompt rather than the general quality of a model. There are no retries in the present 86 records, and the recorded `attempts` field is 1. Free-provider rate limits may affect future reruns. The exact reproduction commands and runnable source files still need to be brought together for a fresh-clone test.

The missing 14 cells must be supplied as original traces by the assigned operators, or clearly identified as instructor-provided historical/replayed data if the instructor authorizes that route. They cannot be silently substituted with generated results.

## Contributions

Cyril Ibrahim ran Model C on C01–C20 and recorded the original CSV and JSONL results. The shared repository contains contributions for the SQL references and models A, B, D and E. The final report still needs the group to confirm who performed each allocation and who independently checked each SQL reference; these roles cannot be determined reliably from the filenames.

AI assistance was used to consolidate the existing experiment data, prepare the comparative tables and draft this report. The original model outputs were not altered to improve scores. The sub-group remains responsible for reviewing the files and explanations.

## Next steps

Complete and upload B's C05–C08 and D's C11–C20 traces, refresh the two merged trace files and two summaries, confirm individual contributions and independent reference checks, and test reproduction from a fresh clone. Then update the README with the commands, verify the public repository, and submit its final commit hash and this report's commit-specific link on Moodle before **25 October 2026, 23:59 (Paris time)**.
