-- TD 2, Pair B, part 2C: wrong consensus on C02, executed on data/boutique.sqlite
-- Question C02: revenue of customers exactly 25 years old on 2026-09-25 (all their orders)
-- Reference (reference-td1.csv): 590320. Shared wrong value: 0.

-- Faulty query 1, openai/gpt-oss-20b (returns 0)
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date > '2025-09-25' AND c.birth_date <= '2026-09-25';

-- Faulty query 2, cohere/north-mini-code:free (returns 0)
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE c.birth_date <= '2026-09-25' AND c.birth_date > date('2026-09-25', '-26 years')
AND c.birth_date <= date('2026-09-25', '-25 years') AND c.birth_date > date('2026-09-25', '-26 years')
AND o.date >= '2026-09-25 00:00:00' AND o.date < '2026-09-26 00:00:00';

-- Faulty query 3, dots-studio/dots-3-note-preview:free (returns 0)
SELECT COALESCE(SUM(o.quantity_product * p.price), 0) AS revenue_cents
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN product p ON o.product_id = p.product_id
WHERE (c.birth_date IS NOT NULL)
  AND (strftime('%Y-%m-%d', c.birth_date) = '1999-09-25')
  AND (strftime('%Y-%m-%d', '2026-09-25') = '2026-09-25');

-- Delta diagnostic query: customers counted by the reference, missed by all three faulty queries
SELECT c.customer_id, c.birth_date,
       SUM(o.quantity_product * p.price) AS revenue_cents
FROM customers c
JOIN orders o  ON o.customer_id = c.customer_id
JOIN product p ON p.product_id = o.product_id
WHERE c.birth_date > '2000-09-25' AND c.birth_date <= '2001-09-25'
GROUP BY c.customer_id, c.birth_date
ORDER BY c.customer_id;

-- Check: the sum of the delta rows must equal reference - wrong value = 590320 - 0
SELECT SUM(revenue_cents) AS delta_total FROM (
  SELECT SUM(o.quantity_product * p.price) AS revenue_cents
  FROM customers c
  JOIN orders o  ON o.customer_id = c.customer_id
  JOIN product p ON p.product_id = o.product_id
  WHERE c.birth_date > '2000-09-25' AND c.birth_date <= '2001-09-25'
  GROUP BY c.customer_id
);
