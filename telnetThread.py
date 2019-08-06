"""
telnetThread class is inherited from threading.Thread. Its 'run' method
    performs test scenario in a separate thread so that GUI doesn't suspend.

Instance of telnetThread is initiated inside telnetToolGui class.

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
import threading

class telnetThread(threading.Thread):
    def run(self):
        if(not self.myThrTelnet.interrupted):
            self.myThrTelnet.startSession()
            self.myThrTelnet.log_in()
            self.myThrTelnet.runCommandsFromList()
            self.myThrTelnet.calculateFinalResult()
            self.myThrTelnet.endSession()
            self.myThrTelnet.releaseLoggingHandlers()
            self.myThrTelnet.finalProgressUpdate()
        self.myThrTelnet.convertLogIntoHtml()
        self.myThrTelnet.deactivateGui()

    def setMyTelnetHandler(self, myTel):
        self.myThrTelnet = myTel

