r"""Run every statement of a .sql file on data/boutique.sqlite (read-only) and print the rows.
Usage, from kit-td1:  .\.venv\Scripts\python.exe run_sql.py c02-diagnostic.sql"""
import sqlite3, sys
con = sqlite3.connect("file:data/boutique.sqlite?mode=ro", uri=True)
text = open(sys.argv[1], encoding="utf-8").read()
for stmt in [s.strip() for s in text.split(";") if s.strip()]:
    code = "\n".join(l for l in stmt.splitlines() if not l.strip().startswith("--")).strip()
    if not code:
        continue
    print("-" * 70); print(code.splitlines()[0][:70] + " ...")
    cur = con.execute(code)
    print([d[0] for d in cur.description])
    for row in cur.fetchall():
        print(row)
