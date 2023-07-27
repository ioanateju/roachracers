import matplotlib.pyplot as plt
import numpy as np

"""
RUN THIS FILE BY DOING

python3 custom_track_build.py
"""

def take_plot(plots, axis = "x"):
    """
    return back a single array of all X points, or all Y points
    """
    axis_line = []
    for item in plots:
        value = item[0] if axis == "x" else item[1]
        axis_line.append(value)

    return axis_line


def pick_plot(waypoint_id: int, plots):
    """
    Picks the "perfect" line points and returns back the current X, Y of the plot chosen
    """
    middle_x = plots[0]
    middle_y = plots[1]

    inner_x = plots[2]
    inner_y = plots[3]

    outer_x = plots[4]
    outer_y = plots[5]

    if waypoint_id % 5 == 0:
        return [middle_x, middle_y]
    return [inner_x, inner_y]


def print_plot_locations(item):
    """
    Print All Locations for Plots
    """
    middle_x = item[0]
    middle_y = item[1]

    inner_x = item[2]
    inner_y = item[3]

    outer_x = item[4]
    outer_y = item[5]

    print(f"Track Way Points | OUTER: x{outer_x}, y{outer_y} | MIDDLE x{middle_x}, y{middle_y} | INNER x{inner_x}, y{inner_y}")

def create_track_waypoints():
    # Track Name
    track_name = "2022_april_open_ccw"
    absolute_path = "."

    waypoints = np.load("%s/%s.npy" % (absolute_path, track_name))

    # Total Track Waypoints
    print("Number of waypoints = " + str(waypoints.shape[0]))

    return waypoints


# "Perfect" line is the [[X, Y], ...] co-ordernates of the best line chosen from pick_plot
perfect_line = []

# For each waypoint_id (waypoint on track) and item (collection of waypoints)
for waypoint_id, item in enumerate(create_track_waypoints()):
    # Creates Logs for Waypoint Locations
    print_plot_locations(item)

    # Plots the "Perfect" line
    perfect_line.append(pick_plot(waypoint_id, item))


for i, point in enumerate(create_track_waypoints()):
    # PLOTS FOR OUTER/MID/INNER Track Limits
    waypoint_middle = (point[0], point[1])
    waypoint_inner = (point[2], point[3])
    waypoint_outer = (point[4], point[5])

    # ACTUALLY SCATTER HERE
    plt.scatter(waypoint_outer[0], waypoint_outer[1], c="blue", s=4, zorder=1)
    plt.scatter(waypoint_middle[0], waypoint_middle[1], c="blue", s=4, zorder=1)
    plt.scatter(waypoint_inner[0], waypoint_inner[1], c="blue", s=4, zorder=1)

# ACTUALLY PLOTS THE LINE HERE (overrides the scatter plotting with line)
plt.plot(take_plot(perfect_line, "x"), take_plot(perfect_line, "y"), '.r-', zorder=2)

# SHOWS the plt graph
plt.show()
