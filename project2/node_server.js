// server.js
 
const WebSocket = require('ws')
var mysql = require('mysql'); 

//open webscoket on local host port 8080 
const wss = new WebSocket.Server({ port: 8080 })
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
  console.log("Connected to Sensor Database");

});




//once websocket connection is made. Wait for messages.
wss.on('connection', ws => {
  
  ws.send('Connected to node_js server!');
  
  ws.on('message', message => {
    console.log("Message from Client: "+ message);
    
    //read one entry from my sql db
    if (message=="Read one from db") {
      rows=1
       console.log("Reading last " +rows + " entries from sensor db.");
      db_cmd="SELECT * FROM (SELECT * FROM sensordata ORDER BY timestamp DESC LIMIT " + rows + ") sub ORDER by timestamp ASC"
      db_con.query(db_cmd, function (err, result, fields) {
      if (err) throw err;
      var time = result[0].timestamp;
      var temp= result[0].temp;
      var humid = result[0].humid;
      reading = time + "       Temperature : " + temp+"*C " + "  Humidity : "+ humid+"%"
      console.log(reading);
      ws.send(reading);
      });
    } 
    
    else if (message=="bye") {} 
    
    else {
      console.log("Invalid command from client:");
      ws.send('Invalid command sent to node_js server');
      }
  
  })
  
  console.log("Connected to Client");
  
})






