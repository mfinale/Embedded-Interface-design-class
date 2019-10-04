import os
import sys
import subprocess
import time
import signal


# The os.setsid() is passed in the argument preexec_fn so
# it's run after the fork() and before  exec() to run the shell.
cmd1= "python3 DHT22_application.py"
pro1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 
cmd2= "node node_server.js"
pro2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, 
                       shell=True, preexec_fn=os.setsid) 

while True:
	try:
		time.sleep(1)
		print(".")
	except KeyboardInterrupt:
		os.killpg(os.getpgid(pro1.pid), signal.SIGTERM)
		os.killpg(os.getpgid(pro2.pid), signal.SIGTERM)
		print(" ")
		print("Closing program")
		break

