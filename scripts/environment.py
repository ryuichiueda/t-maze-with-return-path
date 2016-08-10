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
        self.prev_x = None
        self.prev_y = None
        self.d = "^"
        self.food_x = None
        self.food_y = None

        self.trial = 0

    def p(self):
        ans = "-------"
        for i,line in enumerate(self.cell):
            if self.y == i:
                line = line[0:self.x] + self.d + line[self.x+1:]
            if self.food_y == i and self.food_x != None:
                line = line[0:self.food_x] + '@'+ line[self.food_x+1:]
            line = "|" + line + "|"

            ans = ans + "\n" + line

        return ans + "\n-------"

    def in_the_env(self,x,y):
        if y < 0 or y >= len(self.cell): return False
        if x < 0 or x >= len(self.cell[y]): return False
        if (x,y) == (1,1) or (x,y) == (3,1): return False

        return True

    def move(self,action):
        self.prev_x,self.prev_y = self.x,self.y
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

    def food_rule(self):
        if (self.x,self.y) == (self.food_x,self.food_y):# agent gets the food
            self.food_x = None
            self.food_y = None
            return 99.0

        if self.x == 2 and self.y == 2: # at the start pos
            if self.food_x != None:
                return -1.0

            self.food_y = 0
            if self.trial%2 == 0:
                self.food_x = 3
            else:
                self.food_x = 1

            self.trial = self.trial + 1
            return -1.0

        return -1.0

env = Env()

def callback_action(message):
    a = message.action
    d = ExecActionResponse()
    d.result = env.move(a)
    d.sensor = "NO_WALL" if env.is_visible_forward() else "WALL"

    d.reward = env.food_rule()

    rospy.loginfo("\n" + env.p())
    return d

def listner():
    env.food_x = 1
    env.food_y = 0
    rospy.init_node('environment')
    srv = rospy.Service('action', ExecAction, callback_action)
    rospy.spin()


if __name__ == '__main__':
    try:
        listner()

    except rospy.ROSInterruptException:
        pass
