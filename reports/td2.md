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
