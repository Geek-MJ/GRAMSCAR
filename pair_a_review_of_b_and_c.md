# Evaluation Report: Pair B & C Deliverables (TD 2 - Step 2)

## 1. Overview and Assessment
The work produced for Step 2 demonstrates a rigorous and methodical investigation into the phenomenon of **shared wrong consensus** using real experimental data from the TD 1 batch (`traces-td1.csv`). Instead of relying on the historical fallback (`DEMO-SQL-C11`), the analysis successfully identified an actual observed failure case on question **C02** where three distinct models (`openai/gpt-oss-20b`, `cohere/north-mini-code:free`, and `dots-studio/dots-3-note-preview:free`) independently converged on the identical incorrect value of `0`.

## 2. Key Strengths of the Deliverables
* **Quorum Analysis (2-of-3 vs. 3-of-5):** The evaluation clearly highlights the core risk of consensus mechanisms: integrating error-prone models into an expanded quorum (3-of-5) shifted the final decision from the correct reference (`590320`) to the shared wrong value (`0`). This provides a textbook demonstration of why majority agreement does not guarantee correctness.
* **Faulty SQL Clause Diagnosis:** The breakdown of the root causes for each model's failure is precise and well-documented. The diagnosis successfully mapped how entirely different logical errors (incorrect age window boundaries, unrequested order-date filters, and arbitrary exact birth-date matches) all resulted in an empty result set, which subsequently defaulted to `0` via the `COALESCE` aggregation.
* **Delta Verification & Reproducibility:** The implementation of the delta diagnostic query (`c02-diagnostic.sql`) executed via read-only mode (`run_sql.py`) provides irrefutable quantitative proof. By isolating the exact six customer records omitted by the faulty filters, the analysis accounted precisely for the `590320` cent gap (`reference - wrong value = 590320 - 0`).

## 3. Minor Areas for Alignment & Polish
* **Methodological Consistency:** While a dedicated script (`vote_2b.py`) was used to verify ballot counts and attempt filtering correctly (taking the latest attempt per model), ensuring full cross-compatibility with the core `Orchestrateur.vote_k_sur_n` implementation in `skeleton-multi-llm-en.py` guarantees a unified codebase.
* **Documentation Structure:** The technical artifacts (`c02-diagnostic.sql`, `run_sql.py`) are cleanly structured and immediately runnable, ensuring high reproducibility.

## 4. Conclusion
The analytical output is of **high academic quality**, effectively blending theoretical insights from the lectures with empirical verification on the SQLite database.