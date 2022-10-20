import json, csv
import tableHelper,patternHelper

f = open('./totto_format_data.jsonl',"r", encoding="utf-8",errors='replace')
e = open('./rel_cells_5.txt','a',encoding="utf-8",errors='replace')
table_no = -1
tables_data = {}
for line in f:
    if table_no>=40000 and table_no<50000:
        if table_no%100 == 0 : print(table_no)
        table_json = json.loads(line)
        arr, d, d_inverse, middle_headers = tableHelper.createTable(table_json,table_no)
        relevant_cells_for_table = []
        for entailment in table_json["entailments"]:
            # print(entailment)
            try:
                org_sen = entailment
                sentence = entailment.lower().strip()
                relevant_cells = []
                for row in range(0,len(arr)):
                    for col in range(0,len(arr[row])):
                        cell_value = str(arr[row][col])
                        found, coords = patternHelper.findOrdinals(cell_value,sentence)
                        if not found:
                            found, coords = patternHelper.findExactMatch(cell_value,sentence)
                            if not found:
                                found, coords = patternHelper.findPartialMatch(cell_value,org_sen,sentence)
                        if found: relevant_cells.append((row,col))
            except:
                continue
            relevant_cells_for_table.append(relevant_cells)
        for contradiction in table_json["contradictions"]:
            # print(contradiction)
            try:
                org_sen = contradiction
                sentence = contradiction.lower().strip()
                relevant_cells = []
                for row in range(0,len(arr)):
                    for col in range(0,len(arr[row])):
                        cell_value = str(arr[row][col])
                        found, coords = patternHelper.findOrdinals(cell_value,sentence)
                        if not found:
                            found, coords = patternHelper.findExactMatch(cell_value,sentence)
                            if not found:
                                found, coords = patternHelper.findPartialMatch(cell_value,org_sen,sentence)
                        if found: relevant_cells.append((row,col))
            except:
                continue
            relevant_cells_for_table.append(relevant_cells)      
        data = [
            table_no,
            table_json["entailments"] + table_json["contradictions"],
            [1]*len(table_json["entailments"]) + [0]*len(table_json["contradictions"]),
            table_json["table_page_title"] + table_json["table_section_title"],
            relevant_cells_for_table
        ]
        e.write(str(data) + '\n')
    table_no = table_no + 1

# with open('tabfact_data_relevant_cells.jsonl', 'w', encoding='utf-8') as js_file:
#     try:
#         json.dump(tables_data, js_file)
#     except:
#         print("could not write table")