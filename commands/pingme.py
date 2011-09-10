# Copyright 2011 orabot Developers
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

import config
import re
import sqlite3

def usage(self, user, channel):
    self.send_reply( ("Usage: "+config.command_prefix+"pingme when USERNAME back"), user, channel )

def pingme(self, user, channel):
    command = (self.command)
    command = command.split()
    if not re.search("^#", channel):
        message = "Command can be used only on a channel"
        self.send_notice( message, user )
        return
    conn = sqlite3.connect('../db/openra.sqlite')   # connect to database
    cur=conn.cursor()
    if ( len(command) == 4 ):
        if ( command[1].lower() != 'when' ):
            usage(self, user, channel)
            cur.close()
            return
        if ( command[3].lower() != 'join' ):
            usage(self, user, channel)
            cur.close()
            return
        #send NAMES channel to server
        str_buff = ( "NAMES %s \r\n" ) % (channel)
        self.irc_sock.send (str_buff.encode())
        #recover all nicks on channel
        recv = self.irc_sock.recv( 4096 )
        recv=self.decode_stream(recv)
        if str(recv).find ( " 353 "+config.bot_nick ) != -1:
            user_nicks = str(recv).split(':')[2].rstrip()
            user_nicks = user_nicks.replace('+','').replace('@','').replace('%','')
            user_nicks = user_nicks.split(' ')
            
        if command[2] in user_nicks:  #reciever is on the channel right now
            self.send_message_to_channel( ("User is online!"), channel)
            cur.close()
            return
        sql = """SELECT users_back FROM pingme
                WHERE who = '"""+user+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) == 0 ):
            sql = """INSERT INTO pingme
                    (who,users_back)
                    VALUES
                    (
                    '"""+user+"','"+command[2]+"""'
                    )
            """
            cur.execute(sql)
            conn.commit()
            self.send_reply( ("I will do it!"), user, channel )
        else:
            records_list = records[0][0].split(',')
            if ( len(records_list) == 20 ):
                message = "Sorry, You've already requested `"+config.command_prefix+"pingme` of 20 users! I don't support more..."
                self.send_notice( message, user )
                cur.close()
                return
            records_list.append(command[2])
            records_back = ",".join(records_list)
            sql = """UPDATE pingme
                    SET users_back = '"""+records_back+"""'
                    WHERE who = '"""+user+"""'
            """
            cur.execute(sql)
            conn.commit()
            self.send_reply( ("I will do it!"), user, channel )
    elif ( len(command) == 1 ):
        sql = """SELECT users_back FROM pingme
                WHERE who = '"""+user+"""'
        """
        cur.execute(sql)
        records = cur.fetchall()
        conn.commit()
        if ( len(records) == 0 ):
            message = "You've not requested anything yet..."
            self.send_notice( message, user )
        else:
            message = "You will be pinged when next users join: " + records[0][0]
            self.send_notice( message, user )
    else:
        usage(self, user, channel)
    cur.close()
