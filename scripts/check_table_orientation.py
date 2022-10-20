import json,re
import csv
import tableHelper,patternHelper
import spacy

nlp = spacy.load('en_core_web_sm')

f = open('./totto_data/totto_dev_data.jsonl',)
table_no = 0
csv_rowlist = []

total_sentences = 0
unusable = 0
empty_box = 0
first_col_header = 0
regex = 0
next = 0
total=0

sents = []
for line in f:
    table_json = json.loads(line)
    table_no = table_no + 1
    #print("Table : ",table_no, table_json["table_webpage_url"])
    arr,d,d_inverse,middle_headers = tableHelper.createTable(table_json,table_no)
    usable_rows = tableHelper.getUsableRows(arr,middle_headers)
    usable_cells_per_column = tableHelper.getUsableCellsPerColumn(arr,usable_rows)
    ## print(usable_cells_per_column)
    #check for regex
    horiz = 0
    row_dict = []
    for x in range(0,len(arr)):
        row = arr[x]
        if x in usable_rows:
            row_values = {}
            for i in range(1,len(row)):
                cell = str(row[i]).strip()
                res = "".join(filter(lambda x: not x.isdigit(), cell))
                res = re.sub('[-—(),.?;−%✓"$/:\']','',res)
                res = res.replace(" ","").replace("—","").replace("Yes","").replace("No","").replace("N/A","").replace("yes","").replace("no","").replace("n/a","")
                res = res.replace("NA","").replace("na","")
                if len(res)>0:
                    if res not in row_values.keys(): row_values[res] = 0
                    row_values[res] = row_values[res]+1
            mx = 0
            mx_key = ""
            #print(row_values)
            for value in row_values.keys():
                if row_values[value]>mx:
                    mx = row_values[value]
                    mx_key = value
            if mx > 0.5*(len(row)-1) and mx>=2: 
                horiz = horiz + 1
                row_dict.append([mx_key,mx])
    #print(horiz)    
    if horiz > 5 and len(arr[0])>=3:
        sents.append(table_json["table_webpage_url"])
        sents.append(str(row_dict))
        sents.append(str(horiz))
        regex = regex + 1
        print(table_json["table_webpage_url"])
        print(horiz)
        
                    


with open('regex_tables.txt','w') as f:
    for sent in sents:
        f.write(sent+'\n')

# print("Empty first box ",empty_box)
# print("First column header ",first_col_header)
print("Regex ",regex)