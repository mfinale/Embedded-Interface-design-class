  
#!/usr/bin/env python
"""launch.py: This script launches the node.js server and 
python DHT22_application, which includes the sensor QT gui and tornado websocket server.
This script must be ran from the command line before opening the client.html file.
The script will terminate both processes upon entering CTRL+C into the
terminal.
"""


import os
import sys
import subprocess
import time
import signal

__author__ = "Michael Finale"
__copyright__ = "Copyright (C) 2019 by Bruce Montgomery"
#
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. Users are
# permitted to modify this and use it to learn about the field of embedded
# software. Michael Finale and the University of Colorado
# are not liable for any misuse of this material.
#




# The os.setsid() is passed in the argument preexec_fn so
# it's run after the fork() and before  exec() to run the shell.
cmd1= "python3 DHT22_application.py"
pro1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
print("Starting DHT22 Sensor Gui and tornado server.")   

                    
cmd2= "node node_server.js"
pro2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid)
print("Starting node.js server.")   
print("Both servers are ready.")   
print("Enter CTRL+C to kill the program.")
while True:
	try:
		time.sleep(1)
	except KeyboardInterrupt:
		os.killpg(os.getpgid(pro1.pid), signal.SIGTERM)
		os.killpg(os.getpgid(pro2.pid), signal.SIGTERM)
		print(" ")
		print("Closing program")
		break

