
/*
node_server.js: This file runs a node.js server on local host port 8080. The server establishes a websocket with 
the client as well as a mySQL database connection with the database that is populated with sensor data from DHT22_application.py

The server accepts 2 commands from the client: "Read one from db" which retrieves and sends the latest entry from the database, and
"fetch 10 samples" which retrieves and sends the last 10 samples from the database.

This file must be ran before opening the client. Please use launch.py to start this file.
*/ 
const WebSocket = require('ws')
var mysql = require('mysql'); 

/*
__author__ = "Michael Finale"
__copyright__ = "Copyright (C) 2019 by Michael Finale"
#
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. Users are
# permitted to modify this and use it to learn about the field of embedded
# software. Michael Finale and the University of Colorado
# are not liable for any misuse of this material.
#
*/

//open webssocket on local host port 8080 
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
  

  
  ws.on('message', message => {
    console.log("Message from Client: "+ message);
    
    //Respond to "Read one from db" command from client.
    if (message=="Read one from db") {
      rows=1
      console.log("Reading last " +rows + " entries from sensor db.");
      //request all readings from the db.
      db_cmd="SELECT * FROM (SELECT * FROM sensordata ORDER BY timestamp DESC LIMIT " + rows + ") sub ORDER by timestamp ASC"
      db_con.query(db_cmd, function (err, result, fields) {
      if (err) throw err;
      //Only attempt to parse the information from the most recent sb reading if there is at least on entry in the db.
      //Otherwise an error is throne.
      if (result.length > 0){
        var time = result[0].timestamp;
        var temp= result[0].temp;
        var humid = result[0].humid;
        reading = "Timestamp: " + time + "      / Temperature : " + temp+"*C " + " / Humidity : "+ humid+"%"
        console.log(reading);
        ws.send('noderead'+reading);
        }
       // Send this message if there is no data in the db.
       else {ws.send('noderead'+"Timestamp: no data in db      / Temperature : no data in db   / Humidity : no data in db  %");}
      });
    } 
   //Respond to "fetch 10 samples" command from client.
    else if (message=="fetch 10 samples") {
      rows=10
      //retrieve the last "rows" from the mySQL db.
       console.log("Reading last " +rows + " entries from sensor db.");
      db_cmd="SELECT * FROM (SELECT * FROM sensordata ORDER BY timestamp DESC LIMIT " + rows + ") sub ORDER by timestamp ASC"
      db_con.query(db_cmd, function (err, result, fields) {
      if (err) throw err;
      multi_reading = ""
      //increment only up to the current size of the sql sb. Otherwise an error is thrown if trying
      // to get the property of an empty db entry.
      for (var i = 0; i <result.length; i++) {
      var time = result[i].timestamp;
      var temp= result[i].temp;
      var humid = result[i].humid;
     multi_reading = multi_reading + "(Timestamp: " + time + "      / Temperature : " + temp+"*C " + " / Humidity : "+ humid+"%)"
     }
      //send information back
      ws.send('nodefetch'+multi_reading);
      });
    } 

    
    else {
      console.log("Invalid command from client:");
      ws.send('Invalid command sent to node_js server');
      }
  
  })
  
  console.log("Connected to Client");
  
})






