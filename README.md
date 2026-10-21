# Next-Generation AI

**Class:** DIA2  
**Subgroup:** DIA2_3 (GRAMSCAR)  
**Course pack:** `2026-10-18-students-1`

## Group members

- Cyril Ibrahim
- Valentin Fournel
- POUELMO NGONDIA Russine Maurine
- Yutong Cao
- Anais KAMTCHOUANG NONO
- Dinh Chi NGUYEN
- Rakesh Pallepogu
- Guilhem LE DU
- Mahij Gosai
- Soukaina Bahami

## Environment

The project uses Python 3.10 or later, SQLite, and the `requests` library.

Our tested environment includes Python 3.12.15 and SQLite 3.34.1 on Oracle Linux 9.7 (WSL).

The language models are accessed through Groq and OpenRouter using free accounts. API keys are stored locally as environment variables.

**Database:** `boutique.sqlite`  
**SHA-256:** `0077e235adc2ca647b484e3083c98a6d7cae3ef3655ce366a299caf13398fec2`

## Reproducing the results

Use Python 3.10 or later. From a fresh clone:

```bash
git clone https://github.com/Geek-MJ/GRAMSCAR.git
cd GRAMSCAR
python bootstrap_td1.py
python verify-data.py
python skeleton-multi-llm-en.py --rates --state traces-td1.jsonl
python skeleton-multi-llm-en.py --replay traces-td1.jsonl --state replay-check.jsonl --out replay-check.csv
```

The setup script downloads the official student kit `2026-10-18-students-1`, checks the ZIP SHA-256 and restores the original database and supporting files. Existing group results are not overwritten. The replay uses stored SQL responses and makes **no model API calls**, so no API keys are needed. The new `replay-check` files contain replayed results and must not be mixed with the original real traces.
