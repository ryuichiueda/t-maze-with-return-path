#!/usr/bin/env python
import sys
import rospy
import time
import random
from t_maze_return_path.srv import ExecAction,ExecActionResponse
from std_msgs.msg import String

def act():
    rospy.wait_for_service('/t_maze_return_path/action')
    try:
        exec_action = rospy.ServiceProxy('/t_maze_return_path/action',ExecAction)

        action = "fw"
        r = random.randint(0,2)
        if r == 1:
            action = "cw"
        elif r == 2:
            action = "ccw"

        res = exec_action(action)

        print action, res.result, res.sensor, res.reward
    except rospy.ServiceException, e:
        print "EXECPTION"

    time.sleep(0.3)

if __name__ == '__main__':
    rospy.init_node('behavior_random')
    while True:
        act()
