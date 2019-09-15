# installation steps for readme
# clone from git
# install mySQL drive for python sudo pip3 install mysql-connector
# install mySQL and create a local database with user and password info https://pimylifeup.com/raspberry-pi-mysql/
# install DHT library for Raspberry Pi sudo pip3 install Adafruit_DHT
import mysql.connector

#create a database connection
mydb = mysql.connector.connect(host="localhost",user="eiduser",passwd="Shrek2",
                               database='sensordb')

mycursor = mydb.cursor()

#start with clean table called "sensordata"
mycursor.execute("DROP TABLE sensordata")
mycursor.execute("CREATE TABLE sensordata (temp float(4,2), humid float(4,2))")




mycursor.execute("SHOW TABLES")

for x in mycursor:
  print(x)
  

sql = "INSERT INTO sensordata (temp, humid) VALUES (%s, %s)"
val = (12.00, 17.55)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")

mycursor.execute("SELECT * FROM sensordata")

myresult = mycursor.fetchall()

for x in myresult:
  print(x)



