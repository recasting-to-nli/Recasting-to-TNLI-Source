import json,re
import csv
import itertools
import spacy

en = spacy.load('en_core_web_sm')
file_name = './totto_to_tabfact_data_v2/d5.json'
output_file_name = 'simplified_d5.json'

def simplify(sentence):
    doc = en(sentence)

    seen = set() # keep track of covered words
    seen2 = set()
    chunks = []
    for sent in doc.sents:
        # for cc in sent.root.children:
        #     print(cc.dep_)
        heads = [cc for cc in sent.root.children if cc.dep_ == 'conj']

        nsubj = [cc for cc in sent.root.children if cc.dep_ == 'nsubj']
        nsubjchunk = ""
        if len(nsubj) > 0:
            nsubj = nsubj[0]
            words = [ww for ww in nsubj.subtree]
            for word in words:
                seen2.add(word)
            nsubjchunk = (' '.join([ww.text for ww in words]))
            # print(nsybjchunk)

        for head in heads:
            words = [ww for ww in head.subtree]
            for word in words:
                seen.add(word)
            chunk = (' '.join([ww.text for ww in words]))
            chunks.append( (head.i, chunk) )

        unseen = [ww for ww in sent if ww not in seen]
        chunk = ' '.join([ww.text for ww in unseen])
        chunks.append( (sent.root.i, chunk) )

    chunks = sorted(chunks, key=lambda x: x[0])

    if len(chunks)>1:
        for ii, chunk in chunks:
            if "and ." in chunk or "but ." in chunk:
                updated_sen = chunk.replace(", and .",'.').replace(", but .",".").replace("and .",'.').replace("but .",'.')
                return updated_sen
    return ""


f = open(file_name,'r')
dic = json.load(f)

print(len(dic.keys()))
count = 0
for value in dic.values():
    
    if count%100==0: print(count)
    count += 1

    stmts = value[0]
    new_sents = []
    for i in range(0,len(stmts)):
        stmt = stmts[i]
        sim_stmt = simplify(stmt)
        if sim_stmt != "":
            new_sents.append(sim_stmt)
            value[1].append(value[1][i])
            value[3].append(value[3][i])
    value[0] += new_sents

with open(output_file_name, "w") as outfile:
    json.dump(dic, outfile)