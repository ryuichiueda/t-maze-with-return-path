# t_maze_return_path

A state transition simulator of a mouse in T-maze with pathway (8-maze) 

## Service

* action: to give an action to the agent, it returns a measured reward obtained by the action

# environment

    -------
    | @   |   @: food
    | x x |   x: occupied cell
    |<    |   <: agent
    -------

# actions

Receive via service "action"

* fw
* cw
* ccw

# rewards

* when the agent did an action: -1
* when the agent obtained a food: 100

# food placement rule

A food is placed one of the left arm or the right arm alternately
when the agent reaches to the bottom center cell.
