import os
import sys
import subprocess
import time
import signal
#This script launches the node.js server and p
#python DHT22_application (which includes the sensor gui and t
#tornado websocket server.
#
#The script will terminate both processes upon enterin CTRL+C into the
#terminal.




# The os.setsid() is passed in the argument preexec_fn so
# it's run after the fork() and before  exec() to run the shell.
cmd1= "python3 DHT22_application.py"
pro1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
print("Starting DHT22 Sensor Gui and tornado server.")   
#allow the python application to start up and populate mySQL db.
#if user attempts to read empyt mysql db via node.js, the node.js server
#closes.
time.sleep(20)
                    
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

