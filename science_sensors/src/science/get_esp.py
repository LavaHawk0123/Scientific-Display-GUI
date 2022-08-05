import socket
import rospy

rospy.init_node('moisture_sensor')
s = socket.socket()
s.bind(('192.168.1.169', 11520))
s.listen(0)
while True:
    client, addr = s.accept()
    while True:
        content = client.recv(32)
        if len(content) == 0:
           break
        else:
            print(content)
            rospy.set_param("/hyd/moisture",content)
    client.close()