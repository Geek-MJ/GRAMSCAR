# TD 2 — Step 1: k-of-n Consensus Evaluation (2-of-3 vs 3-of-5)

Comparison between the fixed 3-model panel (`openai/gpt-oss-120b`, `cohere/north-mini-code:free`, `qwen/qwen3.8-27b`, threshold $k=2$) and the 5-model quorum across all TD 1 models (threshold $k=3$).

## Definitions

- **Ballot:** one model's last executed proposal on a case that carries a usable numeric value (raw statuses `correct` and `incorrect` are mapped to `executed`). A model that errors or is unavailable stays in $n$ without casting a vote.
- **Quorum ($k$-of-$n$):** a strict-majority threshold ($n // 2 < k \le n$) for validity. A value is accepted when it reaches $k$ votes; otherwise the panel abstains.
- **Consensus:** agreement among ballots. Reaching a quorum implies consensus on the winning value, but consensus does not imply correctness.
- **`Consensus (N votes)`:** $N$ is the number of ballots cast for the winning value, not the total number of models that voted. In the 3-of-5 panel, $N$ can be 3, 4, or 5.

## Summary Across 20 Questions

| Outcome across 20 questions | Fixed 2-of-3 Panel ($k=2$) | 3-of-5 Quorum ($k=3$) |
|---|---:|---:|
| **Correct consensus** | 18 | 17 |
| **Incorrect consensus** | 0 | 1 |
| **Abstention** | 2 | 2 |

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

### C02 — The Only Decision Shift
Decision shifted from `590320` (2-of-3) to `0` (3-of-5):

| Model | Provider | Panel Membership | Value (cents) | Raw Verdict |
|---|---|---|---:|---|
| `openai/gpt-oss-120b` | Groq | Fixed 2-of-3 & 3-of-5 | `590320` | `correct` |
| `cohere/north-mini-code:free` | OpenRouter | Fixed 2-of-3 & 3-of-5 | `0` | `incorrect` |
| `qwen/qwen3.8-27b` | Groq | Fixed 2-of-3 & 3-of-5 | `590320` | `correct` |
| `openai/gpt-oss-20b` | Groq | 3-of-5 only | `0` | `incorrect` |
| `dots-studio/dots-3-note-preview:free` | OpenRouter | 3-of-5 only | `0` | `incorrect` |

- **2-of-3 panel ($k=2$):** reaches consensus on the correct reference value `590320` (2 votes against 1).
- **3-of-5 quorum ($k=3$):** reaches consensus on the wrong value `0` (3 votes against 2). Adding `openai/gpt-oss-20b` and `dots-studio/dots-3-note-preview:free` adds two incorrect votes and flips the outcome.
- **Takeaway:** a $k$-of-$n$ quorum measures agreement, not correctness. The fixed panel succeeds here because of its composition (it happens to include two models that computed C02 properly), not because smaller panels are inherently safer.

## Method Notes

- **Trace deduplication:** `traces-td1.csv` contains 102 real trace rows across 100 unique model-question cells. Two initial HTTP 429 rate-limit failures on `qwen/qwen3.8-27b` (`C19` and `C20`) were retried; only the last attempt per model and question is retained.
- **Strict contract enforcement:** only proposals explicitly marked `executed` (mapped from raw `correct` and `incorrect` statuses) with a valid integer value cast a vote. Errors (`sql_invalid`) stay in $n$ without voting.
- **Independent reference comparison:** reference values are computed independently in TD 1 and stored in `reference-td1.csv`. The vote decides first without seeing the reference; comparison occurs strictly afterward.
- **Cross-verification:** vote counts were independently produced via `python vote_2b.py traces-td1.csv` and verified against `Orchestrateur.vote_k_sur_n`.
