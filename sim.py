#!/usr/bin/env python3 

""" Table of Contents (* to jump)
    CONSTANTS
    INIT-GENERATION
    DRAWING-POINTS-AND-VECTORS
    ANIMATION-AND-DISPLAY
"""
from time import sleep
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import juggle_axes
import numpy as np


def gen_points():
    global points 
    points['mass'] = np.random.choice(masses, size=points_amt)

    points['coords'][:,0] = ((ranx[1] - ranx[0]) * 
                                np.random.random(points_amt) + ranx[0])
    points['coords'][:,1] = ((rany[1] - rany[0]) * 
                                np.random.random(points_amt) + rany[0])

    angles = np.random.uniform(0, 2 * np.pi, points_amt)
    lengths = np.random.uniform(*speed_range, points_amt)
    points['speed'][:,0] = np.cos(angles) * lengths
    points['speed'][:,1] = np.sin(angles) * lengths

# Returns distance between two planets.
def get_dist(p1, p2):
    return sum((points['coords'][p1] - points['coords'][p2]) ** 2) ** 0.5

# Returns length of a vector between p1 and p2.
def get_length(p1, p2):
    return (p1 ** 2 + p2 ** 2) ** 0.5

# Animation function.
def update_points(frame):
    global points
    global tracks

    # Uncomment for screen recording.
    # if frame == 1: sleep(7)

    # Moving the point according to its speed.
    points['coords'] += points['speed']

    # Calculating gravity forces for each planet.
    # Result - array of vector<float, float> for each point.
    forces = np.zeros(points_amt, dtype="2float32")
    for p1 in range(points_amt):
        p1_force = np.array([0.0, 0.0])
        for p2 in range(points_amt):
            if p1 == p2: continue
            dist = get_dist(p1, p2)

            force_val = (points['mass'][p1] * points['mass'][p2]) / (dist ** 2)
            force_vec = (points['coords'][p2] - points['coords'][p1])
            p1_force += force_vec / dist * force_val

        # Attracting planets to big central gravity source.
        p1_force += (np.array([0.0, 0.0]) - points['coords'][p1]) * 1

        # Calculating the total force vector and doing some magic.
        p1_force = p1_force / points['mass'][p1] / 3
        if get_length(*points['speed'][p1]) >= get_length(*p1_force):
            forces[p1] = p1_force
        else:
            forces[p1] = (p1_force / get_length(*p1_force) * 
                                     get_length(*points['speed'][p1]))
        points['speed'][p1] += p1_force / 20

    # Draw speed and force vector.
    if draw_vecs:
        speed_quiv.set_offsets(points['coords'].reshape(points_amt, 2))
        speed_quiv.set_UVC(points['speed'][:,0], points['speed'][:,1])
        # speed_quiv.set_sizes(list(map(lambda x: get_length(*x),
                                      # points['speed'])))
        force_quiv.set_offsets(points['coords'].reshape(points_amt, 2))
        force_quiv.set_UVC(forces[:,0], forces[:,1])
        # force_quiv.set_sizes(list(map(lambda x: get_length(*x), forces)))
    # Draw tracks after planets.
    if draw_tracks:
        for i in range(points_amt):
            tracks[i].popleft()
            tracks[i].append(np.copy(points['coords'][i]))
            lines[i].set_data([tracks[i][j][0] for j in range(track_len)],
                              [tracks[i][j][1] for j in range(track_len)])
    # Draw planets.
    scat.set_offsets(points['coords'].reshape(points_amt, 2))


#-CONSTANTS-------------------------------------------------------------------#
# seed: 7, points: 4    - great planet gravity example 
# seed: 4, points: 3    - atom 

np.random.seed(7)
masses = [5, 5, 5, 5, 5, 5, 20, 20, 20, 200]
sizes_dict = {5: 5, 20: 20, 200: 50}
points_amt = 4
speed_range = (0.8, 1)
plim = (-100, 100)
ranx = (-50, 50)
rany = (-50, 50)
draw_vecs = False
draw_tracks = True
track_len = 100
#-END-CONSTANTS---------------------------------------------------------------#


#-INIT-GENERATION-------------------------------------------------------------#
points = np.zeros(points_amt, dtype=[("coords",    "2float64"), 
                                     ("speed",     "2float64"),
                                     ("mass",      "int32")])
gen_points()
sizes = np.zeros(points_amt)
for p in range(points_amt):
    sizes[p] = sizes_dict[points['mass'][p]]

fig = plt.figure()
ax = plt.gca()
ax.set_xlim(plim)
ax.set_ylim(plim)
ax.set_xlabel('X')
ax.set_ylabel('Y')
#-END-INIT-GENERATION---------------------------------------------------------#


#-DRAWING-POINTS-AND-VECTORS--------------------------------------------------#
scat = ax.scatter(points['coords'][:,0],
        points['coords'][:,1],
        s=sizes,
        c='k', marker='o')
ax.scatter([0], [0], s=200, c='r', marker='o')
if draw_vecs:
    speed_quiv = ax.quiver(
        points['coords'][:,0],
        points['coords'][:,1],
        points['speed'][:,0],
        points['speed'][:,1],
        width=2, headwidth=3,
        color='b', units='dots', scale_units='dots')
    force_quiv = ax.quiver(
        points['coords'][:,0],
        points['coords'][:,1],
        *np.ones((2, points_amt)),
        width=2, headwidth=3,
        color='r', units='dots', scale_units='dots')
if draw_tracks:
    tracks = [deque() for i in range(points_amt)]
    lines = []
    for i in range(points_amt):
        for j in range(track_len):
            tracks[i].append(np.copy(points['coords'][i]))
        
        l = ax.plot([tracks[i][j][0] for j in range(track_len)],
                    [tracks[i][j][1] for j in range(track_len)])
        lines.append(l[0])
#-END-DRAWING-POINTS-AND-VECTORS----------------------------------------------#


#-ANIMATION-AND-DISPLAY-------------------------------------------------------#
ani = animation.FuncAnimation(fig, update_points, interval=1, blit=False)
plt.show()
#-END-ANIMATION-AND-DISPLAY---------------------------------------------------#

