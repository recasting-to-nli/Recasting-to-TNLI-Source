import json,random,re
import copy
import tableHelper,string

f = open('100_set2.jsonl',)
table_no = 0
csv_rowlist = []
json_list = []

def make_counterfactual_table(table_json, new_cell, cell, cell_value, d_inverse):
    tb = copy.deepcopy(table_json["table"])
        
    # print(tb[cell[0]][cell[1]])
    # print(tb[d_inverse[(new_cell[1],cell[1])][0]][d_inverse[(new_cell[1],cell[1])][1]])

    # print("\n\n")

    tb[cell[0]][cell[1]]["value"] = new_cell[0]
    tb[d_inverse[(new_cell[1],cell[1])][0]][d_inverse[(new_cell[1],cell[1])][1]]["value"] = cell_value
    # print(new_cell[1])
    # print(tb[cell[0]][cell[1]])
    # print(tb[d_inverse[(new_cell[1],cell[1])][0]][d_inverse[(new_cell[1],cell[1])][1]])
    # print("\n\n")
    # print("\n\n")
    # print(table_json["table"])
    # print(tb)
    # print("\n\n")
    table_json["counterfactual_tables"].append(tb)


for line in f:
    table_json = json.loads(line)
    table_json["replaced_sentences"] = []
    table_json["counterfactual_tables"] = []
    table_no = table_no + 1
    # if table_no == 2: break
    # print("Table : ",table_no, table_json["table_webpage_url"])
    arr,d,d_inverse,middle_headers = tableHelper.createTable(table_json,table_no)
    usable_rows = tableHelper.getUsableRows(arr,middle_headers)
    usable_cells_per_column = tableHelper.getUsableCellsPerColumn(arr,usable_rows)
    # print(usable_cells_per_column)

    if len(usable_rows)>0:
        for cell in table_json["highlighted_cells"]:
            r = d[(cell[0],cell[1])][0]
            c = d[(cell[0],cell[1])][1]
            cell_value = arr[r][c].lower()
            cell_value = cell_value.replace("'","").replace(",","").replace("?","").replace("!","").replace('"','')
            org_cell_value = arr[r][c]
            # print(cell_value)
            #len_value = len(cell_value.strip().split(" "))
            for sentence in table_json["sentence_annotations"]:
                csv_row = []
                csv_row.append(table_json["table_webpage_url"])
                csv_row.append(sentence["final_sentence"])
                org_sen = sentence["final_sentence"]
                sentence = sentence["final_sentence"].lower().strip()
                # print(sentence)

                if ("total" in sentence) or ("average" in sentence):
                    continue
                else:
                    # print("starting create contradictions")
                    for i in range(0,len(sentence)-len(cell_value)+1):
                        # print(sentence)
                        # print(cell_value)
                        phrase = sentence[i:i+len(cell_value)]
                        if phrase==cell_value:
                            for new_cell in usable_cells_per_column[c]:
                                try:
                                    if new_cell[0].lower() != cell_value.lower() and new_cell[0].lower() not in sentence.lower():
                                        # print("original : " + sentence)
                                        replaced = org_sen.replace(org_cell_value,new_cell[0])
                                        # print("replaced : " + replaced)
                                        # for making jsons
                                        table_json["replaced_sentences"].append(replaced)
                                        make_counterfactual_table(table_json, new_cell, cell, cell_value, d_inverse)
                                        # print(c_table)
                                        # table_json["counterfactual_tables"].append(c_table)
                                        if replaced not in csv_row:
                                            csv_row.append(replaced)
                                except:
                                    print("here")
                                    continue
                    
                    if len(csv_row)> 2:
                        csv_rowlist.append(csv_row)
        json_list.append(json.dumps(table_json))

with open('contradictions_2.jsonl','w') as x:
    for js in json_list:
        x.write(str(js)+'\n')


