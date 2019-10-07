# EID Project2: Tornado and Node.JS servers for a HTML client

## Author: Michael Finale
## Installation Instructions
- Perform installation from project 1
- Install nvm, node, and npm by performing the following in a terminal:
	- `curl -o-https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash`
	- Restart your terminal
	- `nvm –version`Should return a version number like 0.34.0
	- `nvm install node` 
	- `nvm install 10.16.3`
- Install web socket for node.js by entering `npm install ws`
- Install tornado for python by entering `pip3 install tornado`
- clone repo from https://github.com/mfinale/Embedded-Interface-design-class.git
- To start the program, launch the node.js and tornado servers by running `python3 launch.py` 
- Once the servers are running, use a browser to open `client.html`

 
## Project Work
Application developed by Michael Finale.  



## Project Additions/Known Bugs
 - Retrieval of humid or temperature plots has not been implemented as of 10/6/2019 
 - Temperature conversion has been implemented for single node.js and python/tornado readings but not as part of the network responsiveness test
## References
- [1] https://www.js-tutorials.com/nodejs-tutorial/simple-websocket-example-with-nodejs/
- [2] https://groups.google.com/forum/#!msg/python-tornado/Q3VUpFGvuVY/4rC8VtPaBwAJ
- [3] https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API/Writing_WebSocket_client_applications
- [4] https://stackoverflow.com/questions/25905752/close-the-program-using-keyboard-interrupt-in-python
- [5] https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-truettps://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
- [6] https://www.w3schools.com/nodejs/nodejs_mysql.asp 
- [7] https://www.pubnub.com/blog/nodejs-websocket-programmingexamples/
- [8] https://os.mbed.com/cookbook/Websockets-Server  
