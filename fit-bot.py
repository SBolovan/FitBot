#Kyle Engelken
#Fit Bot
#Displays fits in an irc channel for Eve Online

import sys
import socket
import string

host=raw_input('What server -> ')
port=raw_input('What port -> ')
nick="FitBot"
ident="fitbot"
realname="PFB"
readbuffer=""
chan = raw_input('What channel -> ')

print 'Starting...'


fits = open('fits.txt', 'r')
fit_list = []

for line in fits:
    fit_list.append(line)

irc=socket.socket()
irc.connect((host, port))
irc.send("nick %s\r\n" % nick)
irc.send("USER %s %s bla :%s\r\n" % (ident, host, realname))

print 'Connected.'

logged = False
while 1:
    #Read stuff from server
    readbuffer=readbuffer+irc.recv(1024)
    temp=string.split(readbuffer, "\n")
    readbuffer=temp.pop()

    #Make stuff readable
    for line in temp:
        line=string.rstrip(line)
        line=string.split(line)

        #If you aren't in the channel yet, join the channel
        if line[1] == 'MODE' and not logged:
            irc.send("JOIN %s\r\n" % chan)
            irc.send('PRIVMSG ' + chan + ' :Hello.\r\n')
            logged = True

        #Response that's part of the protocol, don't delete
        if line[0]=="PING":
            irc.send("PONG %s\r\n" % line[1])

        #If you are logged in, look for commands
        if logged and len(line) > 3:
            command = line[3:] #Get rid of protocol parts and get actual content

            #Command to display fits
            if command[0] == ':!fit':
                lines = []
                adding = False

                #Get args from command
                if len(command) > 1:
                    ship_name = command[1]
                    if len(command) > 2:
                        for word in command[2:]:
                            ship_name = ship_name + ' ' + word

                    #Find fit of specified ship in the fits.txt file
                    for line in fit_list:
                        if line[1:line.find(',')] == ship_name:
                            adding = True
                        elif line[0] == '[' and line[0:6] != '[Empty':
                            adding = False
                        if adding:
                            lines.append(line)

                #Respond to command with no args
                if len(lines) == 0:
                    irc.send('PRIVMSG ' + chan + ' :Please include a ship name (!fit Wolf for example) \r\n')
                #Send the asked for ship fit
                else:
                    for line in lines:
                        if line == '\n':
                            irc.send('PRIVMSG ' + chan + ' : \r\n')
                        else:
                            irc.send('PRIVMSG ' + chan + ' :%s\r\n' % line)