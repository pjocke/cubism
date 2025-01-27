import numpy
import matplotlib.pyplot as pyplot

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

def perspective(d):
    return numpy.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, -1/d, 1]
    ])

# x
theta = numpy.radians(30)
# y
phi = numpy.radians(45)
# z
psi = numpy.radians(60)

# Distance
d = 20

# The 8 vertices of the cube, clockwise from top left, front to back
vertices = numpy.array([
    [-4, 4, 4, 1],
    [4, 4, 4, 1],
    [4, -4, 4, 1],
    [-4, -4, 4, 1],

    [-4, 4, -4, 1],
    [4, 4, -4, 1],
    [4, -4, -4, 1],
    [-4, -4, -4, 1],
]).T

projected = perspective(d) @ ((rotation_z(psi) @ rotation_y(phi) @ rotation_x(theta)) @ vertices)
projected /= projected[3]

x = projected[0]
y = projected[1]
z = projected[2]

# The six pair of faces of the cube, vertices and average depth
faces = [
    # Front
    [(0, 1, 3), (z[0]+z[1]+z[3])/3, 0],
    [(3, 1, 2), (z[3]+z[1]+z[2])/3, 0],

    # Back
    [(4, 5, 7), (z[4]+z[5]+z[7])/3, 1],
    [(7, 5, 6), (z[7]+z[5]+z[6])/3, 1],

    # Left
    [(4, 0, 7), (z[4]+z[0]+z[7])/3, 2],
    [(7, 0, 3), (z[7]+z[0]+z[3])/3, 2],

    # Right
    [(1, 5, 2), (z[1]+z[5]+z[2])/3, 3],
    [(2, 5, 6), (z[2]+z[5]+z[6])/3, 3],

    # Top
    [(4, 5, 0), (z[4]+z[5]+z[0])/3, 4],
    [(0, 5, 1), (z[0]+z[5]+z[1])/3, 4],

    # Bottom
    [(7, 6, 3), (z[7]+z[6]+z[3])/3, 5],
    [(3, 6, 2), (z[3]+z[6]+z[2])/3, 5]
]

# Painter's algorithm
faces.sort(key=lambda x: x[1])

# Plött
pyplot.figure(figsize=(8, 8))
pyplot.gca().set_xlim(-8, 8)
pyplot.gca().set_ylim(-8, 8)
pyplot.gca().set_aspect('equal')
pyplot.grid(True, zorder=0)

i = 0
c = ("red", "green", "blue", "cyan", "magenta", "yellow", "black")

for face in faces:
    edge = face[0]
    xys = [(x[edge[0]], y[edge[0]]), (x[edge[1]], y[edge[1]]), (x[edge[2]], y[edge[2]])]
    t = pyplot.Polygon(xys, edgecolor='None', facecolor=c[face[2]], alpha=0.75)
    pyplot.gca().add_patch(t)
    i+=1

pyplot.show()
