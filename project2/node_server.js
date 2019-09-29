// server.js
 
const WebSocket = require('ws')

//open webscoket on local host port 8080 
const wss = new WebSocket.Server({ port: 8080 })
 
//once connection is made print received message and
//send a message back
wss.on('connection', ws => {
  ws.on('message', message => {
    console.log(`Received message => ${message}`)
  })
  ws.send('Hello! Message From Server!!')
})