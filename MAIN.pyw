from tkinter import *
from tkinter.filedialog import *
import os
from SyntaxHighlighting import *

# not quite sure what this does yet...
fileName = "New"
loadText = ""
load2 = False

class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        #basic variables
        self.saveFile = "New" #this stores the file name of the currently open file

        #widgets
        self.scrollbar = Scrollbar(self)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.numbers = Text(self, bg = "lightgrey", width = 4, state=DISABLED)
        self.numbers.pack(side = LEFT, anchor="nw", fill=Y)

        self.textArea = Text(self, wrap = NONE, maxundo = 20, undo = 1)
        self.textArea.pack(fill = BOTH, expand=1)
        self.current = self.textArea.get("0.0",END)

        self.iconbitmap("Logo2.ico")

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

        self.menubar = Menu(self)
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.openFile)
        self.bind("<Control-o>", self.openFile)
        filemenu.add_command(label="Save", command=self.fileSave)
        self.bind("<Control-s>", lambda e: self.fileSave())
        filemenu.add_command(label="Save As", command=self.saveAsFile)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.exitCyntacs)
        self.menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.undo)
        self.bind("<Control-z>", lambda e: self.undo())
        editmenu.add_command(label="Redo", command=self.redo)
        self.bind("<Control-y>", lambda e: self.redo())
        self.menubar.add_cascade(label = "Edit", menu = editmenu)
        self.config(menu = self.menubar)

        self.title(string = "Cyntacs - "+str(self.saveFile)) #changes the title

        self.file_opt = options = {}
        options['filetypes'] = [('all files', '.*'), ('text files', '.txt'), ('python script','.py .pyw')]
        options['initialfile'] = 'myfile.txt'
        options['parent'] = self
        
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
                warn.wait_window(warn)
        self.updateNumbers();
        highlightSyntax(self.textArea, self.saveFile)
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
            highlightSyntax(self.textArea, self.saveFile)
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
