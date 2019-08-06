"""
telnetFiles class is responsible for loading and saving test input files in xml
    format. Used library: xml.dom.minidom.

Instance of telnetFiles class is initiated inside myTelnet class.

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
import xml.dom.minidom
from xml.dom.minidom import getDOMImplementation
import re

class telnetFiles(object):
    def __init__(self):
        self.confDict = {}
        self.commandDicts = []

    def setConfDict(self, confDict):
        self.confDict = confDict

    def setCommandDicts(self, commandDicts):
        self.commandDicts = commandDicts

    def saveXml(self,filePath):
        newXmlImpl = getDOMImplementation()
        newXml = newXmlImpl.createDocument(None, "testscenario", None)
        xmlRootElement = newXml.documentElement
        configNode = newXml.createElement("config")
        xmlRootElement.appendChild(configNode)
        configArray = [['ipaddress','host'],['telnetPort','port'],['username','name'],['password','password'],['loginprompt','login prompt'],['passprompt','password prompt'],['regularprompt','default prompt']]
        for i in configArray:
            subConfigNode = newXml.createElement(i[0])
            subConfigText = newXml.createTextNode(self.confDict[i[1]])
            subConfigNode.appendChild(subConfigText)
            configNode.appendChild(subConfigNode)
        commandsNode = newXml.createElement("commands")
        for i in self.commandDicts:
            subCommandNode = newXml.createElement("command")
            commandsNode.appendChild(subCommandNode)
            sendSubCommandNode = newXml.createElement("send")
            sendSubCommandText = newXml.createTextNode(i['command'])
            sendSubCommandNode.appendChild(sendSubCommandText)
            subCommandNode.appendChild(sendSubCommandNode)
            expSubCommandNode = newXml.createElement("exp")
            expSubCommandText = newXml.createTextNode(i['expected'])
            expSubCommandNode.appendChild(expSubCommandText)
            subCommandNode.appendChild(expSubCommandNode)
            soeSubCommandNode = newXml.createElement("soe")
            soeSubCommandText = newXml.createTextNode(str(i['soe']))
            soeSubCommandNode.appendChild(soeSubCommandText)
            subCommandNode.appendChild(soeSubCommandNode)
        xmlRootElement.appendChild(commandsNode)
        retVal = ""
        try:
            f = open(filePath, 'w')
            f.write(newXml.toxml())
            f.close()
        except IOError as ioe:
            retVal = ioe.strerror
        except TypeError:
            retVal =""
        return retVal

    def getXml(self,filePath):
        self.fileFound = True
        try:
            domTestScenario = xml.dom.minidom.parse(filePath)
        except IOError:
            self.fileFound = False
        if(self.fileFound):
            configNodesList = []
            nodeTestScenario = domTestScenario.getElementsByTagName("testscenario")[0]
            lvl2NodesList = nodeTestScenario.childNodes
            for i in lvl2NodesList:
                nodeString = i.toxml()
                if(re.search("config",nodeString)):
                    configNodesList = i.childNodes
                    configSearch = ["ipaddress","telnetPort","username","password","loginprompt","passprompt","regularprompt"]
                    self.confDict = self.searchNodes(configNodesList,configSearch)
                elif(re.search("commands",nodeString)):
                    commandsNodesList = i.childNodes
                    for k in commandsNodesList:
                        singleCommandNodes = k.childNodes
                        commandSearch = ["send","exp","soe"]
                        commandDict = self.searchNodes(singleCommandNodes,commandSearch)
                        if(commandDict != {}):
                            self.commandDicts.append(commandDict)
        return self.fileFound

    def searchNodes(self,nodeList,searchList):
        nodesValues = {}
        for i in nodeList:
            nodeString = i.toxml()
            for j in searchList:
                if(re.search(j,nodeString)):
                    nodeString = nodeString.replace("<" + j + ">","")
                    nodeString = nodeString.replace("</" + j + ">","")
                    nodeString = nodeString.replace("<" + j + "/>","")
                    nodesValues[j] = nodeString
                    break
        return nodesValues

