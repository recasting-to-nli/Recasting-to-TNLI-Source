import json, csv
from os.path import exists
import tableHelper

f = open('./totto_to_tabfact_output_6.jsonl',"r", encoding="utf-8",errors='replace')
tables_data = {}
table_no = 99194
for line in f:
    if table_no%5000 == 0:
        print(table_no)
    table_json = json.loads(line)
    arr, d, d_inverse, middle_headers = tableHelper.createTable(table_json,table_no)

    if arr != [] and table_json["entailments"] != [] and table_json["contradictions"] != []:

        with open("./tabfact_csv_data/table_" + str(table_no) + ".csv","w+", encoding='utf-8', newline='') as my_csv:
            csvWriter = csv.writer(my_csv,delimiter='#')
            csvWriter.writerows(arr)
        
        table_name = 'table_' + str(table_no) + '.csv'
        tables_data[table_no]= [
                        table_json["entailments"] + table_json["contradictions"],
                        [1]*len(table_json["entailments"]) + [0]*len(table_json["contradictions"]),
                        table_json["table_page_title"] + table_json["table_section_title"]
                    ]
        table_no += 1
with open('tabfact_data_new_6.jsonl', 'w', encoding='utf-8') as js_file:
    try:
        json.dump(tables_data, js_file)
    except:
        print("could not write table")