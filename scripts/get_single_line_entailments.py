import json,re
import csv
import tableHelper,patternHelper
import itertools

f = open('100_set2.jsonl',)
table_no = 0
csv_rowlist = []
json_list = []


total_sentences = 0
unusable = 0

for line in f:
    table_json = json.loads(line)
    table_no = table_no + 1
    print("Table : ",table_no, table_json["table_webpage_url"])
    table_json["replaced_sentences"] = []
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
            
            
            cant_use = False
            coordinates_cells_found = {}
            highlighted_cell_rows = {}
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
                if coordinates_cells_found[(r,c)] == [0,0] :
                    # print(org_sen)
                    # print(cell_value, " : entry not found")
                    cant_use = True
            if cant_use: unusable = unusable + 1
            total_sentences = total_sentences + 1

            if ("total" in sentence) or ("average" in sentence) or cant_use:
                continue
            else:
                if len(highlighted_cell_rows)==1:
                    #print("rows 1")
                    options = []
                    for r in highlighted_cell_rows:
                        common_rows = []
                        flag = True
                        for c in highlighted_cell_rows[r]:
                            new_options = []
                            for row_number in usable_cells_per_column[c]:
                                row_number = row_number[1]
                                if row_number in common_rows or flag: 
                                    new_options.append(row_number)
                            common_rows = new_options  
                            flag = False
                        if r in common_rows: common_rows.remove(r)   
                        options.append(common_rows)
                    print(options)
                    for r in highlighted_cell_rows:
                        for option in common_rows:
                            replaced_sentence = org_sen
                            for c in highlighted_cell_rows[r]:
                                coords = coordinates_cells_found[(r,c)]
                                phrase = org_sen[coords[0]:coords[1]]
                                for el in usable_cells_per_column[c]:
                                    if el[1] == option:
                                        replaced_sentence = replaced_sentence.replace(phrase,el[0])
                                        # replaced_sentence = replaced_sentence.strip()
                                        # replaced_sentence = re.sub('\s+',' ',replaced_sentence)
            
                            print("original : " + org_sen)
                            print("replaced : " + replaced_sentence)
                            table_json["replaced_sentences"].append(replaced_sentence)
                            if replaced_sentence not in csv_row:
                                csv_row.append(replaced_sentence)
                            
                if len(csv_row)> 2:
                    csv_rowlist.append(csv_row)
        json_list.append(json.dumps(table_json))
#with open('output_entailments_v2_set2.csv', 'w') as file:
#    writer = csv.writer(file)
#    writer.writerows(csv_rowlist) 
with open('entailments.jsonl','w') as x:
    for js in json_list:
        x.write(str(js)+'\n')                    
