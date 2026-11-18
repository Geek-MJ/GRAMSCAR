# TD2 – Pair C, Step 3: Routing Rules
## Person 2 – Model selection, verification and fallback

**Project:** Trustworthy Generative AI  
**Group:** Pair C  
**Role:** Person 2 – Routing decision analysis  
**Date:** 18 November 2026

---

## 1. Objective

The objective is to define how the system selects an LLM for each query family, how its result is verified, and what happens when the preferred model is unavailable.

The routing policy considers:
- observed TD1 accuracy for the relevant query family;
- documented model prices;
- the impact of an incorrect result;
- route availability, quota limits and refill deadlines.

The calculations below use the actual results in `model-question-comparison-en.csv` and the family membership derived from the SQL queries in `reference-td1.csv`. The family groups overlap: a query containing several filters can belong to several families.

## 2. Query families and TD1 accuracy

The families are defined as follows:

- **F1 – Period:** queries containing a date or period condition.
- **F2 – Fixed age:** queries calculating age at a fixed reference date.
- **F2b – Age at order:** queries calculating age using each order's date.
- **F3 – Product list:** queries filtering a specified product or product list.
- **Combinations:** queries combining two or more conditions.

### Case membership used for the calculations

| Family | TD1 cases |
|---|---|
| F1 – Period | C01, C03, C04, C05, C06, C07, C13, C14, C15, C17, C18, C19, C20 |
| F2 – Fixed age | C02, C08, C09, C11, C15, C16, C17, C19 |
| F2b – Age at order | C10, C18 |
| F3 – Product list | C03, C12, C13, C14, C16, C17, C19 |
| Combinations | C03, C13, C14, C15, C16, C17, C18, C19 |

### Accuracy by model and family

| Model | F1 Period | F2 Fixed age | F2b Age at order | F3 Products | Combinations |
|---|---:|---:|---:|---:|---:|
| GPT-OSS-120B | 12/13 (92.3%) | 7/8 (87.5%) | 2/2 (100%) | 6/7 (85.7%) | 7/8 (87.5%) |
| GPT-OSS-20B | 13/13 (100%) | 6/8 (75%) | 2/2 (100%) | 7/7 (100%) | 8/8 (100%) |
| Cohere North Mini Code | 10/13 (76.9%) | 2/8 (25%) | 0/2 (0%) | 5/7 (71.4%) | 5/8 (62.5%) |
| Qwen 3.8 27B | 10/13 (76.9%) | 4/8 (50%) | 2/2 (100%) | 4/7 (57.1%) | 4/8 (50%) |
| Dots 3 Note Preview | 10/13 (76.9%) | 3/8 (37.5%) | 0/2 (0%) | 5/7 (71.4%) | 4/8 (50%) |

**Interpretation:** GPT-OSS-20B has the strongest observed results for F1, F3 and combined queries. GPT-OSS-120B has the strongest observed result for F2 fixed-age queries. For F2b, GPT-OSS-120B, GPT-OSS-20B and Qwen each obtained 2/2, but this family contains only two test cases.

These figures describe the TD1 test set; they do not guarantee future performance. Because the family groups overlap, one case can contribute to more than one column.

## 3. Price and availability comparison

The TD1 experiments used free access. The recorded free quotas have been used, so these routes may require a quota refill before they can be used again.

The available price information documents one paid route for the exact same model:

| Model / route | Documented paid input price | Documented paid output price |
|---|---:|---:|
| GPT-OSS-120B through OpenRouter | $0.15 / 1 million tokens | $0.60 / 1 million tokens |
| GPT-OSS-20B | No exact-model paid price documented | No exact-model paid price documented |
| Cohere North Mini Code `:free` | No exact-model paid price documented | No exact-model paid price documented |
| Qwen 3.8 27B | No exact-model paid price documented | No exact-model paid price documented |
| Dots 3 Note Preview `:free` | No exact-model paid price documented | No exact-model paid price documented |

It is not possible to rank all five models by paid cost because comparable paid prices are not documented for the other exact model routes. A free route should not be described as a paid route costing zero: it has quota and availability limits.

The router must compare prices only when they are documented. It must not invent or assume a price.

## 4. Proposed routing decisions

The first model should be selected from models with suitable observed accuracy on the relevant family. Among eligible routes, choose the cheapest route whose price is documented and whose verification requirements can be met. If the price is unknown, mark it as unknown rather than assuming that the model is the cheapest.

| Query family | Accuracy-based preferred model | Reason |
|---|---|---|
| F1 – Period | GPT-OSS-20B | 13/13 correct (100%) |
| F2 – Fixed age | GPT-OSS-120B | Highest observed result: 7/8 (87.5%) |
| F2b – Age at order | GPT-OSS-120B, GPT-OSS-20B or Qwen | Each obtained 2/2; sample is very small |
| F3 – Product list | GPT-OSS-20B | 7/7 correct (100%) |
| Combinations | GPT-OSS-20B | 8/8 correct (100%) |

These are accuracy-based preferences, not claims that the routes are currently available or that their paid prices are known. In particular, the documented OpenRouter price for GPT-OSS-120B does not establish the paid price of GPT-OSS-20B.

## 5. Verification rules according to risk

The verification level depends on where the answer will be used and the consequence of an error.

| Use case | Proposed verification | Reason |
|---|---|---|
| Internal dashboard, low impact | No additional check only if the selected model has 100% TD1 accuracy on that exact family; otherwise verify | A wrong internal result has limited impact, but observed family errors should not be ignored |
| Customer-facing figure or report | Require agreement from 3 of 5 models, or use a deterministic reference check | Incorrect figures could mislead a customer |
| Payout, payment or other high-impact decision | Validate against trusted reference data or require human review | An incorrect result could cause financial or operational loss |

A model that made at least one error on a family should not be trusted alone for that family. It needs an independent check, such as a model quorum or deterministic validation.

A majority vote does not guarantee correctness because models can make correlated mistakes. For critical values, a deterministic check against the reference data is preferable.

The no-check exception is narrow: it applies only to low-stakes internal dashboard use and only when the model obtained 100% on the exact family in TD1. It must not be used for customer-facing figures or payout decisions.

## 6. Fallback and abstention policy

If the preferred model is unavailable, the router should:

1. **Try the next eligible model** with suitable TD1 results for the same family and the ability to meet the required verification level.
2. **Wait for quota refill** if the task can safely wait and the refill occurs before the deadline.
3. **Abstain or defer the answer** if no sufficiently reliable model or verification route is available before the deadline.

The system should not silently switch to a model with weak results for the relevant family just to return an answer. For high-impact decisions, abstention is safer than an unverified answer.

## 7. Subscription route versus free route

The simulator may select a subscription route immediately when it has no additional cash cost and still has available allocation (`cash = 0`, `allocation > 0`). It may select this route before a free route whose allocation is exhausted (`cash = 0`, `allocation = 0`), even if the free route is expected to refill before the deadline.

This behavior prioritizes immediate availability and avoids waiting. However, it can consume limited subscription allocation unnecessarily.

The priority should be reversed when the task is not urgent, the free quota will refill before the deadline, and waiting does not create a meaningful risk. In that situation, using the free route after refill preserves subscription allocation for tasks that cannot wait.

For urgent or high-impact tasks, the router should prioritize a route that can respond and meet the verification requirement before the deadline.

## 8. Conclusion

The routing policy combines observed family-level accuracy, documented cost, risk-based verification and availability. GPT-OSS-20B is the strongest observed choice for period, product-list and combined queries. GPT-OSS-120B has the strongest observed result for fixed-age queries. For age-at-order queries, the TD1 sample is too small to distinguish the three models that achieved 2/2.

No model should be selected based on an undocumented price. Low-stakes internal results may avoid an extra check only under the strict 100%-accuracy condition. Customer-facing figures need a quorum or deterministic check, while payout decisions require reference validation or human review. If no reliable route is available before the deadline, the system should wait or abstain rather than return an unsafe result.

**Contribution boundary:** This document contains Person 2's routing analysis and proposed decision rules. Person 3 is responsible for implementing and testing the simulator behavior. The final combined report should be checked against Person 1's finalized accuracy methodology so that all members use the same family definitions and figures.
