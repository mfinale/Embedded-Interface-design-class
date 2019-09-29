# EID Project2: ------ 

## Author: Michael Finale
## Installation Instructions
- clone repo from https://github.com/mfinale/Embedded-Interface-design-class.git
- install mySQL sriver for python3 by running the following command from the terminal `sudo pip3 install mysql-connector`
- install mySQL `sudo apt install mariadb-server`

- install DHT library for Raspberry Pi: `sudo pip3 install Adafruit_DHT`

- wire dht sensor to raspberry pi as shown in the figure below[7] :
 
Install nvm, node, and npm•curl -o-https://raw.githubusercontent.com/creationix/nvm/v0.34.0/install.sh | bash•Restart your terminal•nvm –version•Should return a version number like 0.34.0•nvm install node •This installs the latest node, 12.9.0•nvm install 10.16.3•This installs the stable LTS 10.16.3 node


![](https://cdn.pimylifeup.com/wp-content/uploads/2019/05/Raspberry-Pi-Humidity-Sensor-DHT22-Wiring-Schematic.png)

- Install PyQT5 : 
`sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools`
`sudo apt-get install qttools5-dev-tools`
- create a local mySQL database with the following name, user, and password info:
-user="eiduser"
-passwd="Shrek2"  
-database=sensordb
- Reference https://pimylifeup.com/raspberry-pi-mysql/ if more detailed instructions are needed.
- navigate to "project1" folder
- run project1gui.py `python3 project1gui.py`

## Project Work
Application developed by Michael Finale.  

## Project Additions

## References
- [1]https://www.geeksforgeeks.org/python-introduction-matplotlib/
- [2]https://doc.qt.io/qtforpython/PySide2/QtCore/QTimer.html
- [3]https://pythonspot.com/pyqt5-image/
- [4]https://pynative.com/python-mysql-insert-data-into-database-table/
- [5]https://pimylifeup.com/raspberry-pi-mysql/
- [6]https://www.w3schools.com/python/python_mysql_create_db.asp
- [7]https://pimylifeup.com/raspberry-pi-humidity-sensor-dht22/
