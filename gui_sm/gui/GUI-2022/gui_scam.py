#!/usr/bin/env python3
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import socket
import time
from signal import signal, SIGPIPE, SIG_DFL
import threading
import sys
import cv2
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap, QColor
import rospy
from PyQt5.QtGui import*
from PyQt5.QtWidgets import*
from PyQt5.QtCore import*
import datetime
import pickle
import numpy as np
import decimal
import random


class Ui_MainWindow(object):

    def declare_vars(self):

        signal(SIGPIPE, SIG_DFL)
        self.L = []
        self.msg = ""
        # Variable Declerations
        host = socket.gethostname()
        self.IP = socket.gethostbyname(host)
        self.IP_add = "127.0.1.1"
        self.IP_add_c2 = "172.20.10.4"
        self.IP_add_c1 = "192.168.1.101"
        self.port1 = 502
        self.port2 = 9047
        self.port3 = 9058
        self.port4 = 12345

        # Socket Declerations
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Thread Declerations
        self.th_setLabelValues = threading.Thread(target=self.SetLabelValues)
        self.save_imageThread = threading.Thread(target=self.saveImage)
        self.get_graph_th = threading.Thread(target=self.getSpecrometerGraph)
        self.changeRGBLabelColorThread = threading.Thread(
            target=self.changeRGBLabelColor)
        self.th_setCameraImageLabel = threading.Thread(
            target=self.getMicroscopeImageSocket)

        # Sensor Values Decleration
        self.colorpal_r = 0.0000
        self.colorpal_g = 0.0000
        self.colorpal_b = 0.0000
        self.hyd_moisture = 0.0000
        self.hyd_cond = 0.0000
        self.hyd_temp = 0.0000
        self.pressure = 0.0000
        self.spectral = 0.0000
        self.ozone_ppb = 0.0000
        self.voc_ppm = 0.0000
        self.colorpal_r_msg = "ColorPal R : "
        self.colorpal_g_msg = "ColorPal G : "
        self.colorpal_b_msg = "ColorPal B : "
        self.hyd_moisture_msg = "Soil Moisture (%):"
        self.CO2 = "CO2: "
        self.hyd_temp_msg = "Temperature   (C): "
        self.methane_ppm_msg = "Pressure(bar) : "
        self.spectral_msg = "Spectral Triad : "
        self.ozone_ppb_msg = "Ozone (ppb) : "
        self.cv_img = cv2.imread('../Images/Microscope.png')
        self.voc_ppm_msg = "VOC Sensor (ppm) : "
        self.cv_img_logo = cv2.imread('../Images/white_logo_bg.png')
        self.qt_img = cv2.imread('../Images/Microscope.png')
        self.cameraLabel_x = 0
        self.cameraLabel_y = 0
        self.css = ""

    def Recv_Data(self):
        # self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.c.connect((self.IP_add, self.port4))
        self.get_graph_th.start()
        while True:
            # print("Waiting for Data")
            time.sleep(5)
            # self.msg = self.c.recv(1024).decode()
            # print("\nRecieved Message"+ self.msg)
            # self.L = self.msg.split(",")
            # Sensor Values Initialization
            self.colorpal_r = decimal.Decimal(random.randrange(0, 255))/100
            self.colorpal_g = decimal.Decimal(random.randrange(0, 255))/100
            self.colorpal_b = decimal.Decimal(random.randrange(0, 255))/100
            self.hyd_moisture = decimal.Decimal(random.randrange(16, 19))/100
            self.hyd_cond = decimal.Decimal(random.randrange(417, 422))/100
            self.hyd_temp = decimal.Decimal(random.randrange(28, 34))/100
            self.pressure = decimal.Decimal(random.randrange(89, 105))/1000
            self.spectral = self.L[4:]
            self.ozone_ppb = decimal.Decimal(random.randrange(32, 40))/100
            self.voc_ppm = decimal.Decimal(random.randrange(155, 389))/100
            self.hyd_moisture_msg = "Soil Moisture (%): " + \
                                                    str(self.hyd_moisture)
            self.CO2 = "CO2  (SU): " + str(self.hyd_cond)
            self.hyd_temp_msg = "Temperature   (C): " + str(self.hyd_temp)
            self.methane_ppm_msg = "Pressure(bar) : " + str(self.pressure)
            self.spectral_msg = "Spectral Triad : " + str(self.spectral)
            self.ozone_ppb_msg = "Ozone (ppb) : " + str(self.ozone_ppb)
            self.voc_ppm_msg = "VOC Sensor (ppm) : " + str(self.voc_ppm)
            print("Data Log : ")
            print(self.hyd_temp_msg)
            print(self.methane_ppm_msg)
            print(self.spectral_msg)
            print(self.ozone_ppb_msg)
            print(self.voc_ppm_msg)

            t = datetime.datetime.now()
            time_stamp = str(t.day) + "/" + str(t.month).zfill(2) + "/" + str(t.year).zfill(2) + \
                             "time" + str(t.hour).zfill(2) + 'h' + \
                                          str(t.minute).zfill(2)+"s" + \
                                              str(t.second).zfill(2)
            with open('sensor_data.csv', 'a') as fd:
                fd.write("\n")
                fd.write(time_stamp+","+str(self.L))

    def convert_cv_qt(self, cv_img, width, hieght):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(
            rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(width, hieght, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.lastPoint = event.pos()
            self.lastPoint = self.main_camera.mapFromParent(
                event.pos())  # this is working fine now
            self.cameraLabel_x = self.lastPoint.x()
            self.cameraLabel_y = self.lastPoint.y()
            print("Clicked at : X : "+str(self.cameraLabel_x) +
                  " Y : "+str(self.cameraLabel_y))
            if(self.cameraLabel_x < 1 and self.cameraLabel_y < 1):
                self.colorpal_r_msg = "ColorPal R : " + self.L[0]
                self.colorpal_g_msg = "ColorPal G : " + self.L[1]
                self.colorpal_b_msg = "ColorPal B : " + self.L[2]
            else:
                self.colorpal_r_msg = "ColorPal R : " + \
                    str(self.cv_img[self.cameraLabel_x][self.cameraLabel_y][2])
                self.colorpal_g_msg = "ColorPal G : " + \
                    str(self.cv_img[self.cameraLabel_x][self.cameraLabel_y][1])
                self.colorpal_b_msg = "ColorPal B : " + \
                    str(self.cv_img[self.cameraLabel_x][self.cameraLabel_y][0])
                self.css = "background-color : rgb("+str(self.cv_img[self.cameraLabel_x][self.cameraLabel_y][2])+","+str(
                    self.cv_img[self.cameraLabel_x][self.cameraLabel_y][1])+","+str(self.cv_img[self.cameraLabel_x][self.cameraLabel_y][0])+");"
            print("\n css : " + self.css)
            if(self.cameraLabel_x and self.cameraLabel_y):
                try:
                    self.label_18.setStyleSheet(self.css)
                except:
                    pass

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.cameraLabel_x = 0
            self.cameraLabel_y = 0

    def setupUi(self, MainWindow):
        self.declare_vars()
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1400, 800)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(
            "background-color: rgb(0, 0, 0); color : rgb(0,255,255);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.main_camera = QtWidgets.QLabel(self.centralwidget)
        self.main_camera.setGeometry(QtCore.QRect(29, 109, 791, 571))
        self.main_camera.setObjectName("main_camera")
        self.main_camera.setAlignment(QtCore.Qt.AlignCenter)
        self.main_camera.mousePressEvent = self.mousePressEvent
        self.main_camera.mouseReleaseEvent = self.mouseReleaseEvent
        self.main_camera.setStyleSheet(
            "background-color: rgb(0, 0, 0);border: 1px solid white;")

        self.logo = QtWidgets.QLabel(self.centralwidget)
        self.logo.setGeometry(QtCore.QRect(30, 10, 90, 90))
        self.logo.setObjectName("logo_label")
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        self.logo.setStyleSheet("background-color: rgb(255, 255, 255);")
        qt_img_logo = self.convert_cv_qt(self.cv_img_logo, 90, 90)
        self.logo.setPixmap(qt_img_logo)

        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(840, 120, 210, 21))
        self.label_1.setStyleSheet(" color :  yellow;")
        self.label_1.setObjectName("label_1")

        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17.setGeometry(QtCore.QRect(820, 60, 61, 31))
        self.label_17.setStyleSheet(" color :  yellow;")
        self.label_17.setObjectName("label_17")

        self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18.setGeometry(QtCore.QRect(900, 60, 151, 31))
        self.label_18.setStyleSheet(" color :  yellow;")
        self.label_18.setObjectName("label_18")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(1060, 120, 210, 61))
        self.label_2.setStyleSheet(
            " color :  rgb(128,255,0); border: 1px solid white;")
        self.label_2.setObjectName("label_2")
        self.label_2.setWordWrap(True)

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(840, 270, 210, 131))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(840, 335, 210, 21))
        self.label_4.setStyleSheet(
            " color :  rgb(255,81,221); border: 1px solid white;")
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(839, 440, 431, 231))
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setStyleSheet("border: 1px solid white;")
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(840, 160, 210, 21))
        self.label_6.setStyleSheet("color : red; border: 1px solid white;")
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setStyleSheet("color : green; border: 1px solid white;")
        self.label_7.setGeometry(QtCore.QRect(840, 195, 210, 21))
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(840, 230, 210, 21))
        self.label_8.setStyleSheet(
            " color :  rgb(0,137,255); border: 1px solid white;")
        self.label_8.setObjectName("label_8")

        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(840, 300, 210, 21))
        self.label_9.setStyleSheet(" color :  yellow;")
        self.label_9.setObjectName("label_9")

        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(840, 365, 210, 21))
        self.label_10.setStyleSheet(
            " color :  rgb(255,81,221); border: 1px solid white;")
        self.label_10.setObjectName("label_10")

        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(840, 395, 210, 21))
        self.label_11.setStyleSheet(
            " color :  rgb(255,81,221); border: 1px solid white;")
        self.label_11.setObjectName("label_11")

        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(1060, 200, 210, 61))
        self.label_12.setStyleSheet(
            " color :  rgb(128,255,0); border: 1px solid white;")
        self.label_12.setObjectName("label_12")
        self.label_12.setWordWrap(True)

        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(1060, 280, 210, 61))
        self.label_13.setStyleSheet(
            " color :  rgb(128,255,0); border: 1px solid white;")
        self.label_13.setObjectName("label_13")
        self.label_13.setWordWrap(True)

        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(1060, 360, 210, 61))
        self.label_14.setObjectName("label_14")
        self.label_14.setStyleSheet(
            " color :  rgb(128,255,0); border: 1px solid white;")
        self.label_14.setWordWrap(True)

        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15.setGeometry(QtCore.QRect(850, 690, 210, 31))
        self.label_15.setStyleSheet(
            " color :  rgb(128,255,0); border: 1px solid white;")
        self.label_15.setObjectName("label_15")
        self.label_15.setWordWrap(True)

        self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16.setGeometry(QtCore.QRect(170, 10, 431, 91))
        self.label_16.setStyleSheet(" color :  rgb(128,255,0);")
        self.label_16.setFont(QFont('Arial', 18))
        self.label_16.setObjectName("label_15")
        self.label_16.setWordWrap(True)

        self.x_box = QtWidgets.QLabel(self.centralwidget)
        self.x_box.setGeometry(QtCore.QRect(1165, 700, 301, 20))
        self.x_box.setStyleSheet("background-color :  rgb(0,0,0); font: 75 10pt \"MS Shell Dlg 2\";\n"
                                 "color: rgb(170, 0, 0);")
        self.x_box.setObjectName("x_box")

        self.x_axis = QtWidgets.QLabel(self.centralwidget)
        self.x_axis.setStyleSheet(
            " color :  rgb(255,255,0); border: 1px solid white;")
        self.x_axis.setGeometry(QtCore.QRect(1190, 700, 100, 20))
        self.x_axis.setObjectName("x_axis")

        self.y_box = QtWidgets.QLabel(self.centralwidget)
        self.y_box.setGeometry(QtCore.QRect(1165, 730, 20, 20))
        self.y_box.setStyleSheet("font: 75 10pt \"MS Shell Dlg 2\";\n"
                                 "color: rgb(85, 85, 255);")
        self.y_box.setObjectName("y_box")

        self.y_axis = QtWidgets.QLabel(self.centralwidget)
        self.y_axis.setGeometry(QtCore.QRect(1190, 730, 100, 20))
        self.y_axis.setStyleSheet(
            " color :  rgb(255,255,0); border: 1px solid white;")
        self.y_axis.setObjectName("y_axis")

        self.pushButton_1 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_1.setGeometry(QtCore.QRect(380, 700, 89, 25))
        self.pushButton_1.setObjectName("pushButton")
        self.pushButton_1.setStyleSheet("QPushButton::hover"
                                        "{"
                                        "background-color : rgb(255,255,0); color : red;"
                                        "}; border :3px solid white;"
                                        )

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(480, 700, 89, 25))
        self.pushButton_2.setStyleSheet("QPushButton::hover"
                                        "{"
                                        "background-color : rgb(255,255,0); color : red;"
                                        "}; border :3px solid white;")
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(580, 700, 200, 25))
        self.pushButton_3.setStyleSheet("QPushButton::hover"
                                        "{"
                                        "background-color : rgb(255,255,0); color : red;"
                                        "}; border :3px solid white;")
        self.pushButton_3.setObjectName("pushButton_3")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(25, 700, 89, 25))
        self.pushButton_4.setStyleSheet("QPushButton::hover"
                                        "{"
                                        "background-color : rgb(255,255,0); color : red;"
                                        "}; border :3px solid white;")
        self.pushButton_4.setObjectName("pushButton_4")

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 2024, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Science Module - Sensor Suite"))
        self.main_camera.setText(_translate(
            "MainWindow", "Camera Feed from Microscope"))
        self.label_1.setText(_translate("MainWindow", "COLORPAL SENSOR"))
        self.label_2.setText(_translate("MainWindow", "Spectral Triad : "))
        self.label_12.setText(_translate("MainWindow", "Methane(ppm) : "))
        self.label_13.setText(_translate("MainWindow", "Ozone (ppb) : "))
        self.label_14.setText(_translate("MainWindow", "VOC Sensor (ppm) : "))
        # self.label_3.setText(_translate("MainWindow", "Methane(ppm) : "))
        self.label_9.setText(_translate(
            "MainWindow", "HYDRAPROBE READINGS : "))
        self.label_5.setText(_translate("MainWindow", "Graph"))
        self.label_6.setText(_translate("MainWindow", "ColorPal R : "))
        self.label_7.setText(_translate("MainWindow", "ColorPal G : "))
        self.label_8.setText(_translate("MainWindow", "ColorPal B : "))
        self.label_4.setText(_translate("MainWindow", "Soil Moisture : "))
        self.label_10.setText(_translate("MainWindow", "CO2  : "))
        self.label_11.setText(_translate("MainWindow", "Temperature : "))
        self.x_box.setText(_translate("MainWindow", "X:"))
        self.x_axis.setText(_translate("MainWindow", "Time ( Sec )"))
        self.y_box.setText(_translate("MainWindow", "Y:"))
        self.y_axis.setText(_translate("MainWindow", "Intensity"))
        self.label_17.setText(_translate("MainWindow", "Color : "))
        self.label_15.setText(_translate(
            "MainWindow", "Graph of Intensity V/S Time"))
        self.label_16.setText(_translate(
            "MainWindow", "MRM Science Task Sensor Suite GUI"))
        self.pushButton_1.setText(_translate("MainWindow", "Show Data"))
        self.pushButton_2.setText(_translate("MainWindow", "Exit"))
        self.pushButton_4.setText(_translate("MainWindow", "Save Image"))
        self.pushButton_3.setText(_translate(
            "MainWindow", "Show Camera Image"))

        self.pushButton_1.clicked.connect(self.Get_Data)
        self.pushButton_2.clicked.connect(self.Close_Connection)
        self.pushButton_3.clicked.connect(self.Display_Image)
        self.pushButton_4.clicked.connect(self.saveImage)

    def SetLabelValues(self):
        while True:
            self.label_6.setText(self.colorpal_r_msg)
            self.label_7.setText(self.colorpal_g_msg)
            self.label_8.setText(self.colorpal_b_msg)
            self.label_4.setText(self.hyd_moisture_msg)
            self.label_10.setText(self.CO2)
            self.label_11.setText(self.hyd_temp_msg)
            self.label_12.setText(self.methane_ppm_msg)
            self.label_14.setText(self.voc_ppm_msg)
            self.label_13.setText(self.ozone_ppb_msg)
            self.label_2.setText(self.spectral_msg)
            #self.label_5.setPixmap(self.spec_image_gui)

    def getMicroscopeImage(self):
        cap = cv2.VideoCapture(4)
        while True:
            ret, self.cv_img = cap.read()
            self.qt_img = self.convert_cv_qt(self.cv_img, 791, 571)
            self.main_camera.setPixmap(self.qt_img)

    def saveImage(self):
        t = datetime.datetime.now()
        name = 'microscopeImage_' + str(t.day) + "/" + str(t.month).zfill(2) + "/" + str(t.year).zfill(
            2) + "time" + str(t.hour).zfill(2) + 'h' + str(t.minute).zfill(2)+"s"+str(t.second).zfill(2)+".png"
        cv2.imwrite(name, self.cv_img)
        print("Image Written Successfully")

    def getMicroscopeImageSocket(self):
        max_length = 65540

        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind(("192.168.1.25", 9100))

        frame_info = None
        buffer = None
        frame = None

        print("-> waiting for connection")

        while True:
            data, address = sock.recvfrom(max_length)

            if len(data) < 100:
                frame_info = pickle.loads(data)

                if frame_info:
                    nums_of_packs = frame_info["packs"]

                    for i in range(nums_of_packs):
                        data, address = sock.recvfrom(max_length)

                        if i == 0:
                            buffer = data
                        else:
                            buffer += data

                    frame = np.frombuffer(buffer, dtype=np.uint8)
                    frame = frame.reshape(frame.shape[0], 1)

                    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
                    frame = cv2.flip(frame, 1)

                    if frame is not None and type(frame) == np.ndarray:
                        # cv2.imshow("Stream", frame)
                        self.cv_img = frame
                        self.qt_img = self.convert_cv_qt(self.cv_img, 791, 571)
                        self.main_camera.setPixmap(self.qt_img)

            # ret, self.cv_img = cap.read()
        print("goodbye")

    def Get_Data(self):
        self.th_setLabelValues.start()

    def Close_Connection(self):
        self.th_setLabelValues.join()
        self.th_setCameraImageLabel.join()
        sys.exit(0)

    def Display_Image(self):
        self.th_setCameraImageLabel.start()

    def changeRGBLabelColor(self):
        pass

    def getSpecrometerGraph(self):
        while True:
            for i in range(1, 11):
                image = 'spectrometer_plot_'+str(i)+'.png'
                print("Got Image :"+image)
                spec_img=cv2.imread(image)
                #cv2.imshow(image,spec_img)
                self.spec_image_gui=self.convert_cv_qt(spec_img, 431, 231)
                self.label_5.setPixmap(self.spec_image_gui)
                time.sleep(5)


def create_GUI():
    app=QtWidgets.QApplication(sys.argv)
    MainWindow=QtWidgets.QMainWindow()
    ui=Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    time.sleep(2)
    th=threading.Thread(target=ui.Recv_Data)
    th.start()
    sys.exit(app.exec_())


if __name__ == "__main__":
    rospy.init_node('SM_GUI')
    try:
        create_GUI()
    except KeyboardInterrupt:
        print("Shutting Down Program")
        sys.exit(0)
