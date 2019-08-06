"""
telnetToolGui class is responsible for displaying tkinter GUI. Inisde the class
    there is an object of telnetThread class initiated.

Instance of telnetToolGui class is created in 3tpy.py

Created in python 3.2.3.
Author: Marcin Kowalczyk
Website: http://sourceforge.net/projects/three-t-py/


3Tpy - Telnet Testing Tool
Copyright (C) 2013 Marcin Kowalczyk

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter.ttk import *
from fileinput import *
from myTelnet import *
from telnetThread import *
import sys
import webbrowser

class telnetToolGui(object):

    def __init__(self, master,mytelnet):
        self.customizeWindowIconAndTitle(master,"3Tpy - Telnet Testing Tool")
        self.root = master
        self.root.resizable(False,False)
        self.getMyTelnetHandler(mytelnet)
        self.currentFilePath = ""
        self.currentFileChanged = False
        self.initiateGui()
        self.insertCommandsIntoTree()
        self.setOptionsOnNew()
        self.setEntryAndComboOnLoad()
        self.currentFileChanged = False

    def initiateGui(self):
        self.topButtonsFrame = Labelframe(self.root, text="File, run and info")
        self.topButtonsFrame.pack(side=TOP,fill=X)
        topButtonsPadx = 13
        self.buttonNew = Button(self.topButtonsFrame, text="New", command=self.newBtnAction)
        self.buttonNew.pack(side=LEFT,padx=topButtonsPadx)
        self.buttonLoad = Button(self.topButtonsFrame, text="Load", command=self.loadBtnAction)
        self.buttonLoad.pack(side=LEFT,padx=topButtonsPadx)
        self.buttonSave = Button(self.topButtonsFrame, text="Save", command=self.saveBtnAction)
        self.buttonSave.pack(side=LEFT,padx=topButtonsPadx)
        self.buttonSaveAs = Button(self.topButtonsFrame, text="Save as", command=self.saveAsBtnAction)
        self.buttonSaveAs.pack(side=LEFT,padx=topButtonsPadx)
        self.buttonRun = Button(self.topButtonsFrame, text="Run!", command=self.runFromGui)
        self.buttonRun.pack(side=LEFT,padx=topButtonsPadx)
        self.buttonHelp = Button(self.topButtonsFrame, text="Help", command=self.displayHelp)
        self.buttonHelp.pack(side=LEFT,padx=topButtonsPadx)
        self.buttonAbout = Button(self.topButtonsFrame, text="About", command=self.displayAboutMsg)
        self.buttonAbout.pack(side=LEFT,padx=topButtonsPadx)
        self.buttonQuit = Button(self.topButtonsFrame, text="Quit", command=self.quitGui)
        self.buttonQuit.pack(side=LEFT,padx=topButtonsPadx)
        self.configFrame = Labelframe(self.root, text="Test configuration")
        self.configFrame.pack(side=TOP,fill=X)
        self.configLabel = Label(self.configFrame, text="Options :  ")
        self.configLabel.pack(side=LEFT, padx=10)
        self.configComboVar = StringVar()
        self.configCombo = Combobox(self.configFrame, textvariable=self.configComboVar)
        self.configCombo.pack(side=LEFT)
        self.configCombo.bind('<<ComboboxSelected>>', self.configComboBoxEvent)
        self.configCombo['values'] = ("ipaddress","username","password","loginprompt","passprompt","regularprompt")
        self.configCombo.state(['!disabled'])
        self.configEntryVar = StringVar()
        self.configEntryVar.trace("w",self.configChange)
        self.configEntry = Entry(self.configFrame, textvariable=self.configEntryVar)
        self.configEntryVar.set("")
        self.configEntry.pack(side=LEFT, padx=10)
        self.treeFrame = Frame(self.root)
        self.treeFrame.pack(side=TOP, pady=8)
        self.treeScroll = Scrollbar(self.treeFrame)
        self.treeScroll.pack(side=RIGHT, fill=Y)
        self.treeview = Treeview(self.treeFrame,columns=["exp","soe","res"], yscrollcommand = self.treeScroll.set)
        self.treeview.heading("#0", text="Command")
        self.treeview.heading("exp", text="Expected")
        self.treeview.heading("soe", text="Stop on error")
        self.treeview.heading("res", text="Result")
        self.treeview.bind("<Double-1>", self.treeDoubleClick)
        self.treeview.pack(side=LEFT, fill=BOTH)
        self.treeScroll.config(command=self.treeview.yview)
        self.bottomButtonsFrame = Labelframe(self.root, text="Test commands operations")
        self.bottomButtonsFrame.pack(side=TOP,fill=X)
        bottomButtonsPadx = 43
        self.buttonCommandAdd = Button(self.bottomButtonsFrame, text="Add", command=self.commandAdd)
        self.buttonCommandAdd.pack(side=LEFT,padx=bottomButtonsPadx)
        self.buttonCommandModify = Button(self.bottomButtonsFrame, text="Modify", command=self.commandModify)
        self.buttonCommandModify.pack(side=LEFT,padx=bottomButtonsPadx)
        self.buttonCommandMoveUp = Button(self.bottomButtonsFrame, text="MoveUp", command=self.commandMoveUp)
        self.buttonCommandMoveUp.pack(side=LEFT,padx=bottomButtonsPadx)
        self.buttonCommandMoveDown = Button(self.bottomButtonsFrame, text="MoveDown", command=self.commandMoveDown)
        self.buttonCommandMoveDown.pack(side=LEFT,padx=bottomButtonsPadx)
        self.buttonCommandDelete = Button(self.bottomButtonsFrame, text="Delete", command=self.commandDelete)
        self.buttonCommandDelete.pack(side=LEFT,padx=bottomButtonsPadx)

    def setStyling(self,style):
        self.ttkStyle = tkinter.ttk.Style()
        if(style in self.ttkStyle.theme_names()):
            self.ttkStyle.theme_use(style)

    def customizeWindowIconAndTitle(self,window,title):
        window.title(title)
        if(sys.platform=="win32"):
            try:
                window.iconbitmap('3Tpy.ico')
                self.setStyling('xpnative')
            except TclError:
                pass
        elif(sys.platform=="linux2"):
             try:
                self.setStyling('classic')
             except TclError:
                pass

    def getMyTelnetHandler(self,mytelnet):
        self.mytelnet = mytelnet

    def displayAboutMsg(self):
        aboutMsg = "3Tpy - python Telnet Testing Tool\n"
        aboutMsg = aboutMsg + "version 1.0 (released in March 2013)\n"
        aboutMsg = aboutMsg + "requires python 3.2.3 or higher\n"
        aboutMsg = aboutMsg + "website: http://sourceforge.net/projects/three-t-py/\n"
        aboutMsg = aboutMsg + "license: GNU GPLv3 (available in project directory)\n"
        aboutMsg = aboutMsg + "author: Marcin Kowalczyk\n"
        messagebox.showinfo("About 3Tpy",aboutMsg)

    def loadBtnAction(self):
        self.askIfSaveChangedFile()
        someFileName = filedialog.askopenfilename(parent=self.root,defaultextension='.xml',filetypes=[("xml", ".xml")],title='Choose a file')
        if(someFileName!=""):
            getXmlRes = self.mytelnet.getXml(someFileName)
            if(getXmlRes):
                self.insertCommandsIntoTree()
                self.setEntryAndComboOnLoad()
                self.currentFilePath = someFileName
                self.currentFileChanged = False
                self.configCombo.state(['!disabled'])
            else:
                messagebox.showwarning("Warning","Error while trying to open XML file")

    def displayHelp(self):
        linkToHelpPage = 'http://sourceforge.net/p/three-t-py/wiki/Home/'
        webbrowser.open(linkToHelpPage)

    def newBtnAction(self):
        self.askIfSaveChangedFile()
        self.currentFileChanged = True
        self.currentFilePath = ""
        self.mytelnet.clearCommands()
        self.mytelnet.clearConfig()
        self.clearTree()
        self.configCombo.state(['!disabled'])
        self.setOptionsOnNew()
        self.setEntryAndComboOnLoad()

    def setOptionsOnNew(self):
        self.mytelnet.setLoginPrompt("login:")
        self.mytelnet.setPasswordPrompt("password:")
        self.mytelnet.setDefaultPrompt("$")
        self.mytelnet.setHost("0.0.0.0")
        self.mytelnet.setUsr("user name")
        self.mytelnet.setPswd("password")

    def saveBtnAction(self):
        if(self.currentFileChanged):
            self.currentFileChanged = False
            if(self.currentFilePath==""):
                someFileName = filedialog.asksaveasfilename(parent=self.root,defaultextension='.xml',filetypes=[("xml", ".xml")],title='Choose a file or type new name')
                if(someFileName!=""):
                    saveRetVal = self.mytelnet.saveXml(someFileName)
                    if(saveRetVal!=""):
                        messagebox.showerror("File not saved",saveRetVal)
                    else:
                        self.currentFileChanged = False
                        self.currentFilePath = someFileName
                else:
                    messagebox.showwarning("File not saved","Invalid file path")
            else:
                saveRetVal = self.mytelnet.saveXml(self.currentFilePath)
                if(saveRetVal!=""):
                    messagebox.showerror("File not saved",saveRetVal)
        else:
            messagebox.showwarning("File not saved","Nothing was changed")

    def saveAsBtnAction(self):
        someFileName = filedialog.asksaveasfilename(parent=self.root,defaultextension='.xml',filetypes=[("xml", ".xml")],title='Choose a file or type new name')
        if(someFileName!=""):
            saveRetVal = self.mytelnet.saveXml(someFileName)
            if(saveRetVal!=""):
                messagebox.showerror("File not saved",saveRetVal)
            else:
                self.currentFileChanged = False
                self.currentFilePath = someFileName
        else:
            messagebox.showwarning("File not saved","Invalid file path")

    def threadCheck(self):
        thread = telnetThread()
        thread.setMyTelnetHandler(self.mytelnet)
        self.mytelnet.initiateGuiHandlers(treeview=self.treeview)
        thread.start()

    def runFromGui(self):
        if(len(self.mytelnet.commandsList)>0):
            self.logWindow = Toplevel(self.root)
            self.logWindow.protocol("WM_DELETE_WINDOW",self.logWindowClose)
            self.logWindow.resizable(False,False)
            self.customizeWindowIconAndTitle(self.logWindow,"Test run log")
            logVar = StringVar()
            Label(self.logWindow, textvariable=logVar).pack()
            self.calculateProgressStep()
            testprogress = Progressbar(self.logWindow, maximum=self.mytelnet.progressBarMax, length=300)
            testprogress.pack()
            logWindowCloseBtn = Button(self.logWindow, text="Close", command=self.logWindowClose)
            logWindowCloseBtn.pack(side=BOTTOM)
            textScroll = Scrollbar(self.logWindow, orient=VERTICAL)
            textScroll.pack(side=RIGHT, fill=Y)
            logTextBox = Text(self.logWindow, width=80, height=40, yscrollcommand = textScroll.set)
            textScroll['command'] = logTextBox.yview
            logTextBox.pack(side=LEFT, fill=BOTH)
            logTextBox.tag_configure('warn_tag',foreground='red')
            logTextBox.tag_configure('100_tag',foreground='#00cc00')
            logTextBox.tag_configure('timer_tag',foreground='blue')
            self.logWindow.transient(self.root)
            self.mytelnet.initiateGuiHandlers(treeview=self.treeview, text=logTextBox, label=logVar, progress=testprogress)
            self.mytelnet.cleanTestRunVariables()
            self.mytelnet.initiateLogName()
            self.mytelnet.initiateLogging()
            self.telThread = telnetThread()
            self.telThread.setMyTelnetHandler(self.mytelnet)
            self.telThread.start()
            self.logWindow.grab_set()
        else:
            messagebox.showwarning("Tests not started","No commands to run")

    def calculateProgressStep(self):
        self.mytelnet.progressBarMax = 1000
        self.mytelnet.progressStep = 0
        self.mytelnet.totalProgress = 0
        howManyCommands = len(self.mytelnet.commandsList)
        if(howManyCommands>0):
            self.mytelnet.progressStep = self.mytelnet.progressBarMax//howManyCommands
        if(self.mytelnet.progressStep==self.mytelnet.progressBarMax):
            self.mytelnet.progressStep = self.mytelnet.progressStep - 1

    def logWindowClose(self):
        if(not self.telThread.isAlive()):
            self.logWindow.destroy()

    def quitGui(self):
        self.askIfSaveChangedFile()
        self.root.quit()

    def askIfSaveChangedFile(self):
        if(self.currentFileChanged):
            if(messagebox.askyesno("Save a file?","File was changed. Should it be saved?")):
                if(self.currentFilePath==""):
                    self.saveAsBtnAction()
                else:
                    self.saveBtnAction()

    def insertCommandsIntoTree(self):
        self.clearTree()
        for i in self.mytelnet.commandsList:
            self.treeview.insert("","end",text=str(i.command),values=[i.expected,i.stopOnError,"not run"])

    def clearTree(self):
        for i in self.treeview.get_children():
            self.treeview.delete(i)

    def displayOptionsInEntry(self,option):
        if(option=="ipaddress"):
            self.configEntryVar.set(self.mytelnet.getHost())
        elif(option=="username"):
            self.configEntryVar.set(self.mytelnet.getUsr())
        elif(option=="password"):
            self.configEntryVar.set(self.mytelnet.getPswd())
        elif(option=="loginprompt"):
            self.configEntryVar.set(self.mytelnet.getLoginPrompt())
        elif(option=="passprompt"):
            self.configEntryVar.set(self.mytelnet.getPasswordPrompt())
        elif(option=="regularprompt"):
            self.configEntryVar.set(self.mytelnet.getDefaultPrompt())
        else:
            self.configEntryVar.set("")

    def setEntryAndComboOnLoad(self):
        self.configCombo.current(5)
        self.displayOptionsInEntry(self.configCombo.get())

    def getTreeSelection(self):
        selectionDict = {"item":"","itemId":"","command":"","expected":"","soe":""}
        selectedItem = self.treeview.selection()
        if(selectedItem!="" and len(selectedItem)==1):
            selectedItemIndex = self.treeview.index(selectedItem)
            selectionDict["item"] = selectedItem
            selectionDict["itemId"] = selectedItemIndex
            selectionDict["command"] = self.treeview.item(selectedItem,option="text")
            selectionDict["expected"] = self.treeview.item(selectedItem,option="values")[0]
            selectionDict["soe"] = self.treeview.item(selectedItem,option="values")[1]
            selectionDict["result"] = self.treeview.item(selectedItem,option="values")[2]
        return selectionDict

    def commandAdd(self):
        self.treeview.insert("","end",text="new",values=["new","False","not run"])
        self.mytelnet.addCommandTolist("","","")
        self.currentFileChanged = True

    def commandModify(self):
        selectedDict = self.getTreeSelection()
        if(selectedDict["item"]!="" and selectedDict["itemId"]!=""):
            self.modifyWindow = Toplevel(self.root)
            self.customizeWindowIconAndTitle(self.modifyWindow,"Modify command")
            Label(self.modifyWindow, text="Command").pack()
            entryWidgetsWidth=23
            self.commandEntry = Entry(self.modifyWindow, width=entryWidgetsWidth)
            self.commandEntry.pack()
            Label(self.modifyWindow, text="Expected").pack()
            self.commandExpEntry = Entry(self.modifyWindow, width=entryWidgetsWidth)
            self.commandExpEntry.pack()
            Label(self.modifyWindow, text="Stop on error").pack()
            self.modifyComboVar = StringVar()
            self.modifyCombo = Combobox(self.modifyWindow, textvariable=self.modifyComboVar)
            self.modifyCombo.pack()
            self.modifyCombo.bind('<<ComboboxSelected2>>')
            self.modifyCombo['values'] = ("True","False")
            self.putCommandIntoWindow()
            self.modifyConfirmBtn = Button(self.modifyWindow, text="OK", command=self.modifyConfirm)
            self.modifyConfirmBtn.pack(pady=3)
            self.modifyCancelBtn = Button(self.modifyWindow, text="Cancel", command=self.modifyCancel)
            self.modifyCancelBtn.pack()
            self.modifyWindow.transient(self.root)
            self.modifyWindow.grab_set()
            self.root.wait_window(self.modifyWindow)

    def modifyConfirm(self):
        self.getCommandFromWindow()
        self.modifyWindow.destroy()

    def modifyCancel(self):
        self.modifyWindow.destroy()

    def putCommandIntoWindow(self):
        selection = self.getTreeSelection()
        self.commandEntry.insert(0,selection["command"])
        self.commandExpEntry.insert(0,selection["expected"])
        if(selection["soe"]=="True"):
            self.modifyCombo.current(0)
        else:
            self.modifyCombo.current(1)

    def getCommandFromWindow(self):
        updatedCommand = self.commandEntry.get()
        updatedExp = self.commandExpEntry.get()
        updatedSoe = self.modifyCombo.get()
        selectedItem = self.treeview.selection()
        selectedItemIndex = self.treeview.index(selectedItem)
        self.treeview.item(selectedItem,text=str(updatedCommand),values=[updatedExp,updatedSoe,"not run"])
        self.mytelnet.updateCommand(selectedItemIndex,updatedCommand,updatedExp,updatedSoe)
        self.currentFileChanged = True

    def commandMoveUp(self):
        selectedDict = self.getTreeSelection()
        if(selectedDict["item"]!="" and selectedDict["itemId"]!=""):
            self.treeview.move(selectedDict["item"],"",selectedDict["itemId"]-1)
            self.mytelnet.moveCommandsInAList(selectedDict["itemId"],"up")
            self.currentFileChanged = True

    def commandMoveDown(self):
        selectedDict = self.getTreeSelection()
        if(selectedDict["item"]!="" and selectedDict["itemId"]!=""):
            self.treeview.move(selectedDict["item"],"",selectedDict["itemId"]+1)
            self.mytelnet.moveCommandsInAList(selectedDict["itemId"],"down")
            self.currentFileChanged = True

    def commandDelete(self):
        selectedDict = self.getTreeSelection()
        if(selectedDict["item"]!="" and selectedDict["itemId"]!=""):
            self.treeview.delete(selectedDict["item"])
            self.mytelnet.deleteOneCommand(selectedDict["itemId"])
            self.currentFileChanged = True

    def configChange(self, *args):
        self.configModify(comboChoice=self.configCombo.get(),entryChoice=self.configEntryVar.get())

    def configModify(self, **kwargs):
        thisOption = kwargs['comboChoice']
        entryValue = kwargs['entryChoice']
        if(thisOption=="ipaddress"):
            self.mytelnet.setHost(entryValue)
            self.currentFileChanged = True
        if(thisOption=="username"):
            self.mytelnet.setUsr(entryValue)
            self.currentFileChanged = True
        if(thisOption=="password"):
            self.mytelnet.setPswd(entryValue)
            self.currentFileChanged = True
        if(thisOption=="loginprompt"):
            self.mytelnet.setLoginPrompt(entryValue)
            self.currentFileChanged = True
        if(thisOption=="passprompt"):
            self.mytelnet.setPasswordPrompt(entryValue)
            self.currentFileChanged = True
        if(thisOption=="regularprompt"):
            self.mytelnet.setDefaultPrompt(entryValue)
            self.currentFileChanged = True

    def configComboBoxEvent(self,event):
        self.displayOptionsInEntry(self.configCombo.get())

    def treeDoubleClick(self,event):
        clickedItem = self.treeview.identify('item',event.x,event.y)
        if(len(self.treeview.item(clickedItem,option="values"))>2):
            if(self.treeview.item(clickedItem,option="values")[2]!=""):
                self.commandModify()
