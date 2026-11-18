# TD 2 - Internal cross-review of Pair C (from Pair B, part 2C)

## Report (accuracy analysis)

Very good. All numbers were recomputed from `traces-td1.csv` and are correct: scores per family, totals (19, 18, 16, 13, 12 out of 20), the 22 wrong cells (10 of them in combinations) and the two qwen retries (C19, C20).

Small fixes for the report:

1. F3: products a, b, c, d are `product_id` values in the `product` table, not "ordinal positions".
2. "The two free models": all 5 models are free. Better to say "the two OpenRouter models" (cohere and dots).
3. Add our C02 case: in F2, three models (gpt-oss-20b, cohere, dots) agree on the wrong value 0 and the 3-of-5 quorum picks it. So for F2, a quorum is not enough: a deterministic check is needed.

## Code (routing simulator)

1. Main issue: the scores in the code do not match the report.

   | Family, model | Report | Code |
   |---|---|---|
   | F1, gpt-oss-20b | 6/6 | 13/13 |
   | F2, gpt-oss-120b | 4/4 | 7/8 |
   | F3, gpt-oss-20b | 4/4 | 7/7 |
   | Combinations, gpt-oss-20b | 4/4 | 8/8 |

   F1 has only 6 questions, so 13/13 is impossible. The code should use the numbers from the report.
2. The evidence cells are not filtered by family. The assignment asks to cite the TD 1 cells of each family (for example F2 = C02, C08, C09, C11).
3. `atelier-routage.py` is in the kit. The assignment asks to adapt it and to show the outputs before and after adaptation, with the instructor's 7 scenarios.
4. The path `GRAMSCAR-main` is hardcoded, so the code may not run on another member's computer.

## Good points

- Correct `none` rule: only for a low-stakes internal dashboard and a free model at 100 % on the family.
- The simulator abstains when no model is eligible or available.
- Every decision carries a written reason.
- The `--prefer-wait` option answers the priority question: by default the available subscription runs first; when the request is not urgent, waiting for the free refill preserves the subscription capacity.
