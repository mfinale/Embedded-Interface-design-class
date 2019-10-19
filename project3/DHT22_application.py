#!/usr/bin/env python
"""project1gui.py:
DHT22 Temperature and Humidity interface for project 1 of Embedded Interface Design Course.
This python application that runs a PyQt5 which interfaces with a DHT22 sensor with
the following functions:
- a button to read the current temperature (in Celsius) and humidity with corresponding timestamp
- periodic readings from the DHT22 sensor every 15 seconds for up to 30 readings
- alarm system that is configured by setting the upper limits for the temperature
and humidity
- plotting of the last 10 temperature readings
- plotting of the last 10 humidity readings

Application was developed to be used on a Raspberry Pi 3 running Raspian Buster OS.
Please view readme for installation details.
"""

import mysql.connector
import Adafruit_DHT
import datetime
import time
import matplotlib.pyplot as plt
import json
from PyQt5 import QtCore, QtGui, QtWidgets
import paho.mqtt.client as mqtt
import ssl
__author__ = "Michael Finale"
__copyright__ = "Copyright (C) 2019 by Michael Finale"
#
# Redistribution, modification or use of this software in source or binary
# forms is permitted as long as the files maintain this copyright. Users are
# permitted to modify this and use it to learn about the field of embedded
# software. Michael Finale and the University of Colorado
# are not liable for any misuse of this material.
#


#DHT sensor intialization
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

#create a database connection
mydb = mysql.connector.connect(host="localhost",user="eiduser",passwd="Shrek2",
                               database='sensordb')
mycursor = mydb.cursor()

#start with clean table called "sensordata"
mycursor.execute("DROP TABLE sensordata")
mycursor.execute("CREATE TABLE sensordata ( timestamp VARCHAR(30),temp float(10,2), humid float(10,2))")

#function for logging MQTT connection data
def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("MQTT client connected OK Returned code=",rc)
    else:
        print("MQTT clientBad connection Returned code=",rc)


#define credentials for MQTT connection to aws
IoT_protocol_name = "x-amzn-mqtt-ca"
aws_iot_endpoint = "a1i8vja12d7doa-ats.iot.us-east-1.amazonaws.com"
url = "https://{}".format(aws_iot_endpoint)
ca = "/home/pi/Desktop/aws_files/root-ca.pem"
cert = "/home/pi/Desktop/aws_files/1d28cc129f-certificate.pem.crt"
private = "/home/pi/Desktop/aws_files/1d28cc129f-private.pem.key"

# setup ssl for connection
# code borrowed from:
#https://aws.amazon.com/blogs/iot/how-to-implement-mqtt-with-tls-client-authentication-on-port-443-from-client-devices-python/
def ssl_alpn():
    try:
        ssl_context = ssl.create_default_context()
        ssl_context.set_alpn_protocols([IoT_protocol_name])
        ssl_context.load_verify_locations(cafile=ca)
        ssl_context.load_cert_chain(certfile=cert, keyfile=private)
        return  ssl_context
    except Exception as e:
        print("exception ssl_alpn()")
        raise e

#start MQTT connection with ssl credentials
client =mqtt.Client("DHT22_MQTT_Client")
ssl_context= ssl_alpn()
client.tls_set_context(context=ssl_context)
client.on_connect=on_connect
client.connect(aws_iot_endpoint, port=443)
time.sleep(4)
client.loop_start()
client.loop_stop()


#function to publish a MQTT message
def send_MQTT_data(message,client_id):
    client_id.loop_start()
    client_id.publish("sensor",message,qos=1)
    client_id.loop_stop()


#UI class generated by PyQt5 Designer. Additional functions added by Michael Finale.
class Ui_Dialog(object):

    #variables passed between functions within class:
    read_count = 0  #counter for periodic sensor readings
    max_humid = 300 #default humidity limit for alarm
    max_temp = 300  #default temperature limit for alarm

    def setupUi(self, Dialog):
        Dialog.setObjectName("DHT22 Sensor Interface")
        Dialog.resize(941, 490)
        self.read_data_out = QtWidgets.QLabel(Dialog)
        self.read_data_out.setGeometry(QtCore.QRect(60, 370, 811, 41))
        self.read_data_out.setObjectName("read_data_out")
        self.status_out = QtWidgets.QLabel(Dialog)
        self.status_out.setGeometry(QtCore.QRect(60, 430, 811, 31))
        self.status_out.setObjectName("status_out")
        self.temp_limit_in = QtWidgets.QLineEdit(Dialog)
        self.temp_limit_in.setGeometry(QtCore.QRect(580, 80, 91, 38))
        self.temp_limit_in.setObjectName("temp_limit_in")
        self.hum_limit_in = QtWidgets.QLineEdit(Dialog)
        self.hum_limit_in.setGeometry(QtCore.QRect(580, 140, 91, 38))
        self.hum_limit_in.setObjectName("hum_limit_in")
        self.read_data_btn = QtWidgets.QPushButton(Dialog)
        self.read_data_btn.setGeometry(QtCore.QRect(50, 290, 331, 61))
        self.read_data_btn.setObjectName("read_data_btn")
        self.plot_temp_btn = QtWidgets.QPushButton(Dialog)
        self.plot_temp_btn.setGeometry(QtCore.QRect(50, 120, 211, 31))
        self.plot_temp_btn.setObjectName("plot_temp_btn")
        self.plot_hum_btn = QtWidgets.QPushButton(Dialog)
        self.plot_hum_btn.setGeometry(QtCore.QRect(50, 190, 211, 31))
        self.plot_hum_btn.setObjectName("plot_hum_btn")
        self.alarm_message = QtWidgets.QLabel(Dialog)
        self.alarm_message.setGeometry(QtCore.QRect(720, 90, 190, 90))
        self.alarm_message.setObjectName("alarm_message")
        self.alarm_message.setWordWrap(True)
        font = QtGui.QFont("Arial", 15, QtGui.QFont.Bold)
        self.alarm_message.setFont(font)
        self.setlimits_btn = QtWidgets.QPushButton(Dialog)
        self.setlimits_btn.setGeometry(QtCore.QRect(510, 210, 125, 36))
        self.setlimits_btn.setObjectName("setlimits_btn")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(350, 90, 231, 21))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(380, 150, 191, 21))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(680, 60, 31, 81))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(680, 120, 31, 81))
        self.label_7.setObjectName("label_7")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        #setup timer for periodic readings to update status line and store data every 15 seconds
        self.read_timer = QtCore.QTimer()
        self.read_timer.setSingleShot(False)
        self.read_timer.timeout.connect(self.store_sensor_data)
        self.read_timer.start(15000)

        #read sensor data on button press
        self.read_data_btn.clicked.connect(self.get_instant_sensor_data)

        #set max limits of temper and humidty on button press
        self.setlimits_btn.clicked.connect(self.set_limits)

        #plot temperature on button press
        self.plot_temp_btn.clicked.connect(self.plot_temp)

        #plot humidity on button press
        self.plot_hum_btn.clicked.connect(self.plot_humid)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "DHT22 Sensor Interface"))
        self.read_data_out.setText(_translate("Dialog", "Sensor data"))
        self.status_out.setText(_translate("Dialog", "Sensor Status"))
        self.read_data_btn.setText(_translate("Dialog", "Read Temperature and Humidity"))
        self.plot_temp_btn.setText(_translate("Dialog", "Plot Temperature"))
        self.plot_hum_btn.setText(_translate("Dialog", "Plot Humidity"))
        self.alarm_message.setText(_translate("Dialog", "Alarm Message"))
        self.setlimits_btn.setText(_translate("Dialog", "Set Limits"))
        self.label_4.setText(_translate("Dialog", "Max Temperature Limit:"))
        self.label_5.setText(_translate("Dialog", "Max Humidty Limit:"))
        self.label_6.setText(_translate("Dialog", "*C"))
        self.label_7.setText(_translate("Dialog", "%"))



    #get timestamp, temperature in celsius, and humidity for readings on demand and then print to label
    # project 3 addition: also packages the data into JSON and sends to a MQTT Broker
    def get_instant_sensor_data(self):
        try:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                self.alarm(temperature, humidity)
                temperature = "{0:0.2f}".format(temperature)
                humidity = "{0:0.2f}".format(humidity)
                time = str(datetime.datetime.now())
                self.read_data_out.setText(time + "       Temperature : " + temperature+"*C " + "  Humidity : "+ humidity+"%")
                data= {"Label":"sensor_read", "Timestamp":time,"Temperature":temperature, "Humidity": humidity}
                JSON_data = json.dumps(data)
                send_MQTT_data(JSON_data,client)
            else:
                self.read_data_out.setText("Failed to retrieve sensor data. Check DHT22 sensor connection.")
        except:
            self.read_data_out.setText("Sensor Error")



    # called by timer periodically every 15 seconds. Acquires sensor data and stores in a mysql db for 30 reads then does nothing
    def store_sensor_data(self):
        if self.read_count == 30:
            return
        else:
            val = self.get_sensor_data()
            sql = "INSERT INTO sensordata (timestamp, temp, humid) VALUES (%s, %s, %s)"
            mycursor.execute(sql, val)
            mydb.commit()
        self.read_count = self.read_count +1
        print("sensor reading #"+str(self.read_count))

    #called by store_sensor_data every 15 seconds. Return sensor data and status, and print to label.
    # project 3 addition: also packages the data into JSON and sends to a MQTT Broker
    def get_sensor_data(self):
        try:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                self.alarm(temperature, humidity)
                temperature = "{0:0.2f}".format(temperature)
                humidity = "{0:0.2f}".format(humidity)
                time = str(datetime.datetime.now())
                self.status_out.setText(time + "       Temperature : " + temperature+"*C " + "  Humidity : "+ humidity+"%")
                data= {"Label":"sensor_read", "Timestamp":time,"Temperature":temperature, "Humidity": humidity}
                JSON_data = json.dumps(data)
                send_MQTT_data(JSON_data,client)
                return (time, temperature, humidity)
            else:
                self.status_out.setText("Failed to retrieve sensor data. Check DHT22 sensor connection.")
                time = str(datetime.datetime.now())
                return (time, "0.0", "0.0")
        except:
            self.status_out.setText("Sensor Error")
            time = str(datetime.datetime.now())
            return (time, "0.0", "0.0")

    def set_limits(self):
        try:
            self.max_humid = float(self.hum_limit_in.text())
            self.max_temp = float(self.temp_limit_in.text())
            print ("max humidity and temp are:" + str(self.max_humid) + " " + str(self.max_temp))
        except:
            return

    # check temperature and humidity readings
    # project 3 addition: write an alarm message if readings exceed limits, form a JSON alert message and send to a MQTT broker
    def alarm(self, chk_temp, chk_humid):
        times = str(datetime.datetime.now())
        data= {"Label":"Alert", "Timestamp":times,"Temperature Alert Level":chk_temp, "Temperature Trigger Level": self.max_temp, "Humidity Alert Level": chk_humid, "Humidity Trigger Level":self.max_humid}
        JSON_data = json.dumps(data)
        if chk_humid > self.max_humid and chk_temp > self.max_temp :
            self.alarm_message.setText("<font color='red'>Warning: High Temp and Humidty</font>")
            send_MQTT_data(JSON_data,client)
        elif chk_temp > self.max_temp:
            self.alarm_message.setText("<font color='red'>Warning: High Temp</font>")
            send_MQTT_data(JSON_data,client)
        elif chk_humid > self.max_humid :
            self.alarm_message.setText("<font color='red'>Warning: High Humidity</font>")
            send_MQTT_data(JSON_data,client)
        elif chk_humid < self.max_humid and chk_temp < self.max_temp :
            self.alarm_message.setText("<font color='green'>Temp and Humidty OK</font>")


    #get last desired number of readings of humid data
    #from sql db. Number of readings specified by "rows"
    def retrieve_humid_data(self, rows):
        mycursor.execute("SELECT * FROM \
        ( SELECT timestamp, humid FROM sensordata ORDER BY timestamp DESC LIMIT "+str(rows)+ " )\
        sub ORDER by timestamp ASC")
        return mycursor.fetchall()

    #get last desired number readings of temp data
    #from sql db. Number of readings specified by "rows"
    def retrieve_temp_data(self, rows):
        mycursor.execute("SELECT * FROM \
        ( SELECT timestamp, temp FROM sensordata ORDER BY timestamp DESC LIMIT "+str(rows)+ " )\
        sub ORDER by timestamp ASC")
        return mycursor.fetchall()

    #plot last ten temperature readings from sql db
    def plot_temp(self):
        data = self.retrieve_temp_data(10)
        time_x = []
        temp_y =[]
        for i in range(0,len(data)):
            time_x.append(data[i][0])
            temp_y.append(data[i][1])
        try:
            plt.plot(time_x,temp_y)
        except:
            return
            #nodata has been collected
        plt.xlabel('Time', fontsize=18)
        plt.ylabel('Temperature (°C)', fontsize=14)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()

    #plot last ten humidity readings from sql db
    def plot_humid(self):
        data = self.retrieve_humid_data(10)
        time_x = []
        temp_y =[]
        for i in range(0,len(data)):
            time_x.append(data[i][0])
            temp_y.append(data[i][1])
        try:
            plt.plot(time_x,temp_y)
        except:
            return
            #nodata has been collected
        plt.xlabel('Time', fontsize=18)
        plt.ylabel('Humidty (%)', fontsize=14)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.show()





if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
    client.disconnect() #disconnect from MQTT broker