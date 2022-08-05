#!/usr/bin/env python3
import socket
import time
from signal import signal, SIGPIPE, SIG_DFL
import rospy
import threading


class get_params:

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
        self.port4 = 12345
        print("Connected to IP : {}".format(self.IP))
        print("Connected to Port : {}".format(self.port4))

        self.msg = ''

        # Socket Declerations
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_gui(self):
        # binding port and host
        self.s.bind((self.IP, self.port4))
        print("Waiting for client to connect")
        # waiting for a client to connect
        self.s.listen(5)
        c, addr = self.s.accept() 
        while True:
            self.msg = rospy.get_param('sm_gui_msg')
            # sending data type should be string and encode before sending
            print("sent msg : {}".format(self.msg))
            c.send(self.msg.encode())
            time.sleep(5)


if __name__ == '__main__':
    rospy.init_node('sending_socket_node')
    sock_obj = get_params()
    sock_obj.connect_to_gui()
