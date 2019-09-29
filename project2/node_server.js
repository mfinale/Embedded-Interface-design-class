// server.js
 
const WebSocket = require('ws')
var mysql = require('mysql'); 
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

//start connection to sensor db
var db_con = mysql.createConnection({
  host: "localhost",
  user: "eiduser",
  password: "Shrek2",
  database: "sensordb"
});

//on connection do this
db_con.connect(function(err) {
  if (err) throw err;
  console.log("Connected!");
  db_con.query("SELECT * FROM sensordata", function (err, result, fields) {
    if (err) throw err;
    console.log(result);
  });
});
