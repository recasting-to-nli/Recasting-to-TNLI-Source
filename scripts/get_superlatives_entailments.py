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
        starting_coord = -1
        for token in doc:
            if token.tag_=='JJS' or token.tag_=='JJR':
                starting_coord = org_sen.find(token.text)
                
        cant_use = False
        coordinates_cells_found = {}
        highlighted_cell_rows = {}
        if starting_coord != -1:
            for cell in table_json["highlighted_cells"]:
                r = d[(cell[0],cell[1])][0]
                c = d[(cell[0],cell[1])][1]
                if r not in highlighted_cell_rows.keys(): highlighted_cell_rows[r] = [c]
                else: highlighted_cell_rows[r].append(c)
                cell_value = arr[r][c].lower().strip()
                cell_value = cell_value.replace("'","").replace(",","").replace("?","").replace("!","").replace('"','')
                org_cell_value = arr[r][c]
                
                found, coords = patternHelper.findOrdinals(cell_value,sentence)
                if found: coordinates_cells_found[(r,c)] = coords
                else:
                    found, coords = patternHelper.findExactMatch(cell_value,sentence)
                    if found: coordinates_cells_found[(r,c)] = coords
                    else: 
                        found, coords = patternHelper.findPartialMatch(cell_value,org_sen,sentence)
                        if found: coordinates_cells_found[(r,c)] = coords
                        else: coordinates_cells_found[(r,c)] = coords
            
            to_be_replaced = -1
            to_be_replaced_end = 0
            repl_key = (0,0)

            for key,value in coordinates_cells_found.items():
                if value[0] < starting_coord and value[0] > to_be_replaced and (not patternHelper.isOrdinal(sentence[value[0]:value[1]])):
                    #print("values ",value)
                    to_be_replaced = int(value[0])
                    to_be_replaced_end = int(value[1])
                    repl_key = key
            #print("frnjf ",to_be_replaced)
            #print(to_be_replaced_end)
            value_being_replaced = arr[repl_key[0]][repl_key[1]]
            if to_be_replaced != -1 and to_be_replaced_end != 0:
                i=0
                while usable_cells_per_column[repl_key[1]][i][0] == value_being_replaced:
                    i += 1
                new_row_value = usable_cells_per_column[repl_key[1]][i][1]
                new_column_value = repl_key[1]
                new_value = usable_cells_per_column[repl_key[1]][i][0]
                json_row_1 = d_inverse[(new_row_value,new_column_value)][0]
                json_col_1 = d_inverse[(new_row_value,new_column_value)][1]
                json_row_2 = d_inverse[(repl_key[0],new_column_value)][0]
                json_col_2 = d_inverse[(repl_key[0],new_column_value)][1]

                table_json["table"][json_row_1][json_col_1]["value"] = value_being_replaced
                table_json["table"][json_row_2][json_col_2]["value"] = new_value
                #print("To be replaced :" , to_be_replaced)    
                #print(to_be_replaced_end)
                g = org_sen[to_be_replaced:to_be_replaced_end]
                replaced = org_sen.replace(g,new_value)
                print(table_no)
                print(org_sen)
                print(replaced)
                r = json.dumps(table_json)
                with open(str(table_no) + '.jsonl','w') as x:
                    x.write(str(r))
            
            
                        
           

#with open("superlatives_contradictions.txt","w") as f:
#    for sent in sents:
#        f.write(sent+'\n')