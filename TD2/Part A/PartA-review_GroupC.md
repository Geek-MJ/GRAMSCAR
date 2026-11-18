# TD 2 — Step 1: k-of-n Consensus Evaluation (2-of-3 vs 3-of-5)

Comparison between the fixed 3-model panel (`openai/gpt-oss-120b`, `cohere/north-mini-code:free`, `qwen/qwen3.8-27b`, threshold `k=2`) and the 5-model quorum across all TD 1 models (threshold `k=3`).

## Definitions

- **Ballot:** one model's last executed proposal on a case that carries a usable value. A model that errors or is unavailable stays in `n` but casts no vote.
- **Quorum (`k-of-n`):** a threshold for validity. A value is accepted when it reaches `k` votes; otherwise the panel abstains.
- **Consensus:** agreement among ballots. Reaching a quorum implies consensus on the winning value, but consensus does not imply correctness.
- **`Consensus (N votes)` below:** `N` is the number of ballots cast for the winning value, not the number of models that voted. In the 3-of-5 panel, `N` can be 3, 4, or 5.

## Results

| Case | Reference | Fixed 2-of-3 Panel (k=2) | 3-of-5 Quorum (k=3) | Match Ref (2-of-3 / 3-of-5) | Explanation (when decision changes) |
|---|---|---|---|---|---|
| **C01** | `792800` | Consensus (3 votes): `792800` | Consensus (5 votes): `792800` | Yes / Yes | Same decision across both panels. |
| **C02** | `590320` | Consensus (2 votes): `590320` | Consensus (3 votes): `0` | Yes / No | Decision shifted from `590320` (2-of-3) to `0` (3-of-5). See §C02 below. |
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
| **C17** | `258180` | No consensus (max 1 vote) | No consensus (max 2 votes: `0`) | - / - | Both panels abstain. The two 3-of-5 ballots agree on `0` (wrong) but fall short of k=3. |
| **C18** | `62480` | Consensus (2 votes): `62480` | Consensus (3 votes): `62480` | Yes / Yes | Same decision across both panels. |
| **C19** | `1990` | No consensus (max 1 vote) | No consensus (max 2 votes: `0`) | - / - | Both panels abstain. The two 3-of-5 ballots agree on `0` (wrong) but fall short of k=3. |
| **C20** | `1106090` | Consensus (3 votes): `1106090` | Consensus (5 votes): `1106090` | Yes / Yes | Same decision across both panels. |

## Detailed Analysis of Decision Shifts

### C02 — the only decision shift

Decision shifted from `590320` (2-of-3) to `0` (3-of-5).

| Model | Panel | Value (cents) | Verdict |
|---|---|---:|---|
| openai/gpt-oss-120b | Fixed | 590320 | correct |
| cohere/north-mini-code:free | Fixed | 0 | incorrect |
| qwen/qwen3.8-27b | Fixed | 590320 | correct |
| openai/gpt-oss-20b | 3-of-5 only | 0 | incorrect |
| dots-studio/dots-3-note-preview:free | 3-of-5 only | 0 | incorrect |

The fixed panel reaches consensus on the correct value (2 votes vs 1). The 3-of-5 panel reaches consensus on the wrong value (3 votes vs 2). Adding `gpt-oss-20b` and `dots` adds two incorrect votes and flips the result.

**Takeaway:** a k-of-n quorum measures agreement, not correctness. The fixed panel succeeds because of its composition (it happens to contain two correct models), not because small panels are inherently safer. Step 2 diagnoses the shared wrong value.

## Method notes

- One ballot per model (its last attempt on each case). Only executed proposals with a usable value vote; errors stay in `n` without casting a vote.
- The reference column is used to check the decision afterwards and is not an input to the vote.
- Reference values are computed independently in TD 1 and stored in `reference-td1.csv`; they are not derived from any model output.
- Vote counts were produced with `python vote_2b.py traces-td1.csv` and cross-checked against `Orchestrateur.vote_k_sur_n` (see `step2-shared-wrong-consensus.md`, §1).
- Full ballots for every case are in `traces-td1.csv`.