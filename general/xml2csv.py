#!/usr/bin/env python3

import csv
import re
import sys

if len(sys.argv) != 3:
    print("Usage:")
    print("  python3 xml2csv.py input.xml output.csv")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, encoding="utf-8") as f:
    data = f.read()

rows = re.findall(
    r"<ROW>(.*?)</ROW>",
    data,
    flags=re.DOTALL
)

with open(
    output_file,
    "w",
    encoding="utf-8",
    newline=""
) as out:

    writer = csv.writer(
        out,
        quoting=csv.QUOTE_ALL
    )

    writer.writerow(
        [
            "id",
            "workflowname",
            "creatorname",
            "descriptor",
            "islocked"
        ]
    )

    for row in rows:

        def get(tag):
            m = re.search(
                rf"<{tag}>(.*?)</{tag}>",
                row,
                flags=re.DOTALL
            )

            if m:
                return m.group(1).strip()

            return ""

        writer.writerow(
            [
                get("ID"),
                get("workflowname"),
                get("creatorname"),
                get("DESCRIPTOR"),
                get("ISLOCKED"),
            ]
        )

print(f"Wrote {len(rows)} workflows to {output_file}")
