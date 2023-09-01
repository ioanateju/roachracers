import math


def reward_function(params):

    # waypoint coords
    # closest way point
    # coord of self - makes angle more accurate
    # direction of travel - check if array of waypoints change based on direction
    # how many waypoints ahead do we want to check - trial / error
    # get coords of waypoint x ahead
    # calc angle between closest waypoint and waypoint x ahead
    # reward based on how close turnng angle is to calc angle

    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering = abs(params['steering_angle'])
    direction_stearing=params['steering_angle']
    speed = params['speed']
    steps = params['steps']
    is_offtrack=params['is_offtrack']
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    x = params['x']
    y = params['y']

    SPEED_THRESHOLD_2=1.8
    DIRECTION_THRESHOLD = 3.0
    SPEED_THRESHOLD_1=3.5
    # Read input variables

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    benchmark_time=14.2
    benchmark_steps=173
    straight_waypoints=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,138,139,140,141,142,143,144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,160,161,162,163,164,165,166,167,168,169,170]

    reward = 1.0
    # Get reward if completes the lap and more reward if it is faster than benchmark_time    
    if progress == 100:
        if round(steps/15,1)<benchmark_time:
            reward+=100*round(steps/15,1)/benchmark_time
        else:
            reward += 100
    elif is_offtrack:
        reward-=50   
    
    # Calculate the direction of the center line based on the closest waypoints

    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians

    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 

    # Convert to degree

    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car

    direction_diff = abs(track_direction - heading)

    # Penalize the reward if the difference is too large
   
    direction_bonus=1
  
    if direction_diff > DIRECTION_THRESHOLD or not all_wheels_on_track:

        direction_bonus=1-(direction_diff/15)
        if direction_bonus<0 or direction_bonus>1:
            direction_bonus = 0
        reward *= direction_bonus
    else:
        if next_point in (straight_waypoints):
            if speed>=SPEED_THRESHOLD_1:
                reward+=max(speed,SPEED_THRESHOLD_1)
            else:
                reward+=1e-3
        else:
            if speed<=SPEED_THRESHOLD_2:
                reward+=max(speed,SPEED_THRESHOLD_2)
            else:
                reward+=1e-3
    
    # Give additional reward if the car pass every 50 steps faster than expected
    if (steps % 50) == 0 and progress >= (steps / benchmark_steps) * 100 :
        reward += 10.0
    # Penalize if the car cannot finish the track in less than benchmark_steps
    elif (steps % 50) == 0 and progress < (steps / benchmark_steps) * 100 :
        reward-=5.0
    return reward

