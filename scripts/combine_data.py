import json, csv
from os.path import exists
import tableHelper

e = open('./totto_to_tabfact_output_6.jsonl',"r", encoding="utf-8",errors='replace')

lines = 0
# f = open('./totto_counterfactual_data_output_6.jsonl',"r", encoding="utf-8",errors='replace')
for line in e:
    lines += 1
print(lines)
# f = open('./totto_counterfactual_data_output_3.jsonl',"r", encoding="utf-8",errors='replace')
# for line in f:
#     e.write(line)
# f = open('./totto_counterfactual_data_output_5.jsonl',"r", encoding="utf-8",errors='replace')
# for line in f:
#     e.write(line)

# e = open('./totto_format_data.jsonl',"r", encoding="utf-8",errors='replace')

# lines = 0
# for line in e:
#     lines+=1

# print(lines)