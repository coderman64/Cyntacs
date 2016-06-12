from tkinter import *
import keyword

defLists = {}

for i in ["keyword","builtin"]:
    o12 = i+": "
    syntaxDefinitionFile = open("SyntaxDefs.txt")
    synDef = syntaxDefinitionFile.read()
    index1 = synDef.find(o12)
    keyDef = synDef[index1:]
    index2 = keyDef.find("\n")
    keyDefList = keyDef[len(o12):index2].split(',')
    #print(keyDefList)
    defLists[i] = keyDefList

def highlightSyntax(text, filename):
    if filename.endswith(".py") or filename.endswith(".pyw"):
        text.tag_delete("keyword")
        text.tag_delete("builtin")
        text.tag_configure("keyword", foreground="orange")
        text.tag_configure("builtin", foreground="purple")
        for s in defLists["keyword"]:
            s = s.strip()
            start = 1.0
            while 1:
                pos = text.search(s, start, stopindex=END)
                if not pos:
                    break
                else:
                    if text.get(pos+"-1c",pos+"+"+str(len(s)+1)+"c").strip(" \n\t:") == str(s):
                        text.tag_add("keyword",pos,pos+"+"+str(len(s))+"c")
                #print(pos)
                start = pos + "+1c"
        for s in defLists["builtin"]:
            s = s.strip()
            start = 1.0
            while 1:
                pos = text.search(s, start, stopindex=END)
                if not pos:
                    break
                else:
                    if text.get(pos+"-1c",pos+"+"+str(len(s)+1)+"c").strip(" +=\n\t:(.") == str(s):
                        text.tag_add("builtin",pos,pos+"+"+str(len(s))+"c")
                #print(pos)
                start = pos + "+1c"
