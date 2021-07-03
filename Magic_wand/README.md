# EID Project6: Magic Wand Super Project  

## Author: Michael Finale

## Block Diagram

![image](https://user-images.githubusercontent.com/10779404/124338568-aa9d6e00-db76-11eb-90bf-efee0180d291.png)

## Notes and Installation Instructions


### On the Server Rasberry Pi
- clone repo from https://github.com/mfinale/Embedded-Interface-design-class.git
- install mySQL driver for python3 by running the following command from the terminal `sudo pip3 install mysql-connector`
- install mySQL `sudo apt install mariadb-server`
- Install PyQT5 : 
`sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools`
`sudo apt-get install qttools5-dev-tools`
- create a local mySQL database with the following name, user, and password info:
-user="admin"
-passwd="mfeid123"  
-database=magicwanddb
- Reference https://pimylifeup.com/raspberry-pi-mysql/ if more detailed instructions are needed.

- setup boto and aws credentials:
- With Python3 and pip installed run the following commands from the terminal 
- to install boto 3 `sudo pip3 install boto3` 
- to install aws cli `sudo pip3 install awscli`  
- ensure the correct credentials information is stored in ~/.aws/credentials
- navigate to "Magic_wand" folder
- run the following command in one terminal `python3 server.py`
- run the following command in a second terminal `python3 wand_gui.py`

### On the Client Rasberry Pi

- wire pushbutton to raspberry pi as shown in the figure below :
 ![](http://razzpisampler.oreilly.com/images/rpck_1101.png)
- install usb mic into a usb port
- plug speaker into audio port 
- clone repo from https://github.com/mfinale/Embedded-Interface-design-class.git
- setup boto and aws credentials:
- With Python3 and pip installed run the following commands from the terminal 
- to install boto 3 `sudo pip3 install boto3` 
- to install aws cli `sudo pip3 install awscli`  
- ensure the correct credentials information is stored in ~/.aws/credentials
- to install pygame `sudo python3 -m pip install -U pygame --user` 
- to install picamera `sudo pip3 install picamera` 
- to install pydub `sudo pip3 install pydub` 
- to install Rasberry Pi GPIO library `sudo pip3 install RPi.GPIO` 

- navigate to "Magic_wand" folder
- run the following command in one terminal `python3 clientpi.py`

## References 
- [1] http://razzpisampler.oreilly.com/images/rpck_1101.png

## Project Work
Application developed by Michael Finale.  







