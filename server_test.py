#!/usr/bin/env python

# -*- coding:utf8 -*-

import socket
import threading
import rospy
from nav_msgs.msg import Odometry

class Socket_odom(object):
    def __init__(self):
        rospy.init_node('socket_server', anonymous=True)
        self.subscriber = rospy.Subscriber('/odom', Odometry, self.odom_callback)


    def odom_callback(self,msg):
        """
        New Odometry Received
        """
        # rospy.loginfo(rospy.get_caller_id()+"I heard %s",msg)
        self.Sequence = msg.header.seq
        self.Stamp = msg.header.stamp
        self.FrameID = msg.header.frame_id
        self.ChildFrameId = msg.child_frame_id
        self.Position_x = msg.pose.pose.position.x
        self.Position_y = msg.pose.pose.position.y
        self.Position_z = msg.pose.pose.position.z
        self.Orientation_x = msg.pose.pose.orientation.x
        self.Orientation_y = msg.pose.pose.orientation.y
        self.Orientation_z = msg.pose.pose.orientation.z
        self.Orientation_w = msg.pose.pose.orientation.w
        self.Covariance = msg.pose.covariance
        # path_to_send.append(Sequence)
        # path_to_send.append(Stamp)
        # path_to_send.append(FrameID)
        # path_to_send.append(ChildFrameId)

        path_to_send.append(self.Position_x)
        path_to_send.append(self.Position_y)
        path_to_send.append(self.Position_z)
        path_to_send.append(self.Orientation_x)
        path_to_send.append(self.Orientation_y)
        path_to_send.append(self.Orientation_z)
        path_to_send.append(self.Orientation_w)
        # path_to_send.append(Covariance)

    def tcp_server(self):   
        # 创建服务端的socket对象
        session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        addr = ('172.17.0.1', 9000)
        # 绑定一个ip和端口
        session.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        # session.serversocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        session.bind(addr)
        # 服务器端一直监听是否有客户端进行连接
        session.listen(1)
        rospy.loginfo("Waiting for connection...ip_port=%s:%s" % addr)       
        while True:
            # 如果有客户端进行连接、则接受客户端的连接
            sock, addr = session.accept()
            thread = threading.Thread(target=self.tcplink, args=(sock, addr))
            thread.start()        

    def tcplink(self, sock, addr):
        rospy.loginfo('new connection from: %s:%s.' % addr)       
        while True:
            # 客户端与服务端进行通信
            data = sock.recv(1024*100) # 10KB
            if data == 'exit' or not data:
                rospy.loginfo("TCP server receive exit command.")
                break
            data_str = data[1:-1].replace(' ', '')
            data_list = data_str.split(',')
            if len(data_list) != 3:
                rospy.loginfo("received error msg: %s." % data)
                break
            sock.sendall("%s" % str(path_to_send[0:7]))
            # rospy.loginfo(str(path_to_send))
            print(str(path_to_send[0:7])+"/////////////////////")
        sock.close()
        rospy.loginfo("close connection from: %s:%s." % addr)

def main():
        """
        Main rosnode
        """
        socket_odom = Socket_odom()
        tcp_thread = threading.Thread(target=socket_odom.tcp_server, args=())
        tcp_thread.start()  
        rospy.spin()

if __name__ == '__main__':
    # socket_odom = Socket_odom()
    path_to_send = []
    main()

    

    

