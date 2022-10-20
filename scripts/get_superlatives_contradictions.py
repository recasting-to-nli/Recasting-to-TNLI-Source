import json,re
import csv
import tableHelper,patternHelper
import spacy
from nltk.corpus import wordnet

nlp = spacy.load('en_core_web_sm')

f = open('./totto_data/totto_dev_data.jsonl',)
table_no = 0
csv_rowlist = []

count_dict = {}
ant_dict = {'best': 'worst', 
'largest': 'smallest', 
'lowest': 'highest', 
'longest': 'shortest', 
'tallest': 'shortest', 
'oldest': 'newest', 
'most': 'least', 
'fastest': 'slowest', 
'coldest': 'hottest', 
'less': 'more', 
'lower': 'higher', 
'earliest': 'latest',
'larger': 'smaller', 
'earlier': 'later', 
'smaller': 'larger', 
'slowest': 'fastest',
'wettest': 'driest', 
'older': 'newer',
'faster': 'slower', 
'closer': 'farther', 
'warmest': 'coolest',
'youngest': 'oldest',
'wealthiest': 'poorest', 
'strongest': 'weakest', 
'greatest': 'smallest', 
'greater': 'smaller',
'slower': 'faster',
'lightest':'heaviest',
'nearest': 'farthest',
'colder': 'warmer', 
'fewer': 'more',
'richest': 'poorest'}

sents = []
for line in f:
    table_json = json.loads(line)
    table_no = table_no + 1
    #print("Table : ",table_no, table_json["table_webpage_url"])
    arr,d,d_inverse,middle_headers = tableHelper.createTable(table_json,table_no)
    usable_rows = tableHelper.getUsableRows(arr,middle_headers)
    usable_cells_per_column = tableHelper.getUsableCellsPerColumn(arr,usable_rows)
    ## print(usable_cells_per_column)
        
    for sentence in table_json["sentence_annotations"]:
        csv_row = []
        csv_row.append(table_json["table_webpage_url"])
        csv_row.append(sentence["final_sentence"])
        org_sen = sentence["final_sentence"].strip()
        sentence = sentence["final_sentence"].lower().strip()
        doc = nlp(org_sen)
        for token in doc:
            if token.tag_=='JJS' or token.tag_=='JJR':
                if token.text not in count_dict.keys(): count_dict[token.text] = 0
                count_dict[token.text] += 1 
                for i in ant_dict.keys():
                    if i == token.text.lower():
                        cont_sentence = org_sen.replace(token.text,ant_dict[i])
                        sents.append(table_json["table_webpage_url"])
                        sents.append(org_sen)
                        sents.append(cont_sentence)
                    elif token.text.lower() == ant_dict[i]:
                        cont_sentence = org_sen.replace(token.text,i)
                        sents.append(table_json["table_webpage_url"])
                        sents.append(org_sen)
                        sents.append(cont_sentence)
                    
           

with open("superlatives_contradictions.txt","w") as f:
    for sent in sents:
        f.write(sent+'\n')