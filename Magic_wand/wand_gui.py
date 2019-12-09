# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wand_gui.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
import mysql.connector
import datetime
import time

#create a databas connection
mydb = mysql.connector.connect(host="localhost",user="admin",passwd="mfeid123",
                               database='magicwanddb')
mycursor = mydb.cursor()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(921, 655)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.lastimage_button = QtWidgets.QPushButton(self.centralwidget)
        self.lastimage_button.setGeometry(QtCore.QRect(30, 80, 151, 61))
        self.lastimage_button.setObjectName("lastimage_button")
        self.stat_line2_label = QtWidgets.QLabel(self.centralwidget)
        self.stat_line2_label.setGeometry(QtCore.QRect(60, 480, 631, 41))
        self.stat_line2_label.setText("")
        self.stat_line2_label.setObjectName("stat_line2_label")
        self.stat_line3_label = QtWidgets.QLabel(self.centralwidget)
        self.stat_line3_label.setGeometry(QtCore.QRect(60, 530, 621, 41))
        self.stat_line3_label.setText("")
        self.stat_line3_label.setObjectName("stat_line3_label")
        self.stat_line1_label = QtWidgets.QLabel(self.centralwidget)
        self.stat_line1_label.setGeometry(QtCore.QRect(60, 430, 631, 41))
        self.stat_line1_label.setText("")
        self.stat_line1_label.setObjectName("stat_line1_label")
        self.imagedisplay_label = QtWidgets.QLabel(self.centralwidget)
        self.imagedisplay_label.setGeometry(QtCore.QRect(280, 50, 551, 281))
        self.imagedisplay_label.setObjectName("imagedisplay_label")
        self.imagedisplay_label.setScaledContents(True)
        self.image_data_label = QtWidgets.QLabel(self.centralwidget)
        self.image_data_label.setGeometry(QtCore.QRect(280, 350, 531, 41))
        self.image_data_label.setObjectName("image_data_label")
        self.stattistics_button = QtWidgets.QPushButton(self.centralwidget)
        self.stattistics_button.setGeometry(QtCore.QRect(30, 170, 151, 61))
        self.stattistics_button.setObjectName("stattistics_button")
        self.close_button = QtWidgets.QPushButton(self.centralwidget)
        self.close_button.setGeometry(QtCore.QRect(30, 250, 151, 61))
        self.close_button.setObjectName("close_button")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 390, 111, 31))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #retrieve last image taken on  button press
        self.lastimage_button.clicked.connect(self.get_last_image)

        #close gui on button press
        self.close_button.clicked.connect(self.close_program)

        #update statistics on button press
        self.stattistics_button.clicked.connect(self.update_statistics)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lastimage_button.setText(_translate("MainWindow", "Last Picture Taken"))
        self.imagedisplay_label.setText(_translate("MainWindow", "Last Image taken by wand."))
        self.image_data_label.setText(_translate("MainWindow", "Image information"))
        self.stattistics_button.setText(_translate("MainWindow", "Update Statistics"))
        self.close_button.setText(_translate("MainWindow", "Close Program"))
        self.label_3.setText(_translate("MainWindow", "Statistics"))

    def get_last_image(self):
        #log: retrieving last image taken
        self.imagedisplay_label.setPixmap(QPixmap('capture_from_s3.jpg'))
        mycursor.execute("SELECT COUNT(*) FROM label_data ") # get total number of labels from label table
        number_of_labels = mycursor.fetchall()
        number_of_labels= number_of_labels[0][0]

        mycursor.execute("SELECT image_label, time FROM label_data ")
        myresult= mycursor.fetchall()
        latest_label=myresult[number_of_labels-1]
        awslabel=latest_label[0]
        image_capture_time=latest_label[1]

        self.image_data_label.setText("Image Label: "+awslabel+"               Image captured on "+image_capture_time)


    def close_program(self):
        sys.exit(app.exec_())

    # get % of correct recorded commands and % of correct labels from aws
    def update_statistics(self):
        mycursor.execute("SELECT COUNT(*) FROM command_data ") # get total number of commands from command table
        number_of_commands = mycursor.fetchall()
        number_of_commands= number_of_commands[0][0]

        mycursor.execute("SELECT is_valid FROM command_data ") # get number of valid commands from command table
        myresult = mycursor.fetchall()
        number_of_valid_commands = 0
        for x in myresult:
            if '1' in x: #valid commands are recorded with '1' in the "is_valid" column of the table
                number_of_valid_commands = number_of_valid_commands +1

        mycursor.execute("SELECT COUNT(*) FROM label_data ") # get total number of labels from label table
        number_of_labels = mycursor.fetchall()
        number_of_labels= number_of_labels[0][0]


        mycursor.execute("SELECT result FROM label_data ") # get number of correct labels from label table
        myresult = mycursor.fetchall()
        number_of_correct_labels = 0
        for x in myresult:
            if 'correct' in x:
                number_of_correct_labels = number_of_correct_labels+1


        command_success_rate= ((number_of_valid_commands)/(number_of_commands) ) * 100
        label_success_rate =  ((number_of_correct_labels)/(number_of_labels) ) * 100


        self.stat_line1_label.setText("Percent of recorded commands marked as valid: "+str(command_success_rate)+"%" + "         Total commands recorded: " + str(number_of_commands))
        self.stat_line2_label.setText("Percent of correct labels from AWS: "+str(label_success_rate)+"%" + "         Total labels recorded: " + str(number_of_labels))
        self.stat_line3_label.setText("Statistics updated at "+str(datetime.datetime.now()))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
