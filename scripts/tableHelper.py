import re
from dateutil.parser import parse


def createTable(table_json,table_no):
    # convert json tables to 2-D arrays 
    d = {}
    d_inverse = {}
    cols = 0
    for cell in table_json["table"][0]:
        cols = cols + cell["column_span"]
    rows = len(table_json["table"])
    arr = []
    middle_headers = [0]
    for r in range(0, rows):
        arr.append([0 for c in range(0, cols)])

    for x in range(len(table_json["table"])):
        row = table_json["table"][x]
        y = 0
        actual_y = -1
        header_cells = 0
        for cell in row:
            if cell["column_span"] != 99 and cell["row_span"] != 99:
                if cell["is_header"] == True: header_cells = header_cells + 1
                actual_y = actual_y +1
                value = cell["value"]
                try:
                    while arr[x][y]!=0: y = y+1
                    if cell["column_span"]>=cols: 
                        cell["column_span"] = cols 
                        middle_headers.append(x)
                        #print("middle headers",x)
                    #print(x,y)

                    for i in range(cell["row_span"]):
                        if x+i<rows and y<cols:
                            arr[x+i][y] = value
                            d[(x,actual_y)] = (x+i,y) 
                            d_inverse[(x+i,y)] = (x,actual_y)  
                    
                    for i in range(cell["column_span"]):
                        if x<rows and y+i<cols:
                            arr[x][y+i] = value
                            d[(x,actual_y)] = (x,y+i) 
                            d_inverse[(x,y+i)] = (x,actual_y)
                except:
                    print("problem with table ",table_no)
        
        if header_cells == len(row) and x not in middle_headers:
            middle_headers.append(x)

    return arr,d,d_inverse,middle_headers

def getUsableRows(arr,middleHeaders):
    aggregateWords = {"total","sum","average","median","avg"}
    usableRows = []
    for i in range(len(arr)):
        isUsable = True
        for cell in arr[i]:
            if str(cell).lower() in aggregateWords: 
                isUsable = False
                #print("has aggregate words ", cell, i)
        if isUsable and (i not in middleHeaders) and i != 0: usableRows.append(i)
    return usableRows

def is_date(string, fuzzy=False):
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except:
        return False

def getUsableCellsPerColumn(arr,usableRows):
    cols =  len(arr[0])
    usefulColValues = []
    empty_dict = {"–","-","n/a","none","tba",""}
    col_type = []
    for i in range(cols):
        alpha = 0
        numeric = 0
        alphanumeric = 0
        date = 0
    
        for j in usableRows:
            value_initial = str(arr[j][i]).lower()
            value = re.sub(r'[^a-zA-Z0-9]', '', value_initial)
            if value not in empty_dict:
                if is_date(value_initial): date = date + 1
                elif value.isnumeric(): numeric = numeric + 1
                elif value.isalpha(): alpha = alpha + 1
                elif value.isalnum(): alphanumeric = alphanumeric + 1
        mx = max(alpha,alphanumeric,date,numeric)
        if date==mx: col_type.append("date")
        elif mx==numeric: col_type.append("numeric")
        elif mx==alpha: col_type.append("alpha")
        else: col_type.append("alphanumeric")

    for i in range(cols):
        usableCellsinCol = []
        for j in usableRows:
            value_initial = str(arr[j][i]).lower()
            value = re.sub(r'[^a-zA-Z0-9]', '', value_initial)
            #print(value, col_type[i])
            if (
            (col_type[i]=="alpha" and value.isalpha()) or 
            (col_type[i]=="alphanumeric" and value.isalnum()) or  
            (col_type[i]=="numeric" and value.isnumeric()) or 
            (col_type[i]=="date" and is_date(value_initial)) ):
                if (len(value)>0) and (value not in empty_dict) and (arr[j][i] not in usableCellsinCol): 
                    usableCellsinCol.append([arr[j][i],j])
        usefulColValues.append(usableCellsinCol)
    return usefulColValues

def getUsableCellsForValue(arr, column, usable_rows, cell_value):
    value_initial = cell_value.lower()
    value = re.sub(r'[^a-zA-Z0-9]', '', value_initial)
    empty_dict = {"–","-","n/a","none","tba","","TBA"}
    type = 3
    if value not in empty_dict:
        if is_date(value_initial): type = 0
        elif value.isnumeric(): type = 1
        elif value.isalpha(): type = 2
        elif value.isalnum(): type = 3
    usableCellsinCol = []
    for j in usable_rows:
        curr_type = 3
        value_initial = str(arr[j][column]).lower()
        value = re.sub(r'[^a-zA-Z0-9]', '', value_initial)
        if is_date(value_initial): curr_type = 0
        elif value.isnumeric(): curr_type = 1
        elif value.isalpha(): curr_type = 2
        elif value.isalnum(): curr_type = 3
        if curr_type == type and value not in empty_dict:
            usableCellsinCol.append({"phrase" : arr[j][column], "row" : j, "column" : column})
    return usableCellsinCol