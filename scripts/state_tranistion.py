#!/usr/bin/env python
import sys
import rospy
from t_maze_return_path.srv import ExecAction,ExecActionResponse
from std_msgs.msg import String

class Env:
    def __init__(self):
        str1 = "     "
        str2 = " x x "
        str3 = "     "
        self.cell = [str1,str2,str3]
        self.x = 2
        self.y = 2
        self.d = "^"

    def p(self):
        ans = "-------"
        for i,line in enumerate(self.cell):
            if self.y == i:
                line = line[0:self.x] + self.d + line[self.x+1:]
            line = "|" + line + "|"

            ans = ans + "\n" + line

        return ans + "\n-------"

    def in_the_env(self,x,y):
        if y < 0 or y >= len(self.cell): return False
        if x < 0 or x >= len(self.cell[y]): return False
        if (x,y) == (1,1) or (x,y) == (3,1): return False

        return True

    def move(self,action):
        if action == "fw":
            x,y = self.x, self.y
            if self.d == "^": y = y - 1
            elif self.d == "v": y = y + 1
            elif self.d == ">": x = x + 1
            elif self.d == "<": x = x - 1
            if self.in_the_env(x,y):
                self.x, self.y = x,y
                return "OK"

            return "HIT"

        if action == "cw":
            if self.d == "^": self.d = ">"
            elif self.d == "<": self.d = "^"
            elif self.d == "v": self.d = "<"
            elif self.d == ">": self.d = "v"
            return "OK"

        if action == "ccw":
            if self.d == "^": self.d = "<"
            elif self.d == "<": self.d = "v"
            elif self.d == "v": self.d = ">"
            elif self.d == ">": self.d = "^"
            return "OK"

        return "INVALID_ACTION"

    def is_visible_forward(self):
        x,y = self.x, self.y
        if self.d == "^": y = y - 1
        if self.d == "v": y = y + 1
        if self.d == ">": x = x + 1
        if self.d == "<": x = x - 1

        return self.in_the_env(x,y)

env = Env()

def callback_action(message):
    a = message.action
    d = ExecActionResponse()
    d.reward = 0.0
    d.result = env.move(a)
    d.sensor = "NO_WALL" if env.is_visible_forward() else "WALL"
    rospy.loginfo("\n" + env.p())
    return d

def listner():
    rospy.init_node('t_maze_with_return_path')
    srv = rospy.Service('action', ExecAction, callback_action)
    rospy.spin()


if __name__ == '__main__':
    try:
        listner()

    except rospy.ROSInterruptException:
        pass
