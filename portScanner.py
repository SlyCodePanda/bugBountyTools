#!/bin/python

import socket
import subprocess
import sys
from datetime import datetime

"""
A basic remote-host port scanner script.

ref: https://www.pythonforbeginners.com/code-snippets-source-code/port-scanner-in-python/
"""

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


# Clear the screen
subprocess.call('clear', shell=True)

# Ask for input
remoteServer = raw_input("Enter a remote host to scan: ")
remoteServerIP = socket.gethostbyname(remoteServer)

# Print a banner with information on which hose we are about to scan
print bcolors.OKBLUE + "-" * 60
print "Please wait, scanning remote host ", remoteServerIP
print "-" * 60 + bcolors.ENDC

# Check what time the scan started
t1 = datetime.now()

# Using the range function to specify ports (here is will scan all ports between 1 and 1024)
# We also put in some error handling for catching errors

try:
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))

        if result == 0:
            print "Port {}:         ".format(port) + bcolors.OKGREEN + "Open" + bcolors.ENDC

        sock.close()

except KeyboardInterrupt:
    print "Interrupted...Quitting..."
    sys.exit()

except socket.gaierror:
    print "Hostname could not be resolved. Exiting."
    sys.exit()

except socket.error:
    print "Couldn't connect to server"
    sys.exit()

# Check the time again
t2 = datetime.now()

# Calculate the difference of time to see how long the script took to run.
total = t2 - t1

print "Scanning completed in: " + bcolors.OKGREEN + "{}".format(total) + bcolors.ENDC
