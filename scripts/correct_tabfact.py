import json, csv
from os.path import exists
import tableHelper
print("opening")
e = open('./tabfact_counterfactual_data_final.jsonl',"r", encoding="utf-8",errors='replace')

d = {}
a = json.load(e)
vv = 1
print("loaded")
for x in a.items():
    key = "table_" + x[0] + ".csv"
    value = [x[1][0][0],x[1][1],x[1][2]]
    d[key] = value
    if vv==1:
        print(key)
        print(value)
        vv = 2

with open('tabfact_format_counterfactual_data.jsonl', 'w', encoding='utf-8') as js_file:
    try:
        json.dump(d, js_file)
    except:
        print("could not write table")