import math


def group_waypoints_in_straight_lines(waypoints, angle_threshold_degrees=10.0):
    straight_line_groups = []
    current_group = [waypoints[0]]
    for i in range(1, len(waypoints) - 1):
        prev_point = waypoints[i - 1]
        current_point = waypoints[i]
        next_point = waypoints[i + 1]
        # Calculate the angles between the points
        angle1 = math.atan2(current_point[1] - prev_point[1], current_point[0] - prev_point[0])
        angle2 = math.atan2(next_point[1] - current_point[1], next_point[0] - current_point[0])
        # Convert angles to degrees
        angle1_degrees = math.degrees(angle1)
        angle2_degrees = math.degrees(angle2)
        # Check if the difference between angles is below the threshold
        angle_difference = abs(angle2_degrees - angle1_degrees)
        if angle_difference <= angle_threshold_degrees:
            current_group.append(current_point)
        else:
            straight_line_groups.append(current_group)
            current_group = [current_point]
    # Add the last group
    straight_line_groups.append(current_group)
    return straight_line_groups


def calculate_next_turn_angle(waypoints, closest_waypoints, num_waypoints_ahead=5):
    # Get the index of the closest waypoint
    closest_index = closest_waypoints[1]
    # Extract the closest waypoint
    closest_waypoint = waypoints[closest_index]
    # Calculate the angle to the next waypoint 'num_waypoints_ahead' steps ahead
    target_index = (closest_index + num_waypoints_ahead) % len(waypoints)
    target_waypoint = waypoints[target_index]
    # Calculate the angle between the car's current direction and the direction to the target waypoint
    angle_to_target_waypoint = math.atan2(target_waypoint[1] - closest_waypoint[1], target_waypoint[0] - closest_waypoint[0])
    # Convert the angle from radians to degrees
    angle_degrees = math.degrees(angle_to_target_waypoint)
    return angle_degrees


def reward_function(params):

    # waypoint coords
    # closest way point
    # coord of self - makes angle more accurate
    # direction of travel - check if array of waypoints change based on direction
    # how many waypoints ahead do we want to check - trial / error
    # get coords of waypoint x ahead
    # calc angle between closest waypoint and waypoint x ahead
    # reward based on how close turnng angle is to calc angle

    speed = params['speed']
    steps = params['steps']
    is_offtrack=params['is_offtrack']
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']

    SPEED_THRESHOLD_2=1.8
    DIRECTION_THRESHOLD = 3.0
    SPEED_THRESHOLD_1=3.5
    ANGLE_THRESHOLD = 10.0
    # Read input variables

    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
    benchmark_time=14.2
    benchmark_steps=173

    straight_line_waipoints_groups = group_waypoints_in_straight_lines(waypoints, ANGLE_THRESHOLD)
    turn_angle_weight = 1.5

    reward = 1e-3

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
            direction_bonus = 1e-1
        reward *= direction_bonus
    else:
        if next_point in straight_line_waipoints_groups:
            if speed>=SPEED_THRESHOLD_1:
                reward+=max(speed,SPEED_THRESHOLD_1)
            else:
                reward+=1e-1
        else:
            if speed<=SPEED_THRESHOLD_2:
                reward+=max(speed,SPEED_THRESHOLD_2)
            else:
                reward+=1e-1
    
    # Get the waypoints and closest waypoints from params
    # Calculate the angle of the next turn using the function, considering 10 waypoints ahead
    # reward for turning at the right angle for the upcoming turn
    next_turn_angle = calculate_next_turn_angle(waypoints, closest_waypoints, num_waypoints_ahead=5)

    if abs(next_turn_angle - heading) > DIRECTION_THRESHOLD or not all_wheels_on_track:
        direction_bonus=1-(direction_diff/15)
        if direction_bonus<0 or direction_bonus>1:
            direction_bonus = 1e-3
        reward *= direction_bonus
    else:
        reward *= turn_angle_weight
    
    # Give additional reward if the car pass every 50 steps faster than expected
    if (steps % 50) == 0 and progress >= (steps / benchmark_steps) * 100 :
        reward += 10.0
    # Penalize if the car cannot finish the track in less than benchmark_steps
    elif (steps % 50) == 0 and progress < (steps / benchmark_steps) * 100 :
        reward-=5.0
    return reward

