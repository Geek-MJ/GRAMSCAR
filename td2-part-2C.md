## 2. Faulty SQL clause (Pair B, part 2C)

Case: **C02** (own TD 1 batch, nature = real), "revenue of customers exactly 25 years old on 2026-09-25, all their orders".
Shared wrong value **0** returned by `openai/gpt-oss-20b`, `cohere/north-mini-code:free` and `dots-studio/dots-3-note-preview:free`.
Reference (`reference-td1.csv`): **590320**.

Required window: completed age 25 on 2026-09-25, i.e. `birth_date > '2000-09-25' AND birth_date <= '2001-09-25'`, with **no** condition on the order date.

All three faulty queries were executed on `data/boutique.sqlite` (read-only, `run_sql.py c02-diagnostic.sql`) and each returned `0`.

| Model | Faulty condition | What it actually tests | Why it returns 0 |
|---|---|---|---|
| gpt-oss-20b | `c.birth_date > '2025-09-25' AND c.birth_date <= '2026-09-25'` | customers born in the last year, i.e. aged **0**: the model subtracted 1 year instead of 25 | no customer is born after 2025 (birth dates range from 1958-06-08 to 2006-08-15) |
| cohere north-mini-code | `AND o.date >= '2026-09-25 00:00:00' AND o.date < '2026-09-26 00:00:00'` | the age window is right, but only **orders placed on 2026-09-25** are kept, while C02 asks for all orders | the last order in the base is dated 2026-09-20 19:24:25, so no order matches (without this clause, the same query returns 590320) |
| dots-3-note-preview | `strftime('%Y-%m-%d', c.birth_date) = '1999-09-25'` | one **exact** birth date, in the wrong year (that would be age 27), instead of a one-year window | no customer is born on 1999-09-25 |

The three models fail for **three different reasons** but land on the same value 0: an empty filter always gives 0 through `COALESCE(SUM(...), 0)`. Agreement on a value is therefore not evidence of correctness.

## 3. Delta diagnostic query (Pair B, part 2C)

The faulty queries count no customer, so the delta is every customer counted by the reference:

```sql
SELECT c.customer_id, c.birth_date,
       SUM(o.quantity_product * p.price) AS revenue_cents
FROM customers c
JOIN orders o  ON o.customer_id = c.customer_id
JOIN product p ON p.product_id = o.product_id
WHERE c.birth_date > '2000-09-25' AND c.birth_date <= '2001-09-25'
GROUP BY c.customer_id, c.birth_date
ORDER BY c.customer_id;
```

Executed result on `data/boutique.sqlite`:

| customer_id | birth_date | revenue_cents |
|---|---|---|
| C001 | 2001-09-25 | 135000 |
| C002 | 2001-09-24 | 25920 |
| C005 | 2000-09-26 | 150240 |
| C007 | 2000-11-30 | 118740 |
| C008 | 2001-05-15 | 99090 |
| C009 | 2001-03-10 | 61330 |
| **Total** | | **590320** |

Check: 590320 = reference − wrong value = 590320 − 0. These six customers account for the entire gap.
Boundary cases: C001 (born 2001-09-25) turns 25 on the reference date itself and is counted; C005 (born 2000-09-26) is still 25 because he turns 26 the next day.

**Independent checking method.** (1) The total of the delta rows (590320) equals the value of our reference query in `reference-td1.csv`, computed separately in TD 1. (2) The reference itself was cross-checked in TD 1 by a second method (Python on the CSV files, completed-age function). (3) The two correct models of the batch (`gpt-oss-120b`, `qwen3.8-27b`) return 590320 with differently written SQL.

Files: `c02-diagnostic.sql` (the three faulty queries, the delta query and the total check), `run_sql.py` (read-only execution).
