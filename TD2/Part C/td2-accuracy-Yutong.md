# TD2 Accuracy Analysis — Person 1 Deliverable

**Source data:** `traces-td1.csv` (100 executed cells, 5 models × 20 questions C01–C20) cross-checked against `reference-td1.csv` (20 reference answers).
**Dedup rule:** 100 unique `cell_id`. Two cells had `attempts = 2` (qwen3.8-27b, C19 and C20); the **final attempt** is used for the verdict, as required by the TD1 protocol.
**Statistical caveat:** 4–6 questions per family only support a **batch-specific hypothesis**, not a general error rate or a permanent model ranking.

## 1. Family definition (exact question IDs)

| Family | Convention involved | Case IDs | Count |
|---|---|---|---|
| **F1** — Period | Pure time window, boundaries `>=` start / `<` end | C01, C04, C05, C06, C07, C20 | 6 |
| **F2** — Completed age at a date | "exactly 25 years old **on the reference date** Y" → age reached at that date | C02, C08, C09, C11 | 4 |
| **F2b** — Age at the order | "exactly 25 years old **at the time of the order**" → age at the order date, not at a reference date | C10, C18 | 2 |
| **F3** — Product list | Products designated as a/b/c/d (ordinal positions in the product list), optionally with a period | C03, C12, C13, C14 | 4 |
| **Combinations** | Two or more conventions stacked: period + age, product + age, product + period + age | C15, C16, C17, C19 | 4 |

Total: 6 + 4 + 2 + 4 + 4 = **20**. Every case is assigned to exactly one family.

> Classification note: C03, C13 and C14 carry a period filter but their distinctive convention is the **product list** (ordinal product naming), so they sit in F3. C18 carries a period filter but its distinctive convention is **age at the order**, so it sits in F2b alongside C10 (the same convention, without a period filter). Combinations are only the questions that stack two different conventions.

## 2. Accuracy table (correct / total, and percentage)

| Model | F1 Period (6) | F2 Age at date (4) | F2b Age at order (2) | F3 Product (4) | Combinations (4) | **Total (20)** |
|---|---|---|---|---|---|---|
| openai/gpt-oss-120b | 6/6 — 100% | 4/4 — 100% | 2/2 — 100% | 4/4 — 100% | 3/4 — 75% | **19/20 — 95%** |
| openai/gpt-oss-20b | 6/6 — 100% | 2/4 — 50% | 2/2 — 100% | 4/4 — 100% | 4/4 — 100% | **18/20 — 90%** |
| qwen/qwen3.8-27b | 6/6 — 100% | 4/4 — 100% | 2/2 — 100% | 4/4 — 100% | 0/4 — 0% | **16/20 — 80%** |
| dots-studio/dots-3-note-preview:free | 6/6 — 100% | 2/4 — 50% | 0/2 — 0% | 4/4 — 100% | 1/4 — 25% | **13/20 — 65%** |
| cohere/north-mini-code:free | 6/6 — 100% | 0/4 — 0% | 0/2 — 0% | 4/4 — 100% | 2/4 — 50% | **12/20 — 60%** |

**Execution and retry note:** The trace file contains 102 rows representing 100 unique cells (5 models × 20 questions). Two cells (Qwen C19 and C20) had an initial attempt that failed with HTTP 429 (rate limit). Both were successfully retried. All 100 unique cells therefore have a final executed result. Accuracy is calculated using the final attempt for each cell.

## 3. Which cells the models miss

| Model | Wrong cells (family) |
|---|---|
| cohere/north-mini-code:free | C02, C08, C09, C11 (all F2) · C10, C18 (F2b) · C17, C19 (Comb) |
| dots-studio/dots-3-note-preview:free | C02, C09 (F2) · C10, C18 (F2b) · C15, C16 (Comb) · **C17 (Comb, `sql_invalid`: `syntax_error near "AS"`)** |
| openai/gpt-oss-120b | C19 (Comb) — returned `0` instead of 1990 cents: the product-d + period + age filter excluded every row |
| openai/gpt-oss-20b | C02, C11 (F2) |
| qwen/qwen3.8-27b | C15, C16, C17, C19 (all Comb) |

**Conventions behind the gaps (to be reused in TD 2):**
1. **F2 vs F2b** — the reference-date age ("exactly 25 on 2026-09-xx") is computed from a fixed date, while F2b computes the age at the order date. The two free models (cohere, dots) fail F2b systematically, and cohere fails both.
2. **Age boundary construction** — the "exactly N years old on date Y" window (`Y − (N+1) years < birth_date <= Y − N years`) is where the reference/age families break.
3. **Combinations** — stacking conventions is the single largest source of errors: 10 of the 22 wrong cells in the batch are in the 4 combination questions. qwen3.8-27b is 16/20 but 0/4 on combinations.
4. **One invalid SQL** — dots on C17 (`sql_invalid`) is a *syntax* failure, not a wrong value; it must be reported as `sql_invalid`, not as `incorrect`.

## 4. Retries observed

| Cell | Attempts | Final verdict | Final value | Reference |
|---|---|---|---|---|
| qwen/qwen3.8-27b : C20 | 2 | correct | 1 106 090 | 1 106 090 |
| qwen/qwen3.8-27b : C19 | 2 | incorrect | 83 580 | 1 990 |

The C20 cell only became correct on the second attempt; the first attempt must stay in the raw traces and the summary must carry the final verdict (correct). C19 remained wrong after the retry.

## 5. Reading for the routing rule (Person 2 input)

- A model that is **100 % on a family in this batch**: gpt-oss-120b (F1, F2, F2b, F3), gpt-oss-20b (F1, F2b, F3, Comb), qwen3.8-27b (F1, F2, F2b, F3), dots (F1, F3), cohere (F1, F3).
- A model with **at least one error on a family**: gpt-oss-120b (Comb, C19), gpt-oss-20b (F2), qwen (Comb), dots (F2, F2b, Comb), cohere (F2, F2b, Comb).
- Consequence for the "none" checking strategy: `none` is admissible only for a free model with 100 % on that family **and** a low-stakes internal dashboard. Any family where the chosen model has one error in this table, or any customer-facing figure / payout, requires a quorum or a deterministic reference check.
