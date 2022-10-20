import spacy,re
from num2words import num2words

nlp = spacy.load('en_core_web_sm')

def findExactMatch(cell_value, sentence):
    for i in range(0,len(sentence)-len(str(cell_value))+1):
        phrase = sentence[i:i+len(cell_value)]
        if phrase==cell_value:
            return [True,[i,i+len(cell_value)]]
    return [False,[0,0]]

def findOrdinals(cell_value, sentence):
    numeric_parts = re.findall(r'\d+', cell_value)
    for numeric_part in numeric_parts:
        found, coords = findExactMatch(num2words(int(numeric_part), ordinal=True),sentence)
        if found: return [True,coords]
        found, coords = findExactMatch(num2words(int(numeric_part), ordinal=False),sentence)
        if found: return [True,coords]
    return [False,[0,0]]

def findPartialMatch(cell_value,org_sen,sentence):
    doc = nlp(org_sen)
    for ent in doc.ents:
        # print("entity ",ent.text, cell_value)
        found, coords = findExactMatch(ent.text.lower(),cell_value.lower())
        if found: 
            return findExactMatch(ent.text.lower(),sentence) 
    return [False,[0,0]]

def isOrdinal(value):
    try:
        value = int(value)
        return True
    except:    
        rev = value[::-1]
        print(rev)
        if rev[0:2] == "ht" or rev[0:2] == "ts" or rev[0:2] == "dn" or rev[0:2] == "dr": return True
    return False