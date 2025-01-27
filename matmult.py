import numpy
import matplotlib.pyplot as pyplot

# Tetrahexahedron (https://en.wikipedia.org/wiki/Tetrakis_hexahedron)
#
# TODO: change from equilateral to isosceles triangles
#       simplify vertices to be only points
#

vertices = numpy.array([
    # Left (x centered)
    [-2, 0, 0, 1],
    [-1, 1, -1, 1],
    [-1, 1, 1, 1],
    [-2, 0, 0, 1],
    [-1, 1, -1, 1],
    [-1, -1, -1, 1],
    [-2, 0, 0, 1],
    [-1, -1, -1, 1],
    [-1, -1, 1, 1],
    [-2, 0, 0, 1],
    [-1, 1, 1, 1],
    [-1, -1, 1, 1],

    # Right
    [2, 0, 0, 1],
    [1, 1, -1, 1],
    [1, 1, 1, 1],
    [2, 0, 0, 1],
    [1, 1, -1, 1],
    [1, -1, -1, 1],
    [2, 0, 0, 1],
    [1, -1, -1, 1],
    [1, -1, 1, 1],
    [2, 0, 0, 1],
    [1, 1, 1, 1],
    [1, -1, 1, 1],

    # Top (y centered)
    [0, 2, 0, 1],
    [1, 1, 1, 1],
    [1, 1, -1, 1],
    [0, 2, 0, 1],
    [1, 1, -1, 1],
    [-1, 1, -1, 1],
    [0, 2, 0, 1],
    [-1, 1, -1, 1],
    [-1, 1, 1, 1],
    [0, 2, 0, 1],
    [-1, 1, 1, 1],
    [1, 1, 1, 1],

    # Bottom
    [0, -2, 0, 1],
    [1, -1, 1, 1],
    [1, -1, -1, 1],
    [0, -2, 0, 1],
    [1, -1, -1, 1],
    [-1, -1, -1, 1],
    [0, -2, 0, 1],
    [-1, -1, -1, 1],
    [-1, -1, 1, 1],
    [0, -2, 0, 1],
    [-1, -1, 1, 1],
    [1, -1, 1, 1],

    # Front (z centered)
    [0, 0, 2, 1],
    [1, -1, 1, 1],
    [1, 1, 1, 1],
    [0, 0, 2, 1],
    [1, -1, 1, 1],
    [-1, -1, 1, 1],
    [0, 0, 2, 1],
    [-1, -1, 1, 1],
    [-1, 1, 1, 1],
    [0 ,0, 2, 1],
    [-1, 1, 1, 1],
    [1, 1, 1, 1],

    # Back
    [0, 0, -2, 1],
    [1, -1, -1, 1],
    [1, 1, -1, 1],
    [0, 0, -2, 1],
    [1, -1, -1, 1],
    [-1, -1, -1, 1],
    [0, 0, -2, 1],
    [-1, -1, -1, 1],
    [-1, 1, -1, 1],
    [0 ,0, -2, 1],
    [-1, 1, -1, 1],
    [1, 1, -1, 1],
]).T

# Define the transformation matrices in homogenous coordinates
def rotation_x(theta):
    return numpy.array([
        [1, 0, 0, 0],
        [0, numpy.cos(theta), -numpy.sin(theta), 0],
        [0, numpy.sin(theta), numpy.cos(theta), 0],
        [0, 0, 0, 1]
    ])

def rotation_y(phi):
    return numpy.array([
        [numpy.cos(phi), 0, numpy.sin(phi), 0],
        [0, 1, 0, 0],
        [-numpy.sin(phi), 0, numpy.cos(phi), 0],
        [0, 0, 0, 1]
    ])

def rotation_z(psi):
    return numpy.array([
        [numpy.cos(psi), -numpy.sin(psi), 0, 0],
        [numpy.sin(psi), numpy.cos(psi), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

# Define the perspective projection matrix. d = distance from the camera.
def perspective(d):
    return numpy.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, -1/d, 1]
    ])

# x
theta = numpy.radians(5)
# y
phi = numpy.radians(5)
# z
psi = numpy.radians(5)

# Distance
d = 5

projected = perspective(d) @ ((rotation_z(psi) @ rotation_y(phi) @ rotation_x(theta)) @ vertices)
projected /= projected[3]

# Extract 2D coordinates
x = projected[0]
y = projected[1]

# Define edges
edges = [
    (0, 1), (1, 2) , (2, 0),
    (3, 4), (4, 5), (5, 3),
    (6, 7), (7, 8), (8, 6),
    (9, 10), (10, 11), (11, 9),

    (12, 13), (13, 14), (14, 12),
    (15, 16), (16, 17), (17, 15),
    (18, 19), (19, 20), (20, 18),
    (21, 22), (22, 23), (23, 21),

    (24, 25), (25, 26), (26, 24),
    (27, 28), (28, 29), (29, 27),
    (30, 31), (31, 32), (32, 30),
    (33, 34), (34, 35), (35, 33),

    (36, 37), (37, 38), (38, 36),
    (39, 40), (40, 41), (41, 39),
    (42, 43), (43, 44), (44, 42),
    (45, 46), (46, 47), (47, 45),

    (48, 49), (49, 50), (50, 48),
    (51, 52), (52, 53), (53, 51),
    (54, 55), (55, 56), (56, 54),
    (57, 58), (58, 59), (59, 57),

    (60, 61), (61, 62), (62, 60),
    (63, 64), (64, 65), (65, 63),
    (66, 67), (67, 68), (68, 66),
    (69, 70), (70, 71), (71, 69)
]

pyplot.figure(figsize=(8, 8))

# Draw edges
for edge in edges:
    xs = [x[edge[0]], x[edge[1]]]
    ys = [y[edge[0]], y[edge[1]]]
    pyplot.plot(xs, ys, "b-")

pyplot.grid(True)
pyplot.show()
