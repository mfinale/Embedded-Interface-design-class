# installation steps for readme
# clone from git
# install mySQL drive for python sudo pip3 install mysql-connector
# install mySQL and create a local database with user and password info https://pimylifeup.com/raspberry-pi-mysql/
# install DHT library for Raspberry Pi sudo pip3 install Adafruit_DHT
import mysql.connector
import Adafruit_DHT
import datetime

#DHT sensor intialization
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

#create a database connection
mydb = mysql.connector.connect(host="localhost",user="eiduser",passwd="Shrek2",
                               database='sensordb')
mycursor = mydb.cursor()

#start with clean table called "sensordata"
mycursor.execute("DROP TABLE sensordata")
mycursor.execute("CREATE TABLE sensordata ( timestamp VARCHAR(30),temp float(4,2), humid float(4,2))")


#get timestamp, temperature in celsius, and humidity
def get_sensor_data():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        temperature = "{0:0.2f}".format(temperature)
        humidity = "{0:0.2f}".format(humidity)
        time = str(datetime.datetime.now())
        print(time + " Temperature = " + temperature+"*C " + "Humidity= "+ humidity+"%")
        return (time, temperature, humidity)
    else:
        print("Failed to retrieve data from DHT22 sensor")


def store_sensor_data():
    sql = "INSERT INTO sensordata (timestamp, temp, humid) VALUES (%s, %s, %s)"
    val = get_sensor_data()
    mycursor.execute(sql, val)
    mydb.commit()


#get last desired readings of humid data
def retrieve_humid_data(rows):
    mycursor.execute("SELECT * FROM \
    ( SELECT timestamp, humid FROM sensordata ORDER BY timestamp DESC LIMIT "+str(rows)+ " )\
    sub ORDER by timestamp ASC")
    return mycursor.fetchall()

#get last desired readings of temp data
def retrieve_temp_data(rows):
    mycursor.execute("SELECT * FROM \
    ( SELECT timestamp, temp FROM sensordata ORDER BY timestamp DESC LIMIT "+str(rows)+ " )\
    sub ORDER by timestamp ASC")
    return mycursor.fetchall()


#main for debugging

for x in range (0,10):
    store_sensor_data()
    
print ("            ")
myresult = retrieve_humid_data(4)    
for x in myresult:
    print(x)
    
myresult = retrieve_temp_data(4)    
for x in myresult:
    print(x)








