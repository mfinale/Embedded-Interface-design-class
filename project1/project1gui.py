# clone from git
# install mySQL drive for python3 sudo pip3 install mysql-connector
# install mySQL and create a local database with user and password info https://pimylifeup.com/raspberry-pi-mysql/
# install DHT library for Raspberry Pi sudo pip3 install Adafruit_DHT
# install qt5?? see notes from powerpoint
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
mycursor.execute("CREATE TABLE sensordata ( timestamp VARCHAR(30),temp float(10,2), humid float(10,2))")


from PyQt5 import QtCore, QtGui, QtWidgets



class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dh22 Sensor Interface")
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
        self.alarm_message.setGeometry(QtCore.QRect(760, 90, 171, 81))
        self.alarm_message.setObjectName("alarm_message")
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
        
        #setup timer for periodic readings
        self.read_timer = QtCore.QTimer(self)
        self.read_timer.setSingleShot(False)
        self.read_timer.timeout.connect(self.get_instant_sensor_data)
        self.read_timer.start(1000)
        
        
        
        
        self.read_data_btn.clicked.connect(self.get_instant_sensor_data)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
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



    #get timestamp, temperature in celsius, and humidity for readings on demand
    def get_instant_sensor_data(self):
        try:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                temperature = "{0:0.2f}".format(temperature)
                humidity = "{0:0.2f}".format(humidity)
                time = str(datetime.datetime.now())
                self.read_data_out.setText(time + "       Temperature : " + temperature+"*C " + "  Humidity : "+ humidity+"%")
            else:
                self.read_data_out.setText("Failed to retrieve sensor data. Check DHT22 sensor connection.")
        except:
            self.read_data_out.setText("Sensor Error")
            



    #get timestamp, temperature in celsius, and humidity. 
    def get_sensor_data(self):
        try:
            humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                temperature = "{0:0.2f}".format(temperature)
                humidity = "{0:0.2f}".format(humidity)
                time = str(datetime.datetime.now())
                print(time + " Temperature = " + temperature+"*C " + "Humidity= "+ humidity+"%")
                return (time, temperature, humidity)
            else:
                print("Failed to retrieve sensor data. Check DHT22 sensor connection.")
                time = str(datetime.datetime.now())
                return (time, "0.0", "0.0")
        except:
            print("Sensor Error")
            time = str(datetime.datetime.now())
            return (time, "0.0", "0.0")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

