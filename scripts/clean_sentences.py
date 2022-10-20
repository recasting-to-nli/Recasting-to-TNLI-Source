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
superlatives = 0
comparitive = 0
same = 0
next = 0
total=0

sents = []
word_list = ["same","next","average","total"]
for line in f:
    table_json = json.loads(line)
    table_no = table_no + 1
    #print("Table : ",table_no, table_json["table_webpage_url"])
    arr,d,d_inverse,middle_headers = tableHelper.createTable(table_json,table_no)
    usable_rows = tableHelper.getUsableRows(arr,middle_headers)
    usable_cells_per_column = tableHelper.getUsableCellsPerColumn(arr,usable_rows)
    ## print(usable_cells_per_column)

    if len(usable_rows)>0:
        
        for sentence in table_json["sentence_annotations"]:
            csv_row = []
            csv_row.append(table_json["table_webpage_url"])
            csv_row.append(sentence["final_sentence"])
            org_sen = sentence["final_sentence"].strip()
            sentence = sentence["final_sentence"].lower().strip()
            doc = nlp(org_sen)
            for token in doc:
                if token.tag_=='JJS': superlatives = superlatives + 1    
                if token.tag_=='JJR': comparitive = comparitive + 1
                if token.text.lower()=='same': same = same + 1
                if token.text.lower()=='next': next = next + 1
                if token.text.lower()=='total' or token.text.lower()=='average': total=total+1
                if token.tag_=='JJS' or token.tag_=='JJR' or token.text.lower() in word_list:
                    sents.append(table_json["table_webpage_url"])
                    sents.append(org_sen)
                    
           

print("superlatives ",superlatives)
print("comparitives ",comparitive)
print("totals ",total)
print("same ",same)
print("next ",next)

with open('chosen_sents.txt','w') as f:
    for sent in sents:
        f.write(sent+'\n')

            