"""
myTelnetCommand is an extremly simple class which represents a single telnet
    command, its expected result and 'stop on error' condition. It can also be
    considered as a test case.

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

class myTelnetCommand(object):
    def __init__(self,com,exp,soe):
        self.command = com
        self.expected = exp
        self.stopOnError = soe

