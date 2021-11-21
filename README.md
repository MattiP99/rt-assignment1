Research Track 1, Assignment 1
Student: Mattia Piras




INTRODUCTION:
___________________________________________________________________________________________________________________________________________________________
This is the first assignment of the "Research Track 1" course, in the Robotics Engineering degree, Università di Genova. In the simulator there is a robot in an "arena" of golden and silver tokens. The robot must keep driving in a counter-clockwise direction whilst avoiding the golden tokens which constitute a "wall". When the robot encounters the silver token, it must grab it, turn around 180 degrees, release it, turn back and continue on its path.




RUNNING THE PROGRAM
___________________________________________________________________________________________________________________________________________________________
The simulator requires a Python 2.7 installation, the pygame library, PyPyBox2D, and PyYAML.
Simply launch the file "start"




DESCRIPTION
___________________________________________________________________________________________________________________________________________________________
It was fun coming up with the solution for this project.
First of all, I had to cope with the fact that the Robot should driving in counter clockwise and that its vision is 360° degrees. This last issue has been resolved by limiting the entire view in sectors to better dealing with right, left, back and front side. In order to decide the best direction to drive to, I considered that every token has a code.
When the distance from a front token decreases under a fixed value (I wanted to consider a dynamic value comparing the lateral distance from a golden token with the front one and checking if this last was less than the first one, but I had some issues) the Robot has to take a decision (see evaluation_environment function):

- if front_distance < frontValue:
  - CURVE:
      One of the two lateral distances of a gold token is greater than 1.5
      The Robot should turn until the token code that it saw with the front "scanner" has to reappears within one lateral scanner
      Than It should align itself with the path

  - A WALL:
      If both lateral distances are less than a certain value than It is going to hitting a wall.
      So it has to align itself with the path

Silver tokens are the first priority for the Robot: If in front of it there's one it should align with, drive to and grab it, bringing it back from the current heading (see action_grab_silver and turn180 functions are aimed for this).

The robot moves back slightly, after releasing the silver token, before turning back. This avoids hitting the token when rotating after the release.




FUTURE DEVELOPMENTS
___________________________________________________________________________________________________________________________________________________________
What I could have added was a pile for managing silver tokens: if the Robot inverted its driving direction, it could know it had just grabbed a silver token if this was on top of the pile (Or It should be possible to save the time in which a silver token has been grabbed and if it was not passed a sufficiently long amount of time after this, that particular token can't be considered and a driving inversion should be performed ).

I would have done a better alignment in order to maintain the Robot as close as possible to the center of the path, but while loops(while some angles alignment were reached) were badly managed and the Robot flow was not so linear.

I'd like to improve performances and the way each loop is performed after having considered the last one. My solution failed very few times, when some particular positions are reached and I know that it can be improved.




PSEUDOCODE
___________________________________________________________________________________________________________________________________________________________

WHILE simulation is going:\
- IF silver token has been detected:\
  - IF silver_distance < value:\
     - action_grab_silver()\
  - ELSE:\
     - IF |angle_front| > value:\
       - alignment_with_silver()\
     - ELSE:\
       - drive()\
  - ELIF golden token has been detected:\
    - IF gold_distance > value:\
      - drive()\
    - ELSE:\
      - evaluation_environment()\


