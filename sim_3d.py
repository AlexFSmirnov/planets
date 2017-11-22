from time import sleep
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
    points['coords'][:,2] = ((ranz[1] - ranz[0]) * 
                                np.random.random(points_amt) + ranz[0])
    # points['coords'][:,2] = np.zeros(points_amt)

    points['speed'] = ((speed_range[1] - speed_range[0]) * 
                                np.random.rand(points_amt, 3) + speed_range[0])

def get_dist(p1, p2):
    return sum((points['coords'][p1] - points['coords'][p2]) ** 2) ** 0.5

def update_points(frame, anim=True):
    global points
    # if frame == 1: sleep(7)
    # Calculating the gravity force for each point
    for p1 in range(points_amt):
        p1_force = np.array([0, 0, 0], dtype="float32")
        for p2 in range(points_amt):
            dist = get_dist(p1, p2)
            if dist <= 0.1: 
                continue 

            force_val = (points['mass'][p1] * points['mass'][p2]) / (dist ** 2)
            force_vec = (points['coords'][p2] - points['coords'][p1])
            p1_force += force_vec / dist * force_val

        # Adding big gravity source to the center of the plane
        # p1_force += (np.array([(plim[1] - plim[0]) / 2 for i in range(3)]) - 
                          # points['coords'][p1]) * 10
        points['speed'][p1] += (p1_force / points['mass'][p1]) / 100
        # points['speed'][p1][2] = 0
        points['coords'][p1] += points['speed'][p1] / 10

    if anim:
        scat._offsets3d = juggle_axes(points['coords'][:,0],
                                      points['coords'][:,1],
                                      points['coords'][:,2], 'z')


masses = [5, 5, 5, 5, 5, 5, 200, 200, 200, 5000]
sizes_dict = {5: 5, 200: 20, 5000: 50}
points_amt = 50
speed_range = (-1, 1)
plim = (0, 100)
ranx = (0, 100)
rany = (0, 100)
ranz = (0, 100)


points = np.zeros(points_amt, dtype=[("coords",    "3float32"), 
                                     ("speed", "3float32"),
                                     ("mass",      "int32")])
gen_points()
sizes = np.zeros(points_amt)
for p in range(points_amt):
    sizes[p] = sizes_dict[points['mass'][p]]

# points['coords'] = np.array([[0, 0, 0], [0, 2, 0], [2, 2, 2]])
# points['coords'] = np.array([[0, 0, 0], [2, 2, 0], [1, 1, 0]])
# points['mass'] = np.array([10, 2, 500])
# sizes = np.array([10, 5, 50])
# points['speed'][-1] = np.array([0,0,0])


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(plim)
ax.set_ylim(plim)
ax.set_zlim(plim)


scat = ax.scatter(points['coords'][:,0],
           points['coords'][:,1],
           points['coords'][:,2],
           s=sizes,
           c='k', marker='o')
# ax.scatter(*[(plim[1] - plim[0]) / 2 for i in range(3)], s=100, c='r', marker='o')
# quiv = ax.quiver(points['coords'][:,0],
          # points['coords'][:,1],
          # points['coords'][:,2],
          # points['speed'][:,0],
          # points['speed'][:,1],
          # points['speed'][:,2])
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
# for i in range(200):
    # update_points(0, False)

ani = animation.FuncAnimation(fig, update_points, interval=10, blit=False)
plt.show()
