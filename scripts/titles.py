import json


# f = open('totto_dev_data.jsonl',)
# #f = open('example2.jsonl',)
# table_no = 0

# horizontal_tables = []
# links = []
# d = {}
# x = 0
# for line in f:
#     table_no = table_no + 1
#     #print("Table : " + str(table_no))
#     table_json = json.loads(line)
#     #print(table_json["highlighted_cells"])
#     cols = 0
#     for r in table_json["table"]:
#         cols = max(cols,len(r))
#     rows = len(table_json["table"])
#     arr = []
#     for r in range(0, rows):
#         arr.append([0 for c in range(0, cols)])

#     row = table_json["table"][0]
#     for cell in row:
#         value = cell["value"].lower()
#         if len(value)>0:
#             if value in d.keys():
#                 d[value] = d[value]+1
#             else:
#                 d[value] = 0
    
# c = 0    
# sorted_titles = sorted(d.items(), key=lambda x: x[1], reverse=True)
# sorted_titles = sorted_titles[0:150]

# tit = []
# for i in sorted_titles:
#     tit.append(i[0])

tit = ['year', 'notes', 'title', 'date', 'role', 'name', 'event', 'location', 'team', 'venue', 'historical population', 'season', 'party', 'result', 'position', 'no.', 'time', 'rank', 'competition', 'opponent', 'league', '#', 'record', 'country', 'director', 'votes', 'round', 'club', 'score', 'player', '%', 'ref', 'film', 'res.', 'method', 'image', 'league cup', 'album', 'ref.', 'category', 'cup', 'city', 'cast', 'gp', 'award', 'candidate', 'artist', 'points', 'nationality', 'regular season', 'playoffs', 'portrait', 'athlete', 'left office', 'language', 'ppg', 'attendance', 'games', 'type', 'pos', 'fg%', 'ft%', 'rushing', 'gs', 'place', 'rpg', 'label', 'took office', 'apg', 'election', 'genre', 'club performance', 'mpg', 'spg', 'bpg', '3p%', 'song', 'region', 'continental', 'conference', 'fa cup', 'winner', 'driver', 'class', 'g', 'receiving', 'division', 'overall', 'series', 'term', 'peak chart positions', 'refs', 'v', 'standing', 'original air date', 'directed by', 'manufacturer', 'wins', 'written by', 'car', 'term of office', 'county', 'seats', 'from', 'pos.', 'format', '±', 'years', 'district', 'fumbles', 'w', 'l', 'peak position', 'to', 'network', 'population', 'arena', 'engine', 'single', 'description', 'meet', 'status', 'no. overall', 'channel', 'picture', 'no', 'no. in season', 'final', 'opening', 'model', 'member', 'event title', 'source', 'production', 'nominated work', 'music director', 'constituency', 'tournament', 'state', 'length', 'governor', 'death', 'races', 'ref(s)']

# for i in range(100):
#     print(sorted_titles[i])
#     if sorted_titles[i][0].isnumeric() : c = c+1

# print(c)

e = open('100tables.jsonl',)

counts = []
persons = []

table_no = 0
for line in e:
    table_no = table_no + 1
    print("Table : " + str(table_no))
    table_json = json.loads(line)
    cols = 0
    for cell in table_json["table"][0]:
        cols = cols + cell["column_span"]
        
    # rows = len(table_json["table"])
    # arr = []
    # for r in range(0, rows):
    #     arr.append([0 for c in range(0, cols)])
    # count = 0
    # tt = []
    # for x in range(len(table_json["table"])):
    #     row = table_json["table"][x]
    #     y = 0
    #     actual = -1
    #     for cell in row:
    #         if int(cell["row_span"]) > 50: continue
    #         else:
    #             #print("entering cell : " + cell["value"])
    #             value = cell["value"]
    #             # print(x,y,len(arr[x]))
    #             while arr[x][y]!=0: 
    #                 print("while",x,y,len(arr[x]))
    #                 y = y+1
    #             #print("starting to write at " + str(x) + " " + str(y))
    #             for i in range(cell["row_span"]):
    #                 try:
    #                     arr[x+i][y] = value
    #                 except:
    #                     continue    
    #             for i in range(cell["column_span"]):
    #                 try:
    #                     arr[x][y+i] = value
    #                 except:
    #                     continue
    #         # print(arr)
    count = 0
    tt = []
    for header in table_json["table"][0]:
        text = header["value"]
        suffix = text.lower()[::-1][0:2][::-1]
        
        if (suffix=="or" or suffix=="er") and text not in persons:
            # print(text)
            # print(suffix)
            persons.append(text)
    for row in table_json["table"]:
        try:
            #print(row[0]['value'])
            text = row[0]['value'].lower()
            if text in tit:
                if text not in tt : 
                    tt.append(text)
                    count = count+1
        except: continue
    #print(count)
    counts.append([count,table_json["table_webpage_url"],table_no,tt])

counts.sort(reverse=True)
print(persons)
# for i in range(100):
#     print(counts[i])
    