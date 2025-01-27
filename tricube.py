import numpy
import matplotlib.pyplot as pyplot

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
theta = numpy.radians(22.5)
# y
phi = numpy.radians(22.5)
# z
psi = numpy.radians(22.5)

# Distance
d = 20

# A cube needs no more than 8 vertices
# Clockwise from top left, back and front
vertices = numpy.array([
    [-4, 4, -4, 1],
    [4, 4, -4, 1],
    [4, -4, -4, 1],
    [-4, -4, -4, 1],

    [-4, 4, 4, 1],
    [4, 4, 4, 1],
    [4, -4, 4, 1],
    [-4, -4, 4, 1],
]).T


projected = perspective(d) @ ((rotation_z(psi) @ rotation_y(phi) @ rotation_x(theta)) @ vertices)
projected /= projected[3]

# Extract 2D coordinates
x = projected[0]
y = projected[1]

# A cube needs 12 edges
#edges = [
#    (0, 1), (1, 2), (2, 3), (3, 0),
#    (0, 4), (1, 5), (2, 6), (3, 7),
#    (4, 5), (5, 6), (6, 7), (7, 4)
#]

# Let's do this with triangles.
#edges = [
#    (0, 1, 3), (1, 2, 3), (0, 4, 3), (4, 7, 3),
#    (1, 5, 2), (5, 6, 2), (4, 5, 7), (5, 6, 7),
#    (1, 5, 4), (1, 4, 0), (3, 7, 2), (2, 6, 7)
#]

# Now we're dealing with faces.
# This needs fixing to become more uniform.
faces = [
    # Back
    ((0, 1, 3), (1, 2, 3)),

    # Right
    ((1, 5, 2), (5, 6, 2)),

    # Top
    ((1, 5, 4), (1, 4, 0)),

    # Bottom
    ((3, 7, 2), (2, 6, 7)),

    # Left
    ((0, 4, 3), (4, 7, 3)),

    # Front
    ((4, 5, 7), (5, 6, 7)),
]

pyplot.figure(figsize=(8, 8))
pyplot.gca().set_xlim(-8, 8)
pyplot.gca().set_ylim(-8, 8)
pyplot.gca().set_aspect('equal')
pyplot.grid(True, zorder=0)

# Draw edges
#for edge in edges:
#    xys = [(x[edge[0]], y[edge[0]]), (x[edge[1]], y[edge[1]]), (x[edge[2]], y[edge[2]])]
#    t = pyplot.Polygon(xys, edgecolor='blue', facecolor='red', alpha=0.5, zorder=1)
#    pyplot.gca().add_patch(t)

i = 0
#c = ("red", "green", "blue", "cyan", "magenta", "yellow", "black")
c = ("cyan", "magenta", "yellow", "red", "green", "blue")

# Draw faces
for face in faces:
    for edge in face:
        xys = [(x[edge[0]], y[edge[0]]), (x[edge[1]], y[edge[1]]), (x[edge[2]], y[edge[2]])]
        t = pyplot.Polygon(xys, edgecolor='None', facecolor=c[i%6], alpha=1)
        pyplot.gca().add_patch(t)
    i+=1

pyplot.show()
