import json,random
import csv
from nltk import word_tokenize,pos_tag

f = open('totto_dev_data.jsonl',)
table_no = 0
csv_rowlist = []
total_sentences = 0
sentences_with_comparitives = 0
for line in f:
    table_no = table_no + 1
    table_json = json.loads(line)
    for sentence in table_json['sentence_annotations']:
        has_adj = False
        total_sentences = total_sentences + 1
        sentence = sentence["final_sentence"].lower().strip()
        tokens = word_tokenize(sentence)
        pos = pos_tag(tokens)
        for item in pos:
            if (item[1]=='JJR' or item[1]=='JJS') and item[0].lower()!='best':
                row = [item,sentence]
                csv_rowlist.append(row)
                has_adj = True
        if has_adj : sentences_with_comparitives += 1

    
print(sentences_with_comparitives," out of ",total_sentences," have comparitives")

with open('output_superlatives.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerows(csv_rowlist)
                     
