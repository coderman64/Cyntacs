from tkinter import *
import keyword
import threading
import os
import os.path
import sys

defLists = {}
currentPath = os.path.realpath(sys.argv[0]);
if currentPath.rfind("/") != -1:
    currentPath = currentPath[:currentPath.rfind("/")]
else:
    currentPath = currentPath[:currentPath.rfind("\\")]
os.chdir(currentPath);

syntaxDefinitionFile = open("SyntaxDefs.txt")
synDef = syntaxDefinitionFile.read()
"""
structure:
{".filetype":[("color",[items]),("color",[items])]}
"""
syntaxDefs = {}
for ruleset in synDef.split("["):
    index = ruleset.find(']')
    filetypes = ruleset[:index].split(',')
    rules = []
    number = 0
    for rule in ruleset[index:].split('\n'):
        if rule.startswith(">") != -1:
            index2 = rule.find(":")
            color12 = rule[1:index2]
            syntax = rule[index2+1:].split(",")
            rules.append((color12,syntax));
            number += 1
    for ft in filetypes:
        ft = ft.strip(" ")
        syntaxDefs[ft] = rules;
        print(str(ft)+": "+str(rules))

class syntaxHighlighter:
    def __init__(self):
        self.thread12 = None
        self.threadOpen12 = False
    def highlightSyntax(self, text, filename):
        if self.threadOpen12 == False:
            self.thread12 = threading.Thread(target = lambda: self.highlightSyntaxSub(text, filename))
            self.thread12.start()
            self.threadOpen12 = True

    def highlightSyntaxSub(self, text, filename):
        index = filename.rfind(".")
        print("hi")
        try:
            syntaxDefs[str(filename[index:])]
            for rule in syntaxDefs[str(filename[index:])]:
                text.tag_delete(rule[0])
                text.tag_configure(rule[0], foreground=rule[0])
                #print(rule[1])
                for item in rule[1]:
                    item = item.strip()
                    start = 1.0
                    if item.find("+*+") != -1:
                        try:
                            while 1:
                                pos2 = "1.0"
                                pos = text.search(item[:item.find("+")], start, stopindex=END)
                                if not pos:
                                    break
                                else:
                                    pos2 = text.search(item[item.rfind("+")+1:].replace("\\n","\n"), pos+"+1c", stopindex=END)
                                    if pos2 != "":
                                        text.tag_add(rule[0],pos,pos2+"+"+str(len(item[item.rfind("+")+1:].replace("\\n","\n")))+"c")
                                #print(pos)
                                start = pos2 + "+1c"
                                if self.threadOpen12 == False:
                                    break
                                    print("thread Ending 1a");
                        except:
                            pass
                    elif item.find("-*-") != -1:
                        try:
                            while 1:
                                pos2 = "1.0"
                                pos = text.search(item[:item.find("-")], start, stopindex=END)
                                if not pos:
                                    break
                                else:
                                    pos2 = text.search(item[item.rfind("-")+1:].replace("\\n","\n"), pos+"+1c", stopindex=END)
                                    if pos2 != "":
                                        text.tag_add(rule[0],pos+"+"+str(len(item[:item.find("-")]))+"c",pos2)
                                #print(pos)
                                start = pos2 + "+1c"
                                if self.threadOpen12 == False:
                                    break
                                    print("thread Ending 1b");
                        except:
                            pass
                    else:
                        try:
                            while 1:
                                pos = text.search(item, start, stopindex=END)
                                if not pos:
                                    break
                                else:
                                    if text.get(pos+"wordstart",pos+"wordend") == str(item):
                                        text.tag_add(rule[0],pos,pos+"wordend")
                                #print(pos)
                                start = pos + "+1c"
                                if self.threadOpen12 == False:
                                    break
                                    print("thread Ending 1c");
                        except:
                            pass
                    if self.threadOpen12 == False:
                        break
                        print("thread Ending 2");
                
        except KeyError:
            print("dunno filetype: "+str(filename[index:]))
        print("Highlighting Finished");
        self.threadOpen12 = False
    """text.tag_delete("keyword")
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
                if text.get(pos+"-1c",pos+"wordend").strip(" \n\t:") == str(s):
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
                if text.get(pos+"-1c",pos+"wordend").strip(" +=\n\t:(.") == str(s):
                    text.tag_add("builtin",pos,pos+"+"+str(len(s))+"c")
            #print(pos)
            start = pos + "+1c"""
              


