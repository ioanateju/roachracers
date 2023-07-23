import math

# Custom waypoints representing the racing line on the track
custom_waypoints = [
    
]

def get_distance_from_waypoint(x, y, waypoint):
    # Calculate Euclidean distance between the car and the waypoint
    dx = x - waypoint[0]
    dy = y - waypoint[1]
    return math.sqrt(dx**2 + dy**2)

def reward_function(params):
    # Define the maximum distance from the racing line to consider the car on track
    max_waypoint_distance = 0.5

    # Extract relevant information from the parameters
    x = params['x']
    y = params['y']
    speed = params["speed"]
    progress = params["progress"]
    all_wheels_on_track = params['all_wheels_on_track']

    # Initialize the reward
    reward = 1e-3

    # Check if all wheels are on the track
    if not all_wheels_on_track:
        reward -= 1.0
        return float(reward)

    # Reward for maintaining speed
    reward *= speed

        # Provide a bonus if the car completes a lap
    if progress == 100:
        reward += 10

    # Calculate the distance from the car to the nearest waypoint
    closest_distance = min([get_distance_from_waypoint(x, y, waypoint) for waypoint in custom_waypoints])

    # Calculate the reward based on the distance from the racing line
    if closest_distance < max_waypoint_distance:
        reward += 1.0 - closest_distance / max_waypoint_distance

    return float(reward)
