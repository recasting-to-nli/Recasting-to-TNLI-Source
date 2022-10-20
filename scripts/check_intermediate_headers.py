import json,random
import csv

f = open('100tables.jsonl',)
table_no = 0

total_tables_with_intermediate_headers = 0
links = []
number_of_middle_headers = []

for line in f:
    table_json = json.loads(line)
    header_rows = 0
    for row in table_json["table"]:
        has_headers = False
        for cell in row:
            if cell["is_header"] and cell["row_span"] > 1:
                has_headers = True
                break
        if has_headers: header_rows = header_rows + 1
    if header_rows>0:
        total_tables_with_intermediate_headers = total_tables_with_intermediate_headers + 1
        links.append(table_json["table_webpage_url"])
        number_of_middle_headers.append(header_rows - 1)

print(total_tables_with_intermediate_headers)
print(links)
print(number_of_middle_headers)

    