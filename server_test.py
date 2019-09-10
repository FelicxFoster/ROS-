import socket
import threading

import rospy
from nav_msgs.msg import Odometry
# from geometry_msgs.msg import Twist, Point, Quaternion

def odom_callback(msg):
    """
    New Odometry Received
    """
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",msg)

    Sequence = msg.header.seq
    Stamp = msg.header.stamp
    FrameID = msg.header.frame_id
    ChildFrameId = msg.child_frame_id
    Position_x = msg.pose.pose.position.x
    Position_y = msg.pose.pose.position.y
    Position_z = msg.pose.pose.position.z
    Orientation_x = msg.pose.pose.orientation.x
    Orientation_y = msg.pose.pose.orientation.y
    Orientation_z = msg.pose.pose.orientation.z
    Orientation_w = msg.pose.pose.orientation.w
    Covariance = msg.pose.covariance

    path_to_send.append(Sequence)
    path_to_send.append(Stamp)
    path_to_send.append(FrameID)
    path_to_send.append(ChildFrameId)
    path_to_send.append(Position_x)
    path_to_send.append(Position_y)
    path_to_send.append(Position_z)
    path_to_send.append(Orientation_x)
    path_to_send.append(Orientation_y)
    path_to_send.append(Orientation_z)
    path_to_send.append(Orientation_w)
    path_to_send.append(Covariance)


def tcp_server():   
    session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    addr = ('172.17.0.1', 9999)
    session.bind(addr)
    session.listen(1)
    rospy.loginfo("Waiting for connection...ip_port=%s:%s" % addr)       
    while True:
        sock, addr = session.accept()
        thread = threading.Thread(target=tcplink, args=(sock, addr))
        thread.start()        

def tcplink(sock, addr):
    rospy.loginfo('new connection from: %s:%s.' % addr)       

    while True:
        data = sock.recv(1024*10) # 10KB
        if data == 'exit' or not data:
            rospy.loginfo("TCP server receive exit command.")
            break
        data_str = data[1:-1].replace(' ', '')
        data_list = data_str.split(',')
        if len(data_list) != 3:
            rospy.loginfo("received error msg: %s." % data)
            break
        sock.sendall("%s" % str(path_to_send))
    sock.close()
    rospy.loginfo("close connection from: %s:%s." % addr)

def main():
    """
    Main rosnode
    """
    rospy.init_node('socket_server', anonymous=True)
    rospy.Subscriber('/odom', Odometry, odom_callback)

    tcp_thread = threading.Thread(target=tcp_server, args=())
    tcp_thread.start()
    
    rospy.spin()


if __name__ == '__main__':
    path_to_send = []
    main()
