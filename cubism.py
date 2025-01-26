import numpy
import matplotlib.pyplot as pyplot

# Light reading:
# https://en.wikipedia.org/wiki/Homogeneous_coordinates
# https://en.wikipedia.org/wiki/Radian
# https://en.wikipedia.org/wiki/Rotation_matrix#In_three_dimensions
# https://en.wikipedia.org/wiki/Projection_(linear_algebra)

# Define the cube centered at 0 with the side length 2 in 3D space.
# Negative numbers go up, to the left and away
# The "top left" corner is -1, -1, -1 (x, y, z)
# 3D coordinates:
# -1, -1,  1 (front top left)
#  1, -1,  1 (front top right)
# -1,  1,  1 (front bottom left)
#  1,  1,  1 (front bottom right)
# -1, -1, -1 (back top left)
#  1, -1, -1 (back top right)
# -1,  1, -1 (back bottom left)
#  1,  1, -1 ((back bottom right)

# Homogenous coordinates (x, y, z, w) in 8x4. Each row is a vertex.
vertices = numpy.array([
    [-1, -1, 1, 1],
    [1, -1, 1, 1],
    [-1, 1, 1, 1],
    [1, 1, 1, 1],
    [-1, -1, -1, 1],
    [1, -1, -1, 1],
    [-1, 1, -1, 1],
    [1, 1, -1, 1]
])

# Transpose matrix to 4x8. Each column is a vertex.
vertices = vertices.T

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

# Define the erspective projection matrix. d = distance from the camera.
def perspective(d):
    return numpy.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, -1/d, 1]
    ])

# Define rotation angles in degrees, convert to radians
# x
theta = numpy.radians(0)
# y
phi = numpy.radians(382)
# z
psi = numpy.radians(0)

# Define distance to camera
d = 5

# Combine transformation matricies and transform vertices
transformation = rotation_z(psi) @ rotation_y(phi) @ rotation_x(theta)
transformed = transformation @ vertices

# Project transformed verticies using projection matrix
projection = perspective(d)
projected = projection @ transformed

# Convert to cartesian coordinates, normalize by w
projected /= projected[3]

# Extract 2D coordinates
x = projected[0]
y = projected[1]

# Define cube edges
# Front:
# 0 + ----- + 1
#   |       |
#   |       |
# 2 + ----- + 3
#
# Back (as seen from front):
# 4 + ----- + 5
#   |       |
#   |       |
# 6 + ----- + 7
#
# Connecting:
# 0 - 4
# 1 - 5
# 2 - 6
# 3 - 7

edges = [
    (0, 1), (1, 3), (3, 2), (2, 0),
    (4, 5), (5, 7), (7, 6), (6, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

pyplot.figure(figsize=(8, 8))

# Draw front edges
for edge in (0, 1, 2, 3):
    pyplot.plot([x[edges[edge][0]], x[edges[edge][1]]], [y[edges[edge][0]], y[edges[edge][1]]], "c-")

# Draw back edges
for edge in (4, 5, 6, 7):
    pyplot.plot([x[edges[edge][0]], x[edges[edge][1]]], [y[edges[edge][0]], y[edges[edge][1]]], "m-")

# Draw connecting edges ("sides")
for edge in (8, 9):
    pyplot.plot([x[edges[edge][0]], x[edges[edge][1]]], [y[edges[edge][0]], y[edges[edge][1]]], "y-")
for edge in (10, 11):
    pyplot.plot([x[edges[edge][0]], x[edges[edge][1]]], [y[edges[edge][0]], y[edges[edge][1]]], "k-")

# Draw lines between vertices
#for edge in edges:
#    xs = [x[edge[0]], x[edge[1]]]
#    ys = [y[edge[0]], y[edge[1]]]
#    pyplot.plot(xs, ys, "b-")

pyplot.grid(True)
pyplot.show()

# TODO (in C99 (or Lua...)):
# Implement transposing of matrixes
# Implement degrees to radians
# Implement "dynamic" matrixes
# Implement matrix multiplication
# Convert cartesian coordinates to "pixel" coordinates