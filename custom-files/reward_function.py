import math


def reward_function(params):
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    progress = params['progress']
    steps = params['steps']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']

    # Set constant parameters
    MAX_STEPS = 50

    # Reward weights
    center_weight = 0.6
    speed_weight = 0.4

    # Reward for staying close to the centerline
    reward = 1 - (distance_from_center / (track_width/2 + 0.01))
    reward = max(reward, 1e-3) * center_weight

    # Reward for maintaining speed
    reward *= speed * speed_weight

    # Penalize if the car goes off track
    if not all_wheels_on_track:
        reward = 1e-5

    # Provide a bonus if the car completes a lap
    if progress == 100:
        reward += 10

    # Penalize if the car takes too many steps (to encourage efficiency)
    if steps >= MAX_STEPS:
        reward = 1e-3

    # Additional reward for following waypoints
    if closest_waypoints[1] < len(waypoints):
        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]
        track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0])
        car_direction = params['heading']
        direction_diff = abs(car_direction - track_direction)
        if direction_diff > math.pi:
            direction_diff = 2 * math.pi - direction_diff
        direction_reward = 1 - direction_diff / math.pi
        reward += 0.3 * direction_reward

    return float(reward)
