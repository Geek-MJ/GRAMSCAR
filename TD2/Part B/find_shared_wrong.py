import csv, collections

rows = list(csv.DictReader(open("traces-td1.csv", encoding="utf-8")))

groups = collections.defaultdict(set)
for r in rows:
    if r["verdict"] == "incorrect" and r["value"] != "":
        groups[(r["case_id"], r["value"])].add((r["provider"], r["model_requested"]))

found = False
for (q, v), models in sorted(groups.items()):
    if len(models) >= 2:
        found = True
        print(q, "value", v, "models", sorted(models))
if not found:
    print("No shared wrong value: use DEMO-SQL-C11")