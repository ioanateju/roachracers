import math

# class PARAMS:
#     prev_speed = None
#     prev_steering_angle = None 
#     prev_steps = None
#     prev_direction_diff = None
#     prev_normalized_distance_from_route = None

# def reward_function(params):
    
#     # Read input parameters
#     heading = params['heading']
#     steps = params['steps']
#     waypoints = params['waypoints']
#     closest_waypoints = params['closest_waypoints']
#     steering_angle = params['steering_angle']
#     speed = params['speed']

#     # Waypoint simple closest waypoint direct setup
#     next_point = waypoints[closest_waypoints[1]]
#     prev_point = waypoints[closest_waypoints[0]]
#     track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
#     car_direction = params['heading']
#     direction_diff = abs(car_direction - track_direction)

#     # Reinitialize previous parameters if it is a new episode
#     if PARAMS.prev_steps is None or steps < PARAMS.prev_steps:
#         PARAMS.prev_speed = None
#         PARAMS.prev_steering_angle = None
#         PARAMS.prev_direction_diff = None
#         PARAMS.prev_normalized_distance_from_route = None

#     #Check if the speed has dropped
#     has_speed_dropped = False
#     if PARAMS.prev_speed is not None:
#         if PARAMS.prev_speed > speed:
#             has_speed_dropped = True

#     #Penalize slowing down without good reason on straight portions
#     if has_speed_dropped and direction_diff: 
#         speed_maintain_bonus = min( speed / PARAMS.prev_speed, 1 )
#     #Penalize making the heading direction worse
#     heading_decrease_bonus = 0

#     if PARAMS.prev_direction_diff is not None:
#         if abs( PARAMS.prev_direction_diff / direction_diff ) > 1:
#             heading_decrease_bonus = min(10, abs( PARAMS.prev_direction_diff / direction_diff ))

#     #has the steering angle changed
#     has_steering_angle_changed = False
#     if PARAMS.prev_steering_angle is not None:
#         if not(math.isclose(PARAMS.prev_steering_angle, steering_angle)):
#             has_steering_angle_changed = True
#     steering_angle_maintain_bonus = 1

#     #Not changing the steering angle is a good thing if heading in the right direction
#     if not has_steering_angle_changed:
#         if abs(direction_diff) < 10:
#             steering_angle_maintain_bonus *= 2
#         if abs(direction_diff) < 5:
#             steering_angle_maintain_bonus *= 2
#         if PARAMS.prev_direction_diff is not None and abs(PARAMS.prev_direction_diff) > abs(direction_diff):
#             steering_angle_maintain_bonus *= 2

#     # Before returning reward, update the variables
#     PARAMS.prev_speed = speed
#     PARAMS.prev_steering_angle = steering_angle
#     PARAMS.prev_direction_diff = direction_diff
#     PARAMS.prev_steps = steps
    
#     reward = float(speed_maintain_bonus + heading_decrease_bonus + steering_angle_maintain_bonus)

#     return float(speed_maintain_bonus)

def reward_function(params):

    # Reward weights
    speed_weight = 100
    heading_weight = 100
    steering_weight = 50

    # Initialize the reward based on current speed
    max_speed_reward = 10 * 10
    min_speed_reward = 2.33 * 2.33
    abs_speed_reward = params['speed'] * params['speed']
    speed_reward = (abs_speed_reward - min_speed_reward) / (max_speed_reward - min_speed_reward) * speed_weight
    
    # - - - - - 
    
    # Penalize if the car goes off track
    if not params['all_wheels_on_track']:
        return 1e-3
    
    # - - - - - 

    # Penalize for going slow
    if not params['speed'] < 3:
        return 1e-3

    # - - - - -
    
    # Calculate the direction of the center line based on the closest waypoints
    next_point = params['waypoints'][params['closest_waypoints'][1]]
    prev_point = params['waypoints'][params['closest_waypoints'][0]]

    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    # Convert to degree
    track_direction = math.degrees(track_direction)

    # Calculate the difference between the track direction and the heading direction of the car
    direction_diff = abs(track_direction - params['heading'])
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
    
    abs_heading_reward = 1 - (direction_diff / 180.0)
    heading_reward = abs_heading_reward * heading_weight
    
    # - - - - -
    
    # Reward if steering angle is aligned with direction difference
    abs_steering_reward = 1 - (abs(params['steering_angle'] - direction_diff) / 180.0)
    steering_reward = abs_steering_reward * steering_weight

    # - - - - -

    # Reward if the car completes a lap
    if params['progress'] == 100:
        progress_reward = 10

    # - - - - -
    
    return speed_reward + heading_reward + steering_reward + progress_reward


# PREVIOUS 1.2.x MODEL REWARD FUNCTION
# def reward_function(params):
#     # Read input parameters
#     track_width = params['track_width']
#     distance_from_center = params['distance_from_center']
#     all_wheels_on_track = params['all_wheels_on_track']
#     speed = params['speed']
#     progress = params['progress']
#     steps = params['steps']
#     waypoints = params['waypoints']
#     closest_waypoints = params['closest_waypoints']

#     # Set constant parameters
#     MAX_STEPS = 80

#     # Reward weights
#     center_weight = 0.65

#     # Reward for staying close to the centerline
#     reward = 1 - (distance_from_center / (track_width/2 + 0.01))
#     reward = max(reward, 1e-3) * center_weight

#     # Reward for maintaining speed
#     reward *= speed

#     # Penalize if the car goes off track
#     if not all_wheels_on_track:
#         reward = 1e-5

#     # Provide a bonus if the car completes a lap
#     if progress == 100:
#         reward += 10

#     # Penalize if the car takes too many steps (to encourage efficiency)
#     if steps >= MAX_STEPS:
#         reward = 1e-3

#     # Additional reward for following waypoints
#     if closest_waypoints[1] < len(waypoints):
#         next_point = waypoints[closest_waypoints[1]]
#         prev_point = waypoints[closest_waypoints[0]]
#         track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
#         car_direction = params['heading']
#         direction_diff = abs(car_direction - track_direction)
#         if direction_diff > math.pi:
#             direction_diff = 2 * math.pi - direction_diff
#         direction_reward = 1 - direction_diff / math.pi
#         reward += 0.9 * direction_reward

#     return float(reward)
