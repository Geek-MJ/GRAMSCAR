# TD 2 - Cross-review of Part 1: quorum voting

**Reviewing team:** Pair B  
**Date:** 18 November 2026

## Work reviewed

Our review covers the implementation of `vote_k_sur_n` in `skeleton-multi-llm-en.py` and the comparison table for the twenty TD 1 questions. We used `traces-td1.csv` to check the reported results.

The file contains 102 real trace rows for 100 distinct model-question cells. The two additional rows correspond to Qwen retries on C19 and C20. We retained only the latest attempt for each model and question. Models with an execution error remained in the panel size without casting a vote.

## Checks performed

The voting method passed 18 isolated tests. These covered strict-majority thresholds, duplicate models, missing values, execution errors, zero-valued answers and abstention. We also checked that an executed answer can vote even when it is incorrect: the reference must only be used after the voting decision.

These tests used synthetic inputs, kept separate from the real TD 1 traces.

We then ran the method on the latest trace values for all twenty questions, after converting their statuses to the expected `executed` or `error` format. We compared its outputs with a separate count of votes by value. All twenty rows of the comparison table were confirmed, including the values, vote counts, abstentions and agreement with the references recorded in the traces.

## Results

| Outcome across 20 questions | Fixed 2-of-3 panel | 3-of-5 quorum |
|---|---:|---:|
| Correct consensus | 18 | 17 |
| Incorrect consensus | 0 | 1 |
| Abstention | 2 | 2 |

C02 is the only question for which the decision changes. The fixed panel returns **590320**, supported by gpt-oss-120b and Qwen. The five-model quorum returns **0**, supported by gpt-oss-20b, Cohere and Dots. The reference is **590320**. The explanation in the report is consistent with these votes.

Both panels abstain on C17 and C19. On C17, Dots has invalid SQL and does not vote; the five-model threshold nevertheless remains three. The latest Qwen attempts are correctly used on C19 and C20.

## Recommendation

One improvement concerns the filtering of verdicts. The current implementation excludes known error statuses but could count an unknown status if it carries a numeric value. A synthetic test using `unavailable` confirmed this behaviour.

We recommend explicitly accepting `executed` proposals. When using raw TD 1 traces, both `correct` and `incorrect` must first be mapped to `executed`. This improvement does not change the results of the twenty-question comparison.

## Conclusion and limits

The comparison table is correct against the supplied traces, and no change to its results is required. The voting method passed the tested contract cases; stricter verdict filtering is recommended for unexpected inputs.

The method was tested in isolation. The complete orchestrator and `atelier-vote.py` were not run. This review did not make API calls or re-execute SQL against the database. Reference values were checked within the traces, rather than independently recalculated or compared with a separate `reference-td1.csv` file.
