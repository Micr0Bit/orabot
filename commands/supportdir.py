# Copyright 2011-2016 orabot Developers
#
# This file is part of orabot, which is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Show OpenRA primary Support directory location
"""

import time

def supportdir(self, user, channel):
    command = (self.command).split()
    if ( len(command) == 1 ):
        self.send_reply( "Windows: Username\\My Documents\\OpenRA\\", user, channel )
        time.sleep(1)
        self.send_reply( "OS X: /Users/username/Library/Application Support/OpenRA/ ", user, channel )
        time.sleep(1)
        self.send_reply( "GNU/Linux: /home/username/.openra/", user, channel )
        return True