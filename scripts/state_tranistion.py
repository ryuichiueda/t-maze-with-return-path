#!/usr/bin/env python
import sys
import rospy
#from raspimouse_ros.srv import PutMotorFreqs
#from raspimouse_ros.srv import SwitchMotors
from t_maze_return_path.srv import ExecAction
from std_msgs.msg import String

def callback_action(message):
#    try: 
#        with open(enfile,'w') as f:
#            if message.on: print >> f, '1'
#            else:          print >> f, '0'
#    except:
#        rospy.logerr("cannot write to " + enfile)
#        return False
#
    d = ExecAction()
    d.reward = 0.0
    d.sensors = "aaa"
    return d

def listner():
    rospy.init_node('t_maze_with_return_path')
    srv = rospy.Service('action', ExecAction, callback_action)
    #sub = rospy.Subscriber('motor_raw', LeftRightFreq, callback_motor_raw)
    #srv = rospy.Service('switch_motors', SwitchMotors, callback_motor_sw)
    rospy.spin()


if __name__ == '__main__':
    try:
        listner()

    except rospy.ROSInterruptException:
        pass

#
#def callback_motor_raw(message):
#    lfile = '/dev/rtmotor_raw_l0'
#    rfile = '/dev/rtmotor_raw_r0'
#
#    print message
#    try:
#        lf = open(lfile,'w')
#        rf = open(rfile,'w')
#        print >> lf, str(message.left)
#        print >> rf, str(message.right)
#    except:
#        rospy.logerr("cannot write to rtmotor_raw_*")
#
#    lf.close()
#    rf.close()
#
#def callback_put_freqs(message):
#    devfile = '/dev/rtmotor0'
#
#    try:
#        with open(devfile,'w') as f:
#            print >> f, "%s %s %s" % (message.left, message.right, message.duration)
#    except:
#        rospy.logerr("cannot write to " + devfile)
#        return False
#
#    return True
#        
