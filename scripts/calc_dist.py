#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseWithCovarianceStamped, PoseStamped, PolygonStamped, PointStamped, Point32
from visualization_msgs.msg import Marker

class CalcDist():
    def __init__(self):
        rospy.Subscriber("clicked_point", PointStamped, self.initial_cb)
        rospy.Subscriber("move_base_simple/goal", PoseStamped, self.goal_cb)
        self.poly_pub = rospy.Publisher("calc_polygon", PolygonStamped, queue_size=1)
        self.text_pub = rospy.Publisher("dist_txt", Marker, queue_size=1)
        self.start_pos = None
        self.goal_pos = None

    def initial_cb(self, _data):
        self.start_pos = _data.point
        self.calc_dist()

    def goal_cb(self, _data):
        self.goal_pos = _data.pose.position
        self.calc_dist()

    def calc_dist(self):
        if self.start_pos == None or self.goal_pos == None:
            rospy.logwarn("please check position of start and goal")
            return
        
        x = abs(self.goal_pos.x - self.start_pos.x)
        y = abs(self.goal_pos.y - self.start_pos.y)

        distance = (x ** 2 + y ** 2) ** 0.5

        rospy.loginfo("distance = {}".format(distance))
        poly = PolygonStamped()
        poly.header.stamp = rospy.Time.now()
        poly.header.frame_id = "map"
        
        tmp_points = Point32()
        tmp_points.x = self.start_pos.x
        tmp_points.y = self.start_pos.y

        poly.polygon.points.append(tmp_points)

        tmp_points = Point32()
        tmp_points.x = self.start_pos.x
        tmp_points.y = self.goal_pos.y

        poly.polygon.points.append(tmp_points)

        tmp_points = Point32()
        tmp_points.x = self.goal_pos.x
        tmp_points.y = self.goal_pos.y

        poly.polygon.points.append(tmp_points)

        self.poly_pub.publish(poly)

        tmp_mark = Marker()
        tmp_mark.header.stamp = rospy.Time.now()
        tmp_mark.header.frame_id = "map"
        tmp_mark.type = 9
        tmp_mark.action = 0
        tmp_mark.pose.position.x = (self.start_pos.x + self.goal_pos.x) / 2
        tmp_mark.pose.position.y = max([self.start_pos.y, self.goal_pos.y]) + 0.1
        tmp_mark.color.r = 1.0
        tmp_mark.color.g = 1.0
        tmp_mark.color.b = 1.0
        tmp_mark.color.a = 1.0
        tmp_mark.scale.z = 0.5
        tmp_mark.text = "{:.3f}".format(distance)

        self.text_pub.publish(tmp_mark)



def run():
    rospy.init_node("calc_dist_map")
    CalcDist()
    rospy.spin()

if __name__ == "__main__":
    run()
