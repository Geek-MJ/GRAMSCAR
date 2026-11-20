# TD 2 — Step 1: k-of-n Consensus Evaluation (2-of-3 vs 3-of-5)

Comparison between the fixed 3-model panel (`openai/gpt-oss-120b`, `cohere/north-mini-code:free`, `qwen/qwen3.8-27b`, threshold $k=2$) and the 5-model quorum across all TD 1 models (threshold $k=3$).

| Case | Reference | Fixed 2-of-3 Panel ($k=2$) | 3-of-5 Quorum ($k=3$) | Match Ref (2-of-3 / 3-of-5) | Explanation (when decision changes) |
|---|---|---|---|---|---|
| **C01** | `792800` | Consensus (3 votes): `792800` | Consensus (5 votes): `792800` | Yes / Yes | Same decision across both panels. |
| **C02** | `590320` | Consensus (2 votes): `590320` | Consensus (3 votes): `0` | Yes / No | Decision shifted from `590320` (2-of-3) to `0` (3-of-5). Details: openai/gpt-oss-120b -> correct (590320); openai/gpt-oss-20b -> incorrect (0); cohere/north-mini-code -> incorrect (0); qwen/qwen3.8-27b -> correct (590320); dots-studio/dots-3-note-preview -> incorrect (0). |
| **C03** | `936350` | Consensus (3 votes): `936350` | Consensus (5 votes): `936350` | Yes / Yes | Same decision across both panels. |
| **C04** | `2826250` | Consensus (3 votes): `2826250` | Consensus (5 votes): `2826250` | Yes / Yes | Same decision across both panels. |
| **C05** | `38480` | Consensus (3 votes): `38480` | Consensus (5 votes): `38480` | Yes / Yes | Same decision across both panels. |
| **C06** | `0` | Consensus (3 votes): `0` | Consensus (5 votes): `0` | Yes / Yes | Same decision across both panels. |
| **C07** | `13970` | Consensus (3 votes): `13970` | Consensus (5 votes): `13970` | Yes / Yes | Same decision across both panels. |
| **C08** | `605580` | Consensus (2 votes): `605580` | Consensus (4 votes): `605580` | Yes / Yes | Same decision across both panels. |
| **C09** | `487980` | Consensus (2 votes): `487980` | Consensus (3 votes): `487980` | Yes / Yes | Same decision across both panels. |
| **C10** | `558980` | Consensus (2 votes): `558980` | Consensus (3 votes): `558980` | Yes / Yes | Same decision across both panels. |
| **C11** | `446690` | Consensus (2 votes): `446690` | Consensus (3 votes): `446690` | Yes / Yes | Same decision across both panels. |
| **C12** | `1666490` | Consensus (3 votes): `1666490` | Consensus (5 votes): `1666490` | Yes / Yes | Same decision across both panels. |
| **C13** | `107740` | Consensus (3 votes): `107740` | Consensus (5 votes): `107740` | Yes / Yes | Same decision across both panels. |
| **C14** | `0` | Consensus (3 votes): `0` | Consensus (5 votes): `0` | Yes / Yes | Same decision across both panels. |
| **C15** | `168680` | Consensus (2 votes): `168680` | Consensus (3 votes): `168680` | Yes / Yes | Same decision across both panels. |
| **C16** | `376740` | Consensus (2 votes): `376740` | Consensus (3 votes): `376740` | Yes / Yes | Same decision across both panels. |
| **C17** | `258180` | No consensus (max 1 vote) | No consensus (max 2 votes) | - / - | Same decision across both panels. |
| **C18** | `62480` | Consensus (2 votes): `62480` | Consensus (3 votes): `62480` | Yes / Yes | Same decision across both panels. |
| **C19** | `1990` | No consensus (max 1 vote) | No consensus (max 2 votes) | - / - | Same decision across both panels. |
| **C20** | `1106090` | Consensus (3 votes): `1106090` | Consensus (5 votes): `1106090` | Yes / Yes | Same decision across both panels. |

## Detailed Analysis of Decision Shifts (2-of-3 vs 3-of-5)

- **C02**: Decision shifted from `590320` (2-of-3) to `0` (3-of-5). Details: openai/gpt-oss-120b -> correct (590320); openai/gpt-oss-20b -> incorrect (0); cohere/north-mini-code -> incorrect (0); qwen/qwen3.8-27b -> correct (590320); dots-studio/dots-3-note-preview -> incorrect (0).

---

## Step 2 — Person 3: Routing simulator (illustrative implementation)

### Objective and implementation

Person 3 implemented `atelier-routage-person3.py`, a standalone routing demonstration based on Person 2's family-level model preferences. It loads model identities and TD1 summary data from `GRAMSCAR-main/five-model-summary-en.csv` and `GRAMSCAR-main/model-question-comparison-en.csv`. The `choose()` function returns an action (`RUN`, `DEFER`, or `ABSTAIN`), a selected model, a required verification method, and an explanation. The simulator does **not** call a model API or perform the verification itself.

The professor's original `atelier-routage.py` was not supplied. Consequently, these seven scenarios and their quota/refill settings are **synthetic demonstrations**, not the official professor's original or before/after outputs.

### Family preferences from Person 2

| Question family | Preferred model | Observed score | Policy |
|---|---|---|---|
| F1 (period) | GPT-OSS-20B | 13/13 | Free route preferred |
| F2 (fixed-reference age) | GPT-OSS-120B | 7/8 | Verification required |
| F2b (age at order date) | GPT-OSS-20B (provisional tie choice) | 2/2 | Compare costs before final choice |
| F3 (product lists) | GPT-OSS-20B | 7/7 | Free route preferred |
| Combinations | GPT-OSS-20B | 8/8 | Free route preferred |

For an internal dashboard, no additional check is requested only when a **free** route has 100% observed accuracy for the relevant family. Customer-facing results require a 3-of-5 quorum or deterministic validation. Payout results require deterministic SQL validation or human review. Selecting a route does not satisfy these checks.

### Seven illustrative scenario results

| Scenario | Action | Model | Required check |
|---|---|---|---|
| `free_ready` | RUN | GPT-OSS-20B | None (F1 dashboard, free 13/13) |
| `subscription_ready` | RUN | GPT-OSS-120B | 3-of-5 quorum or deterministic validation |
| `deferrable` (default priority) | RUN | GPT-OSS-120B | 3-of-5 quorum or deterministic validation |
| `deadline_too_soon` | ABSTAIN | — | — |
| `customer_checked` | RUN | GPT-OSS-20B | 3-of-5 quorum or deterministic validation |
| `payout_checked` | RUN | GPT-OSS-120B | Deterministic SQL validation or human review |
| `all_unavailable` | ABSTAIN | — | — |

The `deferrable` case demonstrates a policy tradeoff: with the default settings, an available subscription allocation runs immediately; with `--prefer-wait`, the simulator returns **DEFER → GPT-OSS-20B** because the free quota refills before the deadline. For nonurgent requests, waiting can conserve subscription allocation.

### Reproduction

```bash
python3 atelier-routage-person3.py
python3 atelier-routage-person3.py --scenario deferrable --prefer-wait
```

The program requires the two CSV files under `GRAMSCAR-main/` next to the script. The scenario output is saved separately in `reports/person3-scenario-results.txt`; further explanation is in `reports/person3-routing.md`.

### Limitations and pending verification

- Official instructor before/after comparison is unavailable without the original `atelier-routage.py`.
- F2 and F2b scores and question IDs should be cross-checked against Person 1's family-level table; the displayed example TD1 case IDs in simulator output are not family-filtered.
- The F2b cost tie and actual paid/subscription route availability have not been independently established.
- Quorum, deterministic SQL checking, and human review are requirements for a downstream system, **not operations performed by this simulator**.
