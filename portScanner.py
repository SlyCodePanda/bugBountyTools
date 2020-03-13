#!/bin/python

import socket
import subprocess
import sys
from datetime import datetime

# Class for changing terminal font colours
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def checkPortResult(p, r, portDesc=None):
    """
    Checks the ports and their results, prints to terminal based on result.
    :param p: Port number.
    :param r: result of scan (0 = open, 111 = closed)
    :param portDesc: if this is passed, then it is a common port with a
                     description of it's default  assignment.
    :return: N/A
    """

    if r == 0 and not portDesc:
        print "Port {}:         ".format(p) + bcolors.OKGREEN + bcolors.BOLD + "Open" + bcolors.ENDC

    elif portDesc:
        if r == 0:
            print "Port " + bcolors.BOLD + str(p) + bcolors.ENDC + " - {}:          ".format(portDesc) + bcolors.OKGREEN + bcolors.BOLD + "Open" + bcolors.ENDC
        elif r == 111:
            print "Port " + bcolors.BOLD + str(p) + bcolors.ENDC + " - {}:          ".format(portDesc) + bcolors.FAIL + "Closed" + bcolors.ENDC

        return None


# Dictionary of common ports.
portsDict = {20: 'FTP Data Transfer',
             21: 'FTP Command Control',
             22: 'SSH',
             23: 'Telnet remote login',
             25: 'SMTP E-mail routing',
             53: 'DNS service',
             67: 'DHCP',
             68: 'DHCP',
             80: 'HTTP',
             110: 'POP3',
             119: 'NNTP',
             123: 'NTP',
             143: 'IMAP',
             161: 'SNMP',
             194: 'IRC',
             443: 'HTTPS'}

# Clear the screen
subprocess.call('clear', shell=True)

# Ask for input
remoteServer = raw_input("Enter a remote host to scan: ")

# If 'https://<url>/' was pasted in, strip it down to '<url>'.
if 'https://' in remoteServer:
    remoteServer = remoteServer.split('https://')[1].split('/')[0]

remoteServerIP = socket.gethostbyname(remoteServer)

# Print a banner with information on which hose we are about to scan
print bcolors.OKBLUE + "-" * 75
print "Please wait, scanning remote host        {} - {}".format(remoteServer, remoteServerIP)
print "-" * 75 + bcolors.ENDC

# Check what time the scan started
t1 = datetime.now()

# Using the range function to specify ports (here is will scan all ports between 1 and 1024)
# We also put in some error handling for catching errors

try:
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))

        # Check if port is in common port dictionary.
        if port in portsDict.keys():
            checkPortResult(port, result, portsDict[port])
        else:
            checkPortResult(port, result)

        sock.close()

except KeyboardInterrupt:
    print bcolors.FAIL + "Interrupted...Quitting..." + bcolors.ENDC
    sys.exit()

except socket.gaierror:
    print bcolors.FAIL + "Hostname could not be resolved. Exiting." + bcolors.ENDC
    sys.exit()

except socket.error:
    print bcolors.FAIL + "Couldn't connect to server" + bcolors.ENDC
    sys.exit()

# Check the time again
t2 = datetime.now()

# Calculate the difference of time to see how long the script took to run.
total = t2 - t1

print "Scanning completed in: " + bcolors.OKGREEN + "{}".format(total) + bcolors.ENDC
