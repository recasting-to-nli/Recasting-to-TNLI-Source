import json


# totto_tables_file = open('totto_to_tabfact_data.jsonl','r')
totto_tables_file = open('totto_counterfactual_data.jsonl','r')

totto_tables = totto_tables_file.readlines()

table_no = 0

# directory_to_save_html = "./totto_html"
directory_to_save_html = "./totto_counterfactual_html"

## Make HTML tables for every json in .jsonl file
for i in range(0,len(totto_tables)):
    ## html will store raw html lines for this table
    html = []
    table_no = table_no+1
    print(table_no)

    table_json = json.loads(totto_tables[i])
    highlighted_cells = table_json["highlighted_cells"]

    ## Add title
    html.append("<html><body><h1>" + table_json["table_page_title"] + "</h1>")

    ## Add table title for reference
    html.append("<h2>" + table_json["table_section_title"] + "</h2><br>")

    ## Split display into two halves, display table on left and text on right
    html.append('<div style="display:flex;"><div style="flex:50%">')

    ## Begin table
    html.append("<table border='1px solid black'>")
    for i in range(0,len(table_json["table"])):
        row = table_json["table"][i]
        row_html = "<tr>"
        for j in range(0,len(row)):
            cell = row[j]
            row_html += '<td rowspan="' + str(cell["row_span"]) + '" colspan="' + str(cell["column_span"]) + '" '
            ## Mark highlighted cells with yellow background
            if [i,j] in highlighted_cells : row_html += "bgcolor='yellow' "
            row_html += '>' + str(cell["value"]) + "</td>"
        row_html += "</tr>"
        html.append(row_html)

    html.append("</table></div><div style='flex:50%'>")
    
    ## Begin printing entailments
    html.append("<h3>Entailments</h3>")
    for sentence in table_json["entailments"]:
        html.append("<p>" + sentence+"</p>")

    ## Begin printing contradictions
    html.append("<h3>Contradictions</h3>")
    for sentence in table_json["contradictions"]:
        html.append("<p>" + sentence+"</p>")
    
    html.append("</div></div>")
    
    for i in range(1,101):
        html.append("<a href=./table"+str(i)+".html> Table"+str(i)+"></a>")
        
    html.append("</body></html>")

    
    try:
        with open(directory_to_save_html + "/table" + str(table_no) + ".html","w") as e:
            for sent in html:
                e.write(sent + '\n')
    except:
        pass

