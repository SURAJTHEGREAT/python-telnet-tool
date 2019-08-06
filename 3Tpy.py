"""
This is a starting point for 3Tpy application. Code below analyses input
    parameters and starts program in gui or non-gui mode. There is an instance
    of myTelnet class created here. Also gui object is initiated here.

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
import sys
import os
from myTelnet import *
from telnetToolGui import *

nOption = ""
lOption = ""
inputOptions = sys.argv
argvCounter = 0
nFound = False
lFound = False
argvFailFound = False
argvFailMsg = ""
licenseMsg = "\n    3Tpy - Telnet Testing Tool\n    Copyright (C) 2013 Marcin Kowalczyk\n"
licenseMsg = licenseMsg + "    This program comes with ABSOLUTELY NO WARRANTY.\n"
licenseMsg = licenseMsg + "    This is free software, and you are welcome to redistribute it\n"
licenseMsg = licenseMsg + "    under certain conditions (http://opensource.org/licenses/GPL-3.0).\n\n"
print(licenseMsg)
#print("Options are")
#print(inputOptions)
for i in inputOptions:
    if(not argvFailFound):
        #print("argv")
        #print(argvCounter)
        if(argvCounter>0):
            if(nFound):
                nFound = False
                if(re.search("-.+",i)):
                    argvFailFound = True
                    #print("Printing failure here")
                    argvFailMsg = "Command line params failure: -n must be followed by a file name or path"
                elif(re.search("\w+",i)):
                    nOption = i
                else:
                    argvFailFound = True
                    argvFailMsg = "Command line params failure: -n must be followed by a file name or path"
            elif(lFound):
                lFound = False
                if(nOption!=""):
                    if(re.search("-.+",i)):
                        argvFailFound = True
                        argvFailMsg = "Command line params failure: -l must be followed by a file name or path"
                    elif(re.search("\w+",i)):
                        lOption = i
                    else:
                        argvFailFound = True
                        argvFailMsg = "Command line params failure: -l must be followed by a file name or path"
                else:
                    argvFailFound = True
                    argvFailMsg = "Command line params failure: -l must not occur without -n"
            elif(re.search("-.+",i)):
                if(re.search("-n",i)):
                    nFound = True
                    #print("into n found loop")
                elif(re.search("-l",i)):
                    lFound = True
                    #print("into l found loop")
                else:
                    argvFailFound = True
                    argvFailMsg = "Command line params failure: unknown parameter"
        argvCounter = argvCounter + 1
if(not argvFailFound):
    if(nOption==""):
        mt = myTelnet()
        guiRoot = Tk()
        guiObject = telnetToolGui(guiRoot,mt)
        print("3Tpy started in GUI mode.")
        guiRoot.mainloop()
    else:
        mt = myTelnet()
        mt.getXml(nOption)
        if(lOption!=""):
            mt.initiateLogName(customLog=lOption)
            print("3Tpy started. Test file to be executed: " + nOption + ", custom log name: " + lOption)
        else:
            print("3Tpy started. Test file to be executed: " + nOption)
        mt.executeTestScenario()
else:
    print(argvFailMsg)



