# Person 2 – Routing Rule (Pair C)

**Project:** TD2 – Voting and Routing  
**Role:** Person 2 – Pair C / Step 3

> **Scope:** these conclusions come from one batch of 20 TD1 questions (C01–C20). They are batch-specific observations, not general model rankings, and a quorum is not a guarantee of reliability. Families overlap, so the rows must not be added together.

## 1. Cost basis

All five models have free access in the portfolio, so their nominal marginal price is $0 while quota lasts. The only documented paid price is for **GPT-OSS-120B** on its OpenRouter route (**$0.15 input / $0.60 output per million tokens**). That price does not apply to its Groq Free route. The other four models have no documented paid route, so their paid price is treated as unknown. Quota availability is not established by the data.

**Selection rule:** among models with the best observed result on the family, choose the cheapest known route. If route costs tie at $0, break the tie with observed accuracy.

## 2. Routing table

| Family | TD1 cases | Accuracy per model (correct / cases) | First model | Consistency status |
|---|---|---|---|---|
| **F1 – Period** | C01, C03, C04, C05, C06, C07, C13, C14, C15, C17, C18, C19, C20 | 120B 12/13 · 20B **13/13** · Cohere 10/13 · Qwen 10/13 · Dots 10/13 | **GPT-OSS-20B** | Only 20B is error-free |
| **F2 – Fixed-date age** | C02, C08, C09, C11, C15, C16, C17, C19 | 120B 7/8 · 20B 6/8 · Cohere 2/8 · Qwen 4/8 · Dots 3/8 | **GPT-OSS-120B** (best observed) | **No model is error-free: always verify** |
| **F2b – Age at order date** | C10, C18 | 120B **2/2** · 20B **2/2** · Cohere 0/2 · Qwen **2/2** · Dots 0/2 | **GPT-OSS-120B** | Three-way tie on a tiny sample |
| **F3 – Product list** | C03, C12, C13, C14, C16, C17, C19 | 120B 6/7 · 20B **7/7** · Cohere 5/7 · Qwen 4/7 · Dots 5/7 | **GPT-OSS-20B** | Only 20B is error-free |
| **Combinations** | C03, C13, C14, C15, C16, C17, C18, C19 | 120B 7/8 · 20B **8/8** · Cohere 5/8 · Qwen 4/8 · Dots 4/8 | **GPT-OSS-20B** | Only 20B is error-free |

**F2b note:** 120B, 20B and Qwen all cost $0 on their free routes. 120B is chosen as the tie-break because it scored best on the related fixed-date age family (F2). With only 2 cases this is weak evidence.

## 3. Checking method by use case

| Use | Rule |
|---|---|
| **Internal dashboard** | No extra check only if the selected free model scored 100% on that family: F1, F3, Combinations (20B) and F2b (120B). **F2 always needs a check**, because every model made at least one error. |
| **Customer-facing figure** | Quorum (3-of-5) or, preferably, a deterministic reference check. |
| **Payout / high-impact** | Deterministic reference check or human review. Never rely on an LLM vote alone. |

**Consistency constraint:** any model that made at least one error on a family (e.g. 120B on F1, F3 and Combinations, or any model on F2) cannot be used alone. It needs a 2-of-3 quorum or a deterministic check, even for an internal dashboard.

## 4. Fallback if the first model is unavailable

| Family | 1. Next model (verification kept) | 2. If the request can wait | 3. Otherwise |
|---|---|---|---|
| F1 | GPT-OSS-120B (12/13) | Wait for the 20B quota refill | Abstain |
| F2 | GPT-OSS-20B (6/8) | Wait for the 120B quota refill | Abstain |
| F2b | GPT-OSS-20B (2/2), then Qwen (2/2) | Wait for the refill | Abstain |
| F3 | GPT-OSS-120B (6/7) | Wait for the 20B quota refill | Abstain |
| Combinations | GPT-OSS-120B (7/8) | Wait for the 20B quota refill | Abstain |

**Rules for all fallbacks**

- Switching model never removes the check required by the use case. A fallback model with an error on that family always needs verification.
- Do not use models below roughly 75% on a family. Defer or abstain instead.
- Do not silently return a result from a poorly performing model.
- If a price or route is unknown, treat it as unknown, not as free.

## 5. Limits

- 20 questions, one batch: a 100% score on 2, 7, 8 or 13 cases does not prove future reliability.
- F2b rests on only 2 cases.
- Quorum sizes (2-of-3, 3-of-5) are policy choices, not measured reliability.
