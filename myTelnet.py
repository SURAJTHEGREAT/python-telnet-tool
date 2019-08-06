"""
About myTelnet class:
    * performs all telnet operations using telnetlib
    * contains all configuration paramters
    * contains a list of commands (test cases) -> list variable commandsList
    * handles logging
    * contains objects of telnetFiles and myTelnetCommand classes

Instance of myTelnet class is initiated in 3Tpy.py.

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

import telnetlib
import time
import re
import logging
import string
from myTelnetCommand import *
from telnetFiles import *
import tkinter

class myTelnet(object):
    def __init__(self):
        self.targetIP = ""
        self.userName = ""
        self.passwd = ""
        self.regularPrompt = ""
        # port is empty at start
        self.telnetPort=""
        self.cleanTestRunVariables()
        self.commandsList = []
        self.addPredefPrompts = False
        self.defaultLoginPrompts = []
        self.defaultPasswordPrompts = []
        self.executionTimeList = []
        self.useGui = False
        if(self.addPredefPrompts):
            self.addPredefinedPrompts()
        self.initiateLogName()
        self.timeout_sessionOpening = 10
        self.timeout_command = 7

    def cleanTestRunVariables(self):
        self.overAllResult = True
        self.interrupted = False
        self.passRate = 0
        self.numberOfSamples = 0

    def initiateLogName(self,**kwargs):
        if(len(kwargs)==0 or kwargs==None):
            self.logName =  time.strftime("%Y%b%d%a%H%M%S", time.localtime())
        elif('customLog' in kwargs):
            self.logName = kwargs['customLog']
        if(self.useGui):
            self.guiLabelVarHandler.set("Log file name: " + self.logName + ".log")

    def addPredefinedPrompts(self):
        self.defaultLoginPrompts = ["login".encode("utf_8"),":".encode("utf_8"),"Login".encode("utf_8"),"LOGIN".encode("utf_8")]
        self.defaultPasswordPrompts = ["password".encode("utf_8"),":".encode("utf_8"),"Password".encode("utf_8"),"PASSWORD".encode("utf_8")]

    def initiateLogging(self):
        logging.basicConfig(filename=self.logName + ".log",filemode='w', level=logging.INFO,format='%(asctime)s:%(levelname)s:%(message)s')
        self.myTelnetLogging("Starting test","info")

    def releaseLoggingHandlers(self):
        rootLoggingHandler = logging.getLogger()
        if rootLoggingHandler.handlers:
            for h in rootLoggingHandler.handlers:
                rootLoggingHandler.removeHandler(h)

    def setHost(self,host):
        self.targetIP = host

    def getHost(self):
        return self.targetIP

    # getter and setter for ports 
    def setPort(self,port):
        self.telnetPort = port

    def getPort(self):
        return self.telnetPort

    def setUsr(self,usr):
        self.userName =  usr

    def getUsr(self):
        return self.userName

    def getUsrUtf8(self):
        return ((self.userName + "\n").encode("utf_8"))

    def setPswd(self,pswd):
        self.passwd = pswd

    def getPswdUtf8(self):
        return ((self.passwd + "\n").encode("utf_8"))

    def getPswd(self):
        return self.passwd

    def startSession(self):
        try:
            self.telnet = telnetlib.Telnet(self.targetIP,self.telnetPort,self.timeout_sessionOpening)
            self.myTelnetLogging("Connecting to " + str(self.targetIP),"info")
            self.connected = True
        except:
            self.myTelnetLogging("Unable to connect " + str(self.targetIP),"warn")
            self.connected = False
            self.interrupted = True

    def endSession(self):
        if(self.connected):
            try:
                self.telnet.close()
                self.myTelnetLogging("Closing the session","info")
                self.connected = False
            except:
                self.myTelnetLogging("Exception occured while closing a session","warn")

    def setLoginPrompt(self,prompt):
        while(len(self.defaultLoginPrompts)):
            self.defaultLoginPrompts.pop()
        self.defaultLoginPrompts.append(prompt)

    def getLoginPrompts(self):
        return self.defaultLoginPrompts

    def getLoginPromptsUtf8(self):
        prompts = []
        for i in self.defaultLoginPrompts:
            prompts.append(i.encode("utf_8"))
        return prompts

    def getLoginPrompt(self):
        if(len(self.defaultLoginPrompts)>0):
            return self.defaultLoginPrompts[0]
        else:
            return ""

    def getLoginPromptUtf8(self):
        if(len(self.defaultLoginPrompts)>0):
            return self.defaultLoginPrompts[0].encode("utf_8")
        else:
            return ""

    def setDefaultPrompt(self,prompt):
        self.regularPrompt = prompt

    def getDefaultPrompt(self):
        return self.regularPrompt

    def getDefaultPromptUtf8(self):
        return ((self.regularPrompt).encode("utf_8"))

    def setPasswordPrompt(self,prompt):
        while(len(self.defaultPasswordPrompts)):
            self.defaultPasswordPrompts.pop()
        self.defaultPasswordPrompts.append(prompt)

    def getPasswordPrompts(self):
        return self.defaultPasswordPrompts

    def getPasswordPromptsUtf8(self):
        prompts = []
        for i in self.defaultPasswordPrompts:
            prompts.append(i.encode("utf_8"))
        return prompts

    def getPasswordPrompt(self):
        if(len(self.defaultPasswordPrompts)>0):
            return self.defaultPasswordPrompts[0]
        else:
            return ""

    def getPasswordPromptUtf8(self):
        if(len(self.defaultPasswordPrompts)>0):
            return self.defaultPasswordPrompts[0].encode("utf_8")
        else:
            return ""

    def log_in(self):
        if(self.connected):
            try:
                self.myTelnetLogging("Logging in","info")
                self.telnet.expect(self.getLoginPromptsUtf8(),self.timeout_command)
                self.telnet.write(self.getUsrUtf8())
                self.telnet.expect(self.getPasswordPromptsUtf8(),self.timeout_command)
                self.telnet.write(self.getPswdUtf8())
                loginOutput = self.telnet.read_until(self.getDefaultPromptUtf8(),self.timeout_command)
                promptToCompare = self.getDefaultPrompt()
                if(re.search("$",promptToCompare)):
                    promptToCompare = promptToCompare.replace("$","\$")
                if(re.search(promptToCompare,loginOutput.decode("utf_8"))):
                    self.myTelnetLogging("Logged in","info")
                else:
                    self.myTelnetLogging("Exception while logging in","warn")
                    self.connected = False
                    self.overAllResult = False
                    self.interrupted = True
            except:
                self.myTelnetLogging("Exception while logging in","warn")
                self.connected = False
                self.overAllResult = False
                self.interrupted = True

    def executeCommand(self,com,exp,soe):
        commandResult = True
        command = com + "\r\n"
        command = command.encode("utf_8")
        self.myTelnetLogging("Sending command {" + com + "} . Expected response is {" + exp + "}","info")
        try:
            #start timer
            startTime = time.time()
            self.telnet.write(command)
            output = self.telnet.read_until(self.getDefaultPromptUtf8(),self.timeout_command)
            #end timer
            endTime = time.time()
            # timer difference
            executionTime=endTime-startTime
            # add to list - to calculate total time taken to 
            # execute all commands
            self.executionTimeList.append(executionTime)
        except:
            commandResult = False
            self.connected = False
            self.overAllResult = False
            self.interrupted = True
        else:
            output = output.decode("utf_8")
            if(re.search(com,output)):
                if(com!=""):
                    output = output.split(com)[1]
                    #below ling is not needed
                    #.replace("\r\n","\n").replace("\r","\n").strip()
                    #only for validating
                    #self.myTelnetLogging(repr(output),"info")
            self.myTelnetLogging("Response: {" + output + "}","info")
            # log the execution time 
            self.myTelnetLogging("Execution time of above command is:{:.3f} sec".format(executionTime),"info")
            self.numberOfSamples = self.numberOfSamples + 1
            if(len(exp)>0):
                comparingString = "Comparing response with expected one. Result:"
                if(re.search(exp,output)):
                    commandResult = True
                    self.passRate = self.passRate + 1
                    self.myTelnetLogging(comparingString + str(commandResult),"info")
                else:
                    commandResult = False
                    self.myTelnetLogging(comparingString + str(commandResult),"warn")
            else:
                self.myTelnetLogging("Nothing compared","info")
                self.passRate = self.passRate + 1
            if(soe and not commandResult):
                self.overAllResult = False
        self.updateProgress()
        return commandResult

    def runCommandsFromList(self):
        treeItems = []
        executionTimeList=[]
        if(self.useGui):
            treeItems = self.guiTreeviewHandler.get_children()
            self.cleanAllTreeCommandResults(treeItems)
        commandIteration = 0
        for i in self.commandsList:
            if((self.overAllResult)and(self.connected)and(not self.interrupted)):
                comResult = self.executeCommand(i.command,i.expected,i.stopOnError)
                if(self.useGui):
                    if(self.interrupted):
                        self.updateTreeCommandResult("not run",treeItems[commandIteration])
                    else:
                        self.updateTreeCommandResult(comResult,treeItems[commandIteration])
            commandIteration = commandIteration + 1

    def updateTreeCommandResult(self,res,iitem):
        passOrNot ="fail"
        if(res=="not run"):
            passOrNot = res
        elif(res):
            passOrNot = "pass"
        exp = self.guiTreeviewHandler.item(iitem,option='values')[0]
        soe = self.guiTreeviewHandler.item(iitem,option='values')[1]
        self.guiTreeviewHandler.item(iitem,values=[exp,soe,passOrNot])

    def cleanAllTreeCommandResults(self,itemList):
        for i in itemList:
            self.updateTreeCommandResult("not run",i)

    def initiateGuiHandlers(self, **handlers):
        self.useGui = True
        if('treeview' in handlers):
            self.setTreeviewHandler(handlers['treeview'])
        if('text' in handlers):
            self.setTextHandler(handlers['text'])
        if('label' in handlers):
            self.setLabelVarHandler(handlers['label'])
        if('progress' in handlers):
            self.setProgressHanlder(handlers['progress'])

    def deactivateGui(self):
        self.useGui = False

    def setTreeviewHandler(self, treeHandler):
        self.guiTreeviewHandler = treeHandler

    def setTextHandler(self, textHandler):
        self.guiTextHandler = textHandler

    def setLabelVarHandler(self, labelVar):
        self.guiLabelVarHandler = labelVar

    def setProgressHanlder(self, progrBar):
        self.guiProgressHandler = progrBar

    def addCommandTolist(self,com,exp,soe):
        self.commandsList.append(myTelnetCommand(com,exp,soe))

    def convertLogIntoHtml(self):
        htmlFile = open(self.logName + ".html","w")
        logFile = open(self.logName + ".log","r")
        logLines = logFile.readlines()
        htmlContents = "<html><head><title>" + self.logName + "</title></head><body>\n<table>\n"
        htmlColor = 0
        for i in logLines:
            if(re.search(":INFO:",i) or re.search(":WARNING:",i)):
                htmlContents = htmlContents + "</td></tr>\n<tr><td bgcolor="
                if(htmlColor==0):
                    htmlContents = htmlContents + "#E0E0E0>"
                    htmlColor = 1
                else:
                    htmlContents = htmlContents + "#F0F0F0>"
                    htmlColor = 0
            if(re.search(":WARNING:",i)):
                htmlContents = htmlContents + "<font color=red>"
            elif(re.search("Scenario pass rate equals",i)):
                htmlContents = htmlContents + "<font color=green>"
            # if the execution time pattern is available , font color is blue in html    
            elif(re.search("Execution time",i)):
                htmlContents = htmlContents + "<font color=blue>"
            htmlContents = htmlContents + i
        htmlContents = htmlContents + "</font></table></body></html>"
        htmlFile.write(htmlContents)
        htmlFile.close()
        logFile.close()

    def calculateFinalResult(self):
        # calculate the total time for execution
        self.myTelnetLogging("Total Execution time is:{:.3f} sec".format(sum(self.executionTimeList)),"info")
        #clear the list
        self.executionTimeList.clear()
        if(self.interrupted):
            self.myTelnetLogging("The test was interrupted","warn")
        else:
            if(self.numberOfSamples>0):
                psrt = (self.passRate/self.numberOfSamples)*100
                passString = "{0:.0f}".format(psrt)
                passString = "Scenario pass rate equals " + passString + "%"
                if(psrt>=95):
                    self.myTelnetLogging(passString,"info")
                else:
                    self.myTelnetLogging(passString,"warn")
            else:
                self.myTelnetLogging("Pass rate can't be calculated (no checks were performed)","info")

    def getXml(self,fileName):
        xmlRetVal = False
        tf = telnetFiles()
        self.clearCommands()
        self.clearOptions()
        if(tf.getXml(fileName)):
            if("ipaddress" in tf.confDict):
                self.setHost(tf.confDict["ipaddress"])
            else:
                self.setHost(tf.confDict[""])
            if("telnetPort" in tf.confDict):
                self.setPort(tf.confDict["telnetPort"])
            else:
                self.setPort(tf.confDict[""])    
            if("username" in tf.confDict):
                self.setUsr(tf.confDict["username"])
            else:
                self.setUsr("")
            if("password" in tf.confDict):
                self.setPswd(tf.confDict["password"])
            else:
                self.setPswd("")
            if("loginprompt" in tf.confDict):
                self.setLoginPrompt(tf.confDict["loginprompt"])
            else:
                self.setLoginPrompt("")
            if("passprompt" in tf.confDict):
                self.setPasswordPrompt(tf.confDict["passprompt"])
            else:
                self.setPasswordPrompt("")
            if("regularprompt" in tf.confDict):
                self.setDefaultPrompt(tf.confDict["regularprompt"])
            else:
                self.setDefaultPrompt("")
            for i in tf.commandDicts:
                xmlSoe = False
                if(i["soe"]=="True"):
                    xmlSoe = True
                self.commandsList.append(myTelnetCommand(i["send"],i["exp"],xmlSoe))
            xmlRetVal = True
        else:
            self.myTelnetLogging("XML file exception","warn")
            self.interrupted = True
            xmlRetVal = False
        return xmlRetVal

    def saveXml(self,filePath):
        tf = telnetFiles()
        tf.setCommandDicts(self.buildCommandDicts())
        tf.setConfDict(self.buildConfDict())
        return tf.saveXml(filePath)

    def buildCommandDicts(self):
        comDicts = []
        for i in self.commandsList:
            newDict = {'command':i.command,'expected':i.expected,'soe':i.stopOnError}
            comDicts.append(newDict)
        return comDicts

    def buildConfDict(self):
        # introduced the port parameter in dict
        confDict = {'host':self.getHost(),'port':self.getPort(),'name':self.getUsr(),'password':self.getPswd(),'login prompt':self.getLoginPrompt(),'password prompt':self.getPasswordPrompt(),'default prompt':self.getDefaultPrompt()}
        return confDict

    def clearOptions(self):
        while(len(self.defaultLoginPrompts)):
            self.defaultLoginPrompts.pop()
        while(len(self.defaultPasswordPrompts)):
            self.defaultPasswordPrompts.pop()
        if(self.addPredefPrompts):
            self.addPredefinedPrompts()

    def clearCommands(self):
        while(len(self.commandsList)>0):
            self.commandsList.pop()

    def clearConfig(self):
        self.setHost("")
        #clear the port when new button is clicked
        self.setPort("")
        self.setUsr("")
        self.setPswd("")
        self.setLoginPrompt("")
        self.setPasswordPrompt("")
        self.setDefaultPrompt("")

    def executeTestScenario(self):
        if(not self.interrupted):
            self.initiateLogging()
            self.startSession()
            self.log_in()
            self.runCommandsFromList()
            self.calculateFinalResult()
            self.endSession()
        self.convertLogIntoHtml()

    def printOptions(self):
        print("\nhost: "+self.getHost())
        print("\nport: "+self.getPort())
        print("\nuser name : "+self.getUsr())
        print("\npassword : "+self.getPswd())
        print("\nlogin prompt : "+self.getLoginPrompt())
        print("\npassword prompt : "+self.getPasswordPrompt())
        print("\ndefault prompt : "+self.getDefaultPrompt())

    def printCommands(self):
        for i in self.commandsList:
            print("\nCommand     "+i.command)
            print("\nExpected    "+i.expected)
            print("\nStopOnError "+i.stopOnError)

    def moveCommandsInAList(self,commandNumber,direction):
        if(direction=="up" and commandNumber>0):
           mtcTemp = myTelnetCommand(self.commandsList[commandNumber-1].command,self.commandsList[commandNumber-1].expected,self.commandsList[commandNumber-1].stopOnError)
           self.commandsList[commandNumber-1] = self.commandsList[commandNumber]
           self.commandsList[commandNumber] = mtcTemp
        elif(direction=="down" and commandNumber<(len(self.commandsList)-1)):
           mtcTemp = myTelnetCommand(self.commandsList[commandNumber+1].command,self.commandsList[commandNumber+1].expected,self.commandsList[commandNumber+1].stopOnError)
           self.commandsList[commandNumber+1] = self.commandsList[commandNumber]
           self.commandsList[commandNumber] = mtcTemp

    def deleteOneCommand(self,commandNumber):
        self.commandsList.pop(commandNumber)

    def updateCommand(self,commandNumber,com,exp,soe):
        self.commandsList[commandNumber].command = com
        self.commandsList[commandNumber].expected = exp
        self.commandsList[commandNumber].stopOnError = soe

    def myTelnetLogging(self,msg,logType):
        if(logType=="info"):
            logging.info(msg)
            if(self.useGui):
                if(re.search("Scenario pass rate equals 100",msg)):
                    self.guiTextHandler.insert(tkinter.END ,"info: " + msg + "\n",('100_tag'))
                elif(re.search("Execution time",msg)):
                    # for execution time , add the timer tag it comes from GUI file
                    self.guiTextHandler.insert(tkinter.END ,"info: " + msg + "\n",('timer_tag'))
                else:
                    self.guiTextHandler.insert(tkinter.END ,"info: " + msg + "\n")
        elif(logType=="warn"):
            logging.warning(msg)
            if(self.useGui):
                self.guiTextHandler.insert(tkinter.END ,"warn: " + msg + "\n",('warn_tag'))

    def updateProgress(self):
        if(self.useGui):
            if(self.totalProgress<self.progressBarMax):
                self.guiProgressHandler.step(self.progressStep)
                self.totalProgress = self.totalProgress + self.progressStep

    def finalProgressUpdate(self):
        finalStep = self.progressBarMax - self.totalProgress
        if(finalStep>0):
            self.guiProgressHandler.step(finalStep - 1)







