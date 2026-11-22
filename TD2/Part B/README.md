# TD 2 - Step 2: Shared wrong consensus on C02

## 1. Identification and quorum verdict

### Identification

**Question C02:** Calculate the revenue excluding VAT, in cents, from all orders of customers who are exactly 25 years old on 2026-09-25.

**Source / nature:** our own merged TD 1 batch, `traces-td1.csv`, real model outputs. This is an observed case, not the historical fallback `DEMO-SQL-C11`.

**Shared wrong value:** 0. Three distinct models agree on this value with verdict `incorrect`: `openai/gpt-oss-20b`, `cohere/north-mini-code:free` and `dots-studio/dots-3-note-preview:free`.

**Reference:** 590320 cents, from the C02 row of `reference-td1.csv`. Part 2A checked this value in the trace `reference` column; Part 2B reports that the reference values in the merged traces match the reference file.

The two faulty queries selected for detailed diagnosis are those returned by `openai/gpt-oss-20b` and `cohere/north-mini-code:free`. Section 2 also records the error made by the third agreeing model.

### Panels and counting rules

| Panel | Members | n | k | Strict majority check |
|---|---|---:|---:|---|
| Fixed 2-of-3 | gpt-oss-120b, cohere, qwen | 3 | 2 | 1 < 2 <= 3 |
| 3-of-5 | All five models below | 5 | 3 | 2 < 3 <= 5 |

Each model has one ballot: its last attempt on C02. Only executed proposals with a usable value vote. An error or an unavailable model remains in n without casting a vote. A value wins when it reaches k votes; otherwise the panel abstains. The reference is used to check the decision afterwards and is not an input to the vote.

### Selected trace values and verdicts

| Model | Provider | Fixed panel? | Value (cents) | Verdict | attempts |
|---|---|---|---:|---|---:|
| openai/gpt-oss-120b | Groq | Yes | 590320 | correct | 1 |
| cohere/north-mini-code:free | OpenRouter | Yes | 0 | incorrect | 1 |
| qwen/qwen3.8-27b | Groq | Yes | 590320 | correct | 1 |
| openai/gpt-oss-20b | Groq | No | 0 | incorrect | 1 |
| dots-studio/dots-3-note-preview:free | OpenRouter | No | 0 | incorrect | 1 |

All five selected proposals executed and carry a value, so all five models vote. There is no abstention caused by an execution error in this case.

### Quorum results

| Panel | Counts | Decision | Check against reference |
|---|---|---|---|
| 2-of-3, k = 2 | 590320: 2 votes (120b, qwen); 0: 1 vote (cohere) | consensus = True; value = 590320; votes = 2 | Correct: the wrong value 0 is outvoted. |
| 3-of-5, k = 3 | 0: 3 votes (20b, cohere, dots); 590320: 2 votes (120b, qwen) | consensus = True; value = 0; votes = 3 | Incorrect: the shared wrong value wins. |

Both panels reach a consensus. Adding 20b and dots to the fixed panel adds two incorrect votes and changes the result from 590320 to 0.

### Reproducible check after cross-review

The updated `find_shared_wrong.py` performs the search and the vote cross-check in one script. The supplied CSV contains **102 real trace rows for 100 model-question cells**. The extra rows are Qwen retries on C19 and C20. The search groups incorrect answers by question and integer value, counting distinct provider/model pairs. It reports candidates across all real attempts and separately across the latest attempts. C02 is a shared wrong case in both searches.

For the vote, only the latest real attempt of each provider/model is retained. Both `correct` and `incorrect` trace statuses are mapped to `executed` when a SQL query and a usable integer value are present and no execution error is recorded. Unknown statuses and failures do not vote. Missing panel members remain in n. No reference value or correctness label is passed to the voting method.

The script loads and executes Pair A's exact `Orchestrateur.vote_k_sur_n` method from `skeleton-multi-llm-en.py`. It does not implement a separate voting algorithm. The reference comparison takes place after the two voting decisions.

From the repository root, run:

```powershell
python find_shared_wrong.py --case C02 --output td2/B-consensus/c02-votes.json
```

When the complete TD 1 reference file is available, also compare its C02 row explicitly:

```powershell
python find_shared_wrong.py --case C02 --reference reference-td1.csv --output td2/B-consensus/c02-votes.json
```

The first command was executed on the supplied real traces. Its [saved output](c02-votes.json) confirms:

- Fixed 2-of-3: `consensus=True, value=590320, votes=2`.
- 3-of-5: `consensus=True, value=0, votes=3`.

The JSON evidence includes the selected ballots, the faulty SQL queries, the reference source, the search results and hashes of the trace file and the submitted voting source. The updated script also reproduces the Part 1 outcomes on the twenty questions: 18 correct consensuses and 2 abstentions for the fixed panel; 17 correct consensuses, 1 wrong consensus and 2 abstentions for the five-model quorum.

The vote method is executed in isolation, without importing the complete kit. This check does not run `atelier-vote.py`, call a provider or re-execute SQL. The optional reference-file comparison was checked with synthetic test inputs, kept separate from the real-trace evidence. A separate complete `reference-td1.csv` was not supplied for this revision; the real-trace run uses its recorded `reference` column. The SQL results in Sections 2 and 3 are the execution results supplied by Part 2C.

### Changes following the reviews

| Review | Follow-up |
|---|---|
| Pair A | Addressed the request for consistency with the common voting implementation: the script now uses Pair A's source method and stores the resulting evidence. |
| Pair C | Incorporated the clarified presentation of the case, voting rules and SQL diagnosis. The correct age window, revenue units and absence of an order-date restriction are stated explicitly. |

Both reviews support the C02 diagnosis and delta calculation. Their feedback does not change the observed values; it improves the consistency of the code and the explanation of the evidence.

### Consequence for checking

A k-of-n quorum measures agreement, not correctness. On C02, three models return 0 through different faulty SQL conditions, and their three votes are enough to make the 3-of-5 quorum accept the wrong value. The fixed 2-of-3 panel succeeds because of its composition. Increasing the number of models does not guarantee a better result when the added models support the same wrong value. A quorum therefore does not protect against an error shared by several models. The result must still be checked independently, using a reference calculated from the data and a deterministic SQL diagnosis such as the delta query in Section 3.

## 2. Faulty SQL clause

### Required rows

Being exactly 25 years old on 2026-09-25 requires the following birth-date window:

```sql
c.birth_date > '2000-09-25'
AND c.birth_date <= '2001-09-25'
```

For date-only birth dates, this means 2000-09-26 to 2001-09-25 inclusive. C02 asks for all orders of these customers, so no order-date restriction is required.

The joins in the faulty queries correctly link customers to their orders using `customer_id`, and orders to products using `product_id`. The errors are in the filters. Revenue is calculated as `SUM(o.quantity_product * p.price)`; `COALESCE(..., 0)` turns the NULL sum of an empty selection into 0.

### Query 1 - openai/gpt-oss-20b

```sql
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date > '2025-09-25' AND c.birth_date <= '2026-09-25';
```

The lower bound keeps customers born after 2025-09-25 and the upper bound keeps those born no later than 2026-09-25. Together, these conditions select customers aged 0 on the reference date, instead of customers aged 25. The birth-date range reported by Part 2C is 1958-06-08 to 2006-08-15, so no customer meets this filter. The query returns 0.

### Query 2 - cohere/north-mini-code:free

```sql
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date <= '2026-09-25' AND c.birth_date > date('2026-09-25', '-26 years')
AND c.birth_date <= date('2026-09-25', '-25 years') AND c.birth_date > date('2026-09-25', '-26 years')
AND o.date >= '2026-09-25 00:00:00' AND o.date < '2026-09-26 00:00:00';
```

| Condition | Actual effect | Comparison with C02 |
|---|---|---|
| `c.birth_date <= '2026-09-25'` | Excludes future births. | Redundant once the upper age-window bound is applied. |
| `c.birth_date > date('2026-09-25', '-26 years')` | Keeps births strictly after 2000-09-25. | Correct lower bound, repeated twice. |
| `c.birth_date <= date('2026-09-25', '-25 years')` | Keeps births on or before 2001-09-25. | Correct upper bound. |
| `o.date >= '2026-09-25 00:00:00'` | Keeps orders at or after midnight on 25 September. | Unrequested restriction on orders. |
| `o.date < '2026-09-26 00:00:00'` | Keeps orders before midnight on 26 September. | Combined with the previous condition, keeps only orders on 25 September. |

The age window is correct, but the order-date filter removes orders required by the question. Part 2C reports that the latest order is dated 2026-09-20 19:24:25, so no order matches this extra day filter. The query returns 0. Removing only the order-date restriction returns 590320.

### Third agreeing model - dots-studio/dots-3-note-preview:free

This model filters on `strftime('%Y-%m-%d', c.birth_date) = '1999-09-25'`. It selects one exact birth date in the wrong year: a customer born then would be 27 on 2026-09-25. The `c.birth_date IS NOT NULL` check does not correct this window. The additional comparison `strftime('%Y-%m-%d', '2026-09-25') = '2026-09-25'` is always true and applies no customer-age restriction. No customer has the selected birth date, so the query also returns 0.

### Recorded execution results

Part 2C reports executing the three faulty queries on `data/boutique.sqlite` with `run_sql.py c02-diagnostic.sql` in read-only mode:

| Query | Result (cents) |
|---|---:|
| gpt-oss-20b faulty query | 0 |
| cohere faulty query | 0 |
| dots faulty query | 0 |
| cohere query without its order-date restriction | 590320 |

The models reach the same wrong value through different filters. Their agreement on 0 does not mean that they selected the same rows correctly.

## 3. Delta diagnostic query

### Rows missed by the faulty queries

The faulty queries select no rows on this database. The delta therefore consists of all customers with orders counted by the correct age window. Listing their revenue identifies exactly which customer contributions were lost:

```sql
SELECT c.customer_id, c.birth_date,
       SUM(o.quantity_product * p.price) AS revenue_cents
FROM customers c
JOIN orders o ON o.customer_id = c.customer_id
JOIN product p ON p.product_id = o.product_id
WHERE c.birth_date > '2000-09-25'
  AND c.birth_date <= '2001-09-25'
GROUP BY c.customer_id, c.birth_date
ORDER BY c.customer_id;
```

### Executed result recorded in Part 2C

| customer_id | birth_date | revenue_cents |
|---|---|---:|
| C001 | 2001-09-25 | 135000 |
| C002 | 2001-09-24 | 25920 |
| C005 | 2000-09-26 | 150240 |
| C007 | 2000-11-30 | 118740 |
| C008 | 2001-05-15 | 99090 |
| C009 | 2001-03-10 | 61330 |
| **Total** | | **590320** |

The six customer contributions sum to 590320, which equals reference minus shared wrong value: **590320 - 0 = 590320**. They account for the entire gap for each faulty query.

The boundary cases confirm the interval: C001 turns 25 on the reference date and is included; C005 turns 26 the next day and is still 25 on the reference date. A customer born on 2000-09-25 would already be 26 and must be excluded.

### Independent checking method

The delta total is compared with the reference query calculated separately in TD 1 and stored in `reference-td1.csv`. Part 2C also reports an independent TD 1 check using Python on the CSV data with a completed-age function. This checks age eligibility by another method rather than accepting agreement between model answers. The two correct model outputs provide supporting observations, but they do not replace this independent reference check.

**Execution material reported by Part 2C:** `c02-diagnostic.sql` contains the faulty queries, the delta query and the total check; `run_sql.py` executes them read-only against `data/boutique.sqlite`.
