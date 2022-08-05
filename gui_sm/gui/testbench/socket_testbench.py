#!/usr/bin/env python3
import socket
import time
from signal import signal, SIGPIPE, SIG_DFL
import rospy
import threading


class Connect_Socket:

    def __init__(self):
        signal(SIGPIPE, SIG_DFL)
        self.L = []
        # Variable Declerations
        host = socket.gethostname()
        self.IP = socket.gethostbyname(host)
        self.IP_add = "192.168.1.99"
        self.IP_add_c2 = "192.168.1.102"
        self.IP_add_c1 = "192.168.1.101"
        self.port1 = 502
        self.port2 = 9047
        self.port3 = 9058
        self.port4 = 9992
        self.colorpal_r_lambda = 12
        self.colorpal_g_lambda = 12
        self.colorpal_b_lambda = 12
        self.colorpal_r = 12
        self.colorpal_g = 12
        self.colorpal_b = 12
        self.CO2 = 0
        self.methane_ppm = 0
        self.ozone_ppb = 0
        self.spectral = ''
        self.voc_ppm = 0
        self.hyd_moisture = 0
        self.hyd_cond = 0
        self.hyd_temp = 0
        self.msg = ''

        # Socket Declerations
        self.s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Thread Declerations
        self.th_send_data_function = threading.Thread(target=self.send_data_func)

    def send_data_func(self):
        # binding port and host
        self.s1.bind((self.IP, self.port4))
        print("Waiting for client to connect")
        # waiting for a client to connect
        self.s1.listen(5)
        c, addr = self.s1.accept() 
        while True:
            self.msg = rospy.get_param('sm_gui_msg')
            # sending data type should be string and encode before sending
            c.send(self.msg.encode())
        
    
    def Testbench(self):
        while not rospy.is_shutdown():
            print("connection established")
            time.sleep(1)
            self.CO2 = rospy.get_param("/CCS811/CO2")
            self.voc_ppm = rospy.get_param("/CCS811/tVOC")
            self.ozone_ppb = rospy.get_param('/aero/O3')
            self.spectral = rospy.get_param('/spectral')
            self.hyd_moisture = rospy.get_param('/hyd/moisture')
            self.msg = str(self.hyd_moisture) + ","+str(self.ozone_ppb)+","+str(self.voc_ppm)+","+str(self.CO2)+","+str(self.spectral)
            rospy.set_param('sm_gui_msg',self.msg)
            print("Updated Message")
            time.sleep(5)


if __name__ == '__main__':
    rospy.init_node('test_sender')
    sock_obj = Connect_Socket()
    sock_obj.Testbench()
