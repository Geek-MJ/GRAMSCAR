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

# Evaluation Report: Pair C Deliverables (TD 2 - Step 3)

## 1. Overview and Assessment
The work produced across Step 3 establishes a structured and risk-aware routing pipeline combining empirical TD 1 accuracy metrics (`traces-td1.csv`), explicit verification policies, and an executable routing simulator (`atelier-routage.py`). The analysis properly grounds model selection in observed family-level performance while avoiding unsupported cost assumptions on free-tier APIs and strictly enforcing verification gates based on business impact (`dashboard`, `customer`, `payout`).

## 2. Key Strengths of the Deliverables
- **Accurate Trace Deduplication & Failure Taxonomy:** The baseline accuracy analysis (Person 1) rigorously deduplicated the 102 raw trace rows down to 100 unique cells by retaining only the final attempt for rate-limited retries (`qwen/qwen3.8-27b` on C19 and C20). Furthermore, it cleanly separated SQL syntax failures (`sql_invalid` for `dots-studio` on C17) from logical execution errors and pinpointed the core SQL breakdown patterns (fixed-date vs. order-date age boundaries and stacked condition failures).
- **Risk-Proportional Verification Policy:** The routing rules (Person 2) accurately translate observed batch limitations into operational safeguards. Restricting the `none` verification bypass strictly to low-stakes internal dashboards—and exclusively when the selected free model achieved 100% accuracy on that exact family—prevents over-reliance on small sample sizes (`2` to `6` questions per family). High-impact flows (`customer` and `payout`) systematically enforce `3-of-5` quorum or deterministic reference/human validation.
- **Faithful Simulator Implementation & Capacity Arbitration:** The standalone simulator (Person 3) faithfully encodes the routing constraints, fallback ordering, and abstention rules. Notably, the `--prefer-wait` flag implements smart resource arbitration by deferring non-urgent requests when a free quota refills before the deadline (`refill_minutes <= deadline`), preserving included subscription capacity for urgent tasks.

## 3. Minor Areas for Alignment & Polish
- **Family Partition Alignment (Critical):** There is a methodological divergence between the strict 20-case partition used in the baseline accuracy analysis (Person 1) and the overlapping multi-label grouping used in the routing rules and simulator (Persons 2 & 3). Under the overlapping grouping, `gpt-oss-120b` scores `7/8` (`87.5%`) on F2 due to combined questions, whereas under the strict partition it achieves `4/4` (`100%`), making it eligible for unverified internal dashboard routing. Updating the `PERSON2` dictionary in `atelier-routage.py` and the accuracy tables in Section 2 to match Person 1's strict partition will ensure complete consistency across the final report.
- **Simulator Edge-Case Refinements:** In `load_models()`, the `evidence` dictionary currently collects all passing `case_id` values for a model rather than filtering them by the specific question family. Additionally, when `choose()` assigns a `3-of-5 quorum` check, adding an explicit availability check to confirm that at least three eligible models are concurrently `available=True` would prevent deadlocks during degraded API states.

## 4. Conclusion
The combined deliverables are of **high engineering and analytical quality**, successfully bridging empirical TD 1 error diagnostics with a transparent, risk-calibrated routing architecture ready for final report integration.
