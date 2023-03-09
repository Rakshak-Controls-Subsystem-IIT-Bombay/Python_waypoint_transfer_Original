import rospy
import mavros
import os
from std_msgs.msg import Float64
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Vector3
from mavros_msgs.msg import Waypoint, WaypointList, CommandCode
from mavros import mission as M
from mavros_msgs.srv import WaypointPull, WaypointPush, WaypointClear, WaypointSetCurrent, WaypointPushRequest
import time

#refer https://mavlink.io/en/messages/common.html for information regarding waypoints parameters

def waypoint_push_client(data):
    waypoint_clear_client()
    wl = WaypointList()
    wp = Waypoint()
    wp.frame = 3
    wp.command = 22  # takeoff
    wp.is_current = True
    wp.autocontinue = True
    wp.param1 = data[0]['altitude']  # takeoff altitude
    wp.param2 = 0
    wp.param3 = 0
    wp.param4 = 0
    wp.x_lat = data[0]['latitude']
    wp.y_long = data[0]['longitude']
    wp.z_alt = data[0]['altitude']
    wl.waypoints.append(wp)

    for point in data:
        wp1 = Waypoint()
        wp1.frame = 3
        wp1.command = 16  # simple waypoint
        wp1.is_current = False
        wp1.autocontinue = True
        wp1.param1 = 0  
        wp1.param2 = 0
        wp1.param3 = 0
        wp1.param4 = 0
        wp1.x_lat = point['latitude']
        wp1.y_long = point['longitude']
        wp1.z_alt = point['altitude']
        wl.waypoints.append(wp1)

    
    service = rospy.ServiceProxy('mavros/mission/push', WaypointPush)
    service.call(0, wl.waypoints)

    data = [{'altitude' : 10,'latitude' : 19.133848,'longitude' : 72.913116},{'altitude' : 10,'latitude' : 19.133858,'longitude' : 72.913373},
    {'altitude' : 15,'latitude' : 19.133742,'longitude' : 72.913261}, {'altitude' : 10,'latitude' : 19.134391,'longitude' : 72.912515}]
    
    wl1 = WaypointList()
    wp1 = Waypoint()
    wp1.frame = 3
    wp1.command = 16  # simple waypoint
    wp1.is_current = False
    wp1.autocontinue = True
    wp1.param1 = 0  
    wp1.param2 = 0
    wp1.param3 = 0
    wp1.param4 = 0
    wp1.x_lat = data[-1]['latitude']
    wp1.y_long = data[-1]['longitude']
    wp1.z_alt = data[-1]['altitude']
    wl1.waypoints.append(wp1)
    
    
    wp = Waypoint()
    wp.frame = 3
    wp.command = 21  # landing
    wp.is_current = False
    wp.autocontinue = True
    wp.param1 = 0
    wp.param2 = 0
    wp.param3 = 0
    wp.param4 = 0
    wp.x_lat = data[-1]['latitude']
    wp.y_long = data[-1]['longitude']
    wp.z_alt = data[-1]['altitude']
    wl1.waypoints.append(wp)
       
    time.sleep(150)
    
    service = rospy.ServiceProxy('mavros/mission/push', WaypointPush)
    if service.call(0, wl1.waypoints).success:
    	print('New waypoint')


def waypoint_clear_client():
        try:
            response = rospy.ServiceProxy(
                'mavros/mission/clear', WaypointClear)
            return response.call().success
        except rospy.ServiceException as e:
            print ("Service call failed: %s" %(e))
            return False

#the data dictionary contains the waypoint data
data = [{'altitude' : 10,'latitude' : 19.133848,'longitude' : 72.913116},{'altitude' : 10,'latitude' : 19.133858,'longitude' : 72.913373},{'altitude' : 15,'latitude' : 19.133742,'longitude' : 72.913261}]
waypoint_push_client(data)
