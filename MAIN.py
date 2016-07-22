from tkinter import *
from tkinter.filedialog import *
import os
oldpath = os.getcwd()
from SyntaxHighlighting import *
import sys
import time

currentPath = os.path.realpath(sys.argv[0]);
if currentPath.rfind("/") != -1:
    currentPath = currentPath[:currentPath.rfind("/")]
else:
    currentPath = currentPath[:currentPath.rfind("\\")]

# not quite sure what this does yet...
fileName = "New"
loadText = ""
load2 = False

class App(Tk):
    def __init__(self):
        os.chdir(currentPath)
        Tk.__init__(self)

        #basic variables
        self.saveFile = "New" #this stores the file name of the currently open file

        self.synHlght = syntaxHighlighter()
        #widgets
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.numbers = Text(self, bg = "lightgrey", width = 4, state=DISABLED)
        self.numbers.pack(side = LEFT, anchor="nw", fill=Y)

        self.textArea = Text(self, wrap = NONE, maxundo = 30, undo = 1,tabs="    ")
        self.textArea.pack(fill = BOTH, expand=1)
        self.current = self.textArea.get("0.0",END)

        self.iconbitmap("Logo2.ico")
        
        """if len(sys.argv) > 1:
            self.saveFile = sys.argv[1]
            self.title(string = "Cyntacs - "+str(self.saveFile))
            file = open(sys.argv[1])
            self.textArea.delete("0.0",END)
            self.textArea.insert("0.0",file.read())
            self.current = self.textArea.get("0.0",END)
            self.updateNumbers();
            self.synHlght.highlightSyntax(self.textArea, self.saveFile)"""
        if len(sys.argv) > 1:
            print("opening a file passed as an argument...");
            os.chdir(oldpath);
            self.saveFile = sys.argv[len(sys.argv)-1]
            self.title(string = "Cyntacs - "+str(self.saveFile))
            file = open(sys.argv[len(sys.argv)-1])
            os.chdir(currentPath)
            self.textArea.delete("0.0",END)
            self.textArea.insert("0.0",file.read())
            self.current = self.textArea.get("0.0",END)
            self.updateNumbers();
            self.synHlght.highlightSyntax(self.textArea, self.saveFile)
        

        def scrollAll(a1=None, a2=None):
            self.scrollbar.set(a1,a2);
            currentScroll = self.scrollbar.get()
            self.numbers.yview_moveto(currentScroll[0])
            self.textArea.yview_moveto(currentScroll[0])

        def dualscroll(a1=None,a2=None,a3=None,a4=None):
            self.textArea.yview(a1,a2,a3,a4);
            self.numbers.yview(a1,a2,a3,a4);

        self.scrollbar.config(command=dualscroll)#connect the scrollbar
        self.textArea.config(yscrollcommand = scrollAll, maxundo = 20)
        self.numbers.config(yscrollcommand = scrollAll)

        #menu
        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        #'file' cascade
        filemenu.add_command(label="Open", command=self.openFile)
        self.bind("<Control-o>", lambda e: self.openFile())
        filemenu.add_command(label="Save", command=self.fileSave)
        self.bind("<Control-s>", lambda e: self.fileSave())
        filemenu.add_command(label="Save As", command=self.saveAsFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exitCyntacs)
        self.menubar.add_cascade(label="File", menu=filemenu)
        #'edit' cascade
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.undo)
        self.bind("<Control-z>", lambda e: self.undo())
        editmenu.add_command(label="Redo", command=self.redo)
        self.bind("<Control-y>", lambda e: self.redo())
        self.menubar.add_cascade(label = "Edit", menu = editmenu)
        #'help' cascade
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="about", command=self.aboutDialog);
        self.menubar.add_cascade(label = 'Help', menu = helpmenu);
        #add menubar to window
        self.config(menu = self.menubar)
        

        self.title(string = "Cyntacs - "+str(self.saveFile)) #changes the title

        self.file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt'), ('python script','.py .pyw'), ('HTML (Hyper-Text Markup Language) file','.html .htm')]
        options['initialfile'] = 'myfile.txt'
        options['parent'] = self

        self.syntaxTimer = 0;
        
        self.after(10, self.checkModified)
        
        self.mainloop()

    def undo(self):
        try:
            self.textArea.edit_undo()
        except:
            pass
    def redo(self):
        try:
            self.textArea.edit_redo()
        except:
            pass
    def aboutDialog(self):
        warn = Toplevel(master = self)
        warn.title(string="About Cyntacs")
        warn.resizable(width = False, height = False)
        warn.transient(master = self)
        Label(warn, text = "Cyntacs\nversion: 0.5\n\n(c) Coderman64 2016\n http://coderman64.github.io/").pack()
        Button(warn, text = "OK", command = warn.destroy, default=ACTIVE, width=10).pack()
        warn.grab_set()
        self.focus_set()
        self.wait_window(warn)
    def openFile(self):
        dialogResult = askopenfilename(**self.file_opt)
        if dialogResult != "":
            try:
                self.saveFile = dialogResult
                self.title(string = "Cyntacs - "+str(self.saveFile))
                file = open(dialogResult)
                self.textArea.delete("0.0",END)
                self.textArea.insert("0.0",file.read())
                self.current = self.textArea.get("0.0",END)
            except FileNotFoundError:
                warn = Toplevel(master = self)
                warn.title(string="ERROR")
                warn.resizable(width = False, height = False)
                warn.transient(master = self)
                warn.grab_set()
                Label(warn, text = "File not found:\n %s" % dialogResult).pack()
                Button(warn, text = "OK", command = warn.destroy, default=ACTIVE, width=10).pack()
                self.wait_window(warn)
        self.updateNumbers();
        self.synHlght.highlightSyntax(self.textArea, self.saveFile)
    def fileSave(self):
        if self.saveFile == "New":
            self.saveAsFile()
        else:
            try:
                file = open(self.saveFile, mode='w')
            except FileNotFoundError:
                file = open(self.saveFile, mode='x')
            file.write(self.current)
            self.title(string = "Cyntacs - "+str(self.saveFile))
    def saveAsFile(self):
        dial = asksaveasfilename(**self.file_opt)
        if dial != "":
            self.saveFile = dial
            self.title(string = "Cyntacs - "+str(self.saveFile))
            try:
                file = open(dial, mode='w')
            except FileNotFoundError:
                file = open(dial, mode='x')
            file.write(self.textArea.get("0.0",END))
        self.updateNumbers()
    def exitCyntacs(self):
        self.quit()
        self.destroy()
    def checkModified(self):
        fileName = self.saveFile;
        now = self.textArea.get("0.0",END)
        if now != self.current:
            self.title(string = "* Cyntacs - "+str(self.saveFile)+" *")# changes the title if the file is not saved
            self.current = now
            self.updateNumbers()
            self.textArea.see(INSERT)
            self.numbers.see(self.textArea.index(INSERT))
            self.syntaxTimer = 0;
            self.synHlght.threadOpen12 = False;
        if self.syntaxTimer == 100:
            # this is supposed to call the syntax highlighter a full second after a user stops typing
            # this is supposed to prevent problems that result from the user editing the text while the syntax highlighter is running
            print("Activating Highlighter");
            self.synHlght.highlightSyntax(self.textArea, self.saveFile)
        self.syntaxTimer += 1;
        self.after(10, self.checkModified)#calls itself again after 10 milliseconds
    def updateNumbers(self):
        now = self.textArea.get("0.0",END)
        self.numbers.config(state = NORMAL)
        self.numbers.delete("0.0",END);
        for i in range(0, str(now).count("\n")):
            if i > 0:
                self.numbers.insert(END,"\n")
            self.numbers.insert(END,str(i+1))
        self.numbers.config(state = DISABLED);

root = App()
time.sleep(1);
