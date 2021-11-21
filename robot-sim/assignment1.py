from __future__ import print_function
import time
from sr.robot import *
import pdb 


d_th2 = 1
d_th = 0.4
boolean_env = False
#boolean for checking if the Robot is searching or not a silver token
is_silver = 0

# instance of the class Robot
R = Robot()
# instance of the class Robot

def drive(speed):

    """
    Function for setting a linear velocity
    Args: speed (int): the speed of the wheels
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed

def stop():
    """
    Function for stopping the robot
    Args: speed (int): the speed of the wheels
    """
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn_and_stop(speed):
    """
    Function for turning the robot stopping its driving
    Args: speed (int): the speed of the wheels
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    



def turn(speed,direction):

  """
  Function for setting an angular velocity without stopping the robot
  Args: speed (int): the speed of the wheels
        direction (string): 'LEFT' or 'RIGHT'
  """
  if direction == 'RIGHT':
    # turn right
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed/6 # in this way the robot will not stop when turning

  elif direction == 'LEFT':
    # turn left
    R.motors[0].m0.power = speed/6
    R.motors[0].m1.power = speed

def turn180(speed):
  """
  Turn 180 degrees clockwise
  R.heading values:
    0deg = 0
    90deg = -1.5
    180deg = -3 = +3
    270deg = 1.5
  Args: speed (int): the speed of the wheels
  """
  max_error = 0.2
  start_heading = R.heading
  curr_heading = R.heading
  discrepancy = abs(start_heading) # |(start_heading + 3) - 3|
  goal_heading = -3 + discrepancy

  # correcting heading if value negative
  if start_heading < 0:
    goal_heading *= -1

  while abs(curr_heading - goal_heading) > max_error:
    curr_heading = R.heading
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(0.01)

  stop()

def find_token_right(max_deg):
    """
    Funstion for finding the closest token on robot's right hand side inside the view cone determined by max_deg
    """
    dist=10
    rot_y = 0 
    code = 0
    for token in R.see():
        	if token.dist < dist and 90- max_deg<= token.rot_y <= 90+ max_deg  and token.info.marker_type is MARKER_TOKEN_GOLD:
           		dist=token.dist
	    		rot_y=token.rot_y
	    		code = token.info.code

    
    if dist==10:
		return -1, -1 , -1
    else:
   		return dist, rot_y ,code

def find_token_left(max_deg):
	"""
	Function for finding the closest token on robot's left hand side  inside the view cone determined by max_deg 
	"""

	dist=100
	rot_y = 0
	code = 0
    	for token in R.see():
        	if token.dist < dist and -90-max_deg<= token.rot_y <= -90+max_deg and token.info.marker_type is MARKER_TOKEN_GOLD:
           		dist=token.dist
	    		rot_y=token.rot_y
	    		code = token.info.code

	
    	if dist==100:
		return -1, -1 , -1
    	else:
   		return dist, rot_y ,code

def find_token_front(max_deg):
   """
   Function for finding the closest token on robot's front side  inside the view cone determined by max_deg  
   If silver is true it means that a silver token has been detected and the robot have to stuck searching and grabbing it
   """
   dist_init = 10
   dist = dist_init
   codeF = 0
   is_silver = 0
   for token in R.see():
    if token.dist < dist and -max_deg < token.rot_y < max_deg:
        dist=token.dist
        rot_y=token.rot_y
        codeF = token.info.code
        if token.info.marker_type == MARKER_TOKEN_SILVER:
          is_silver = 1
   if dist == dist_init:
    return -1, -1
   else:
    return dist, rot_y, is_silver,codeF

def find_token_back():

	dist=100
    	for token in R.see():
        	if token.dist < dist and (100<= token.rot_y <= 180 or -180<= token.rot_y <= -100):
           		dist=token.dist
	    		rot_y=token.rot_y
	    		code = token.code
	    		info = token.info_type

    	if dist == 100:
		return -1, -1 , -1 , -1
    	else:
   		return dist, rot_y ,code, info

def environment_evaluation(minDist_F,codeF):
    """
    Function called when the front distance from a golden token is less than 1.4
    It differenciates if the robot has to perform a curve or avoid hitting the wall
    """

    global code_old_F 
    curve_speed = 100
    
    path_speed = 100
    lateral_deg = 10
    max_search_deg = 20
    
    global boolean_env
    global is_silver
    

    minDist_R,rot_y_RMin,codeR = find_token_right(lateral_deg)
    minDist_L,rot_y_LMin,codeL = find_token_left(lateral_deg)
    
    
    if minDist_R > minDist_L:
        if minDist_R > 1.5:  # if there is a right curve
            
        	if codeL != code_old_F:
                    print("I'm turning on my right")
                    minDist_L,rot_y_LMin,codeL = find_token_left(lateral_deg)
                    turn(curve_speed,"RIGHT")
                    turn(curve_speed,"RIGHT")
                    
                    
            
           	else:
           	    #correction due to the fact is is moving while turning
           	    for i in range(20):
           	    	turn_and_stop(curve_speed)
           	    
	    	    dist, rot_y, is_silver, codeF = find_token_front(max_search_deg)
	    	    if is_silver == 1:
	    			boolean_env = True # this is for not ricalculating front varibles when returning to the main loop
	    			return
	    	
	    	    else:
	    			alignment_with_path(minDist_R,rot_y_RMin,codeR,minDist_L,rot_y_LMin,codeL,path_speed,"LEFT")
                

        elif minDist_R < 1.5: # if the robot is to close to the left wall
            alignment_with_path(minDist_R,rot_y_RMin,codeR,minDist_L,rot_y_LMin,codeL,path_speed,"LEFT")
            


    elif minDist_R < minDist_L:
        if minDist_L > 1.5:
           
           	if codeR != code_old_F: # if there is a left curve
                	print("I'm turning on my left")
                	minDist_R,rot_y_RMin,codeR = find_token_right(lateral_deg)
                	
                	turn(curve_speed,"LEFT")
                	turn(curve_speed,"LEFT")
                	
            
            	else:
            		for i in range(20):
            			
            			turn_and_stop(-curve_speed)
            			
            		dist, rot_y, is_silver, codeF = find_token_front(max_search_deg)
	    		if is_silver == 1:
	    			
	    			boolean_env = True # this is for not ricalculating front varibles when returning to the main loop
	    			return	
	    		else:
	    			alignment_with_path(minDist_R,rot_y_RMin,codeR,minDist_L,rot_y_LMin,codeL,path_speed,"RIGHT")
                

        elif minDist_L < 1.5: # if the robot is to close to the right wall
               alignment_with_path(minDist_R,rot_y_RMin,codeR,minDist_L,rot_y_LMin,codeL,path_speed,"RIGHT")
               

def alignment_with_path(minDist_R,rot_y_RMin,codeR,minDist_L,rot_y_LMin,codeL,rot_speed, direction):

    min_deg = 0
    max_deg = 90
    lateral_deg = 30
    lin_vel = 100
    rot_vel = 100
    boolean_R = None
    boolean_L = None
    stopping = 0.5
    init_rot = 70
    max_search_deg = 35
    
    global boolean_env
    global is_silver


    minDist_R_new,rot_y_RMin_new,codeR_new = minDist_R,rot_y_RMin,codeR
    minDist_L_new,rot_y_LMin_new,codeL_new = minDist_L,rot_y_LMin,codeL
    
    if direction == "RIGHT":
    	minDist_R_new,rot_y_RMin_new,codeR_new = find_token_right(lateral_deg)
	#minDist_L_new,rot_y_LMin_new,codeL_new = find_token_left(lateral_deg)
    	
    	if minDist_R_new <= 0.8:
    	    	minDist_R_new,rot_y_RMin_new,codeR_new = find_token_right(lateral_deg)
    		if rot_y_RMin_new < 100:
    			for i in range(15):
    				turn(rot_vel,"LEFT")
    				#minDist_R_new,rot_y_RMin_new,codeR_new = find_token_right(lateral_deg)
    			
    		else:
    			drive(lin_vel)
    			#minDist_R_new,rot_y_RMin_new,codeR_new = find_token_right(lateral_deg)
    			
    	else:	
    	    	minDist_R_new,rot_y_RMin_new,codeR_new = find_token_right(lateral_deg)
    		if rot_y_RMin_new > 85 or rot_y_RMin_new < 95:
    			return
	    	elif rot_y_RMin_new > 95:
	    		for i in range(15):
	    			turn(rot_vel,"RIGHT")
	    			
	    	
    elif direction == "LEFT":
	#minDist_R_new,rot_y_RMin_new,codeR_new = find_token_right(lateral_deg)
	minDist_L_new,rot_y_LMin_new,codeL_new = find_token_left(lateral_deg)
    	
    	if minDist_L_new <= 0.9:
		minDist_L_new,rot_y_LMin_new,codeL_new = find_token_left(lateral_deg)
    		if rot_y_LMin_new > -100:
    			for i in range(15):
    				turn(rot_vel,"RIGHT")
    				
    	
    		else:
    			drive(lin_vel)
    			
    	else:	
		minDist_L_new,rot_y_LMin_new,codeL_new = find_token_left(lateral_deg)
    		if rot_y_LMin_new < -85 or rot_y_RMin_new > -95:
	    			return
	    		
	    	elif rot_y_LMin_new < -95:
	    		for i in range(10):
	    			turn(rot_vel,"LEFT")
	    			
    		
    		     

""" 
# my idea was to have two dirrent functions for alignment after a curve and for aligning because of a wall but performances are not suffunciently valid especially because of while cicles   	

def alignment_from_wall(minDist_R,rot_y_RMin,codeR,minDist_L,rot_y_LMin,codeL,rot_speed, direction):


    minDist_R_new,rot_y_RMin_new,codeR_new = minDist_R,rot_y_RMin,codeR
    minDist_L_new,rot_y_LMin_new,codeL_new = minDist_L,rot_y_LMin,codeL
    align_angle = 0
    driving_speed = 100
    lateral_deg = 30

    if direction == "RIGHT":
    		align_angle = 110
    		direction1 = "LEFT"
    		direction2 = "RIGHT"
    		
    		while rot_y_RMin_new < align_angle:
    			print("al wall right 1")
    	 		turn(driving_speed,direction1)
    	 		minDist_R_new,rot_y_RMin_new,codeR_new = find_token_right(lateral_deg)
    	 		
    	 	while minDist_R_new <=1:
    	 		print("al wall right 2")
    	 		drive(driving_speed)
			minDist_R_new,rot_y_RMin_new,codeR_new = find_token_right(lateral_deg)
		
		while rot_y_RMin_new > 90:
			print("al wall right 3")
			turn(driving_speed,direction2)
			minDist_R_new,rot_y_RMin_new,codeR_new = find_token_right(lateral_deg)
                
    	
	
    		
    		
    elif direction == "LEFT":
    		align_angle = -110
    		direction1 = "RIGHT"
    		direction2 = "LEFT"
            	while rot_y_LMin_new > align_angle:
            		print("al wall left 1")
    	 		turn(driving_speed,direction1)
    	 		minDist_L_new,rot_y_LMin_new,codeL_new = find_token_left(lateral_deg)
    	 		
    	 	while minDist_L_new <=1:
    	 		print("al wall left 2")
    	 		drive(driving_speed)
			minDist_L_new,rot_y_LMin_new,codeL_new = find_token_left(lateral_deg)
		
		while rot_y_LMin_new < -90:
			print("al wall left 3")
			turn(driving_speed,direction2)
			minDist_L_new,rot_y_LMin_new,codeL_new = find_token_left(lateral_deg)

"""


def alignment_to_silver(max_search_deg, max_rot_error_deg, rot_speed):
  """
  Function for aligning with a siliver token
  """
  global is_silver
  dist, rot_y, is_silver, codeF = find_token_front(max_search_deg)
  
  if rot_y > 0:
    # if token on right, turn right
    turn(rot_speed, 'RIGHT')
    print("Aligning to silver")
  else:
    # if token on left, turn left
    turn(rot_speed, 'LEFT')
    print("Aligning to silver")

def action_grab_silver(speed):
    """
    Function for grabbing a silver token if seen one,bringing it beside and turning again for going forward
    """

    while R.grab() == False: # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
            print("Gotcha!")
            drive(-20)
	    return -1
    turn180(speed)
    R.release()
    drive(-speed)
    time.sleep(0.5)
    turn180(-speed)
    time.sleep(0.5)

def main():
    
    
    max_search_deg = 20 # forward scanner cone angle
    max_deg = 10
    fwd_speed = 100
    rot_speed = 80
    max_rot_error_deg = 3 # acceptable error for silver token alignment
    max_obstacle_dist = 1.5 # max distance before obstacle avoidance kicks in
    global boolean_env
    global is_silver
    global code_old_F
    code_old_F = 0 # variable for performing a curve. When the Robot, on the left or right hand side, sees what it had in front of it, so the curve has been performed and it can continue

    # let the simulator load... (eliminates startup lag)
    print("Booting...")
    time.sleep(1)

    # main simulator loop
    while(1):
    	if boolean_env == False:
    		dist, rot_y, is_silver, codeF = find_token_front(max_search_deg)

	boolean_env = False
        if is_silver == 1:
            
            # if found silver token ahead
            if dist < d_th:
                # if token close, grab it
                action_grab_silver(rot_speed)
                stop()
            else:
                # otherwise, turn to face it and drive towards it
                if abs(rot_y) > max_rot_error_deg:
                    alignment_to_silver(max_search_deg, max_rot_error_deg, rot_speed/3)
                else:
                    drive(fwd_speed)
                    print("Driving to silver")

        else:
            # if found GOLD token ahead
            if dist > max_obstacle_dist:
                # drive until too close
                drive(fwd_speed)
                print("Driving...")

            else:
            	code_old_F = codeF
            	environment_evaluation(dist,codeF)
	     

        time.sleep(0.05)

main()

			            
