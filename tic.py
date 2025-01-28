import numpy
import matplotlib.pyplot as pyplot

width, height = 240.0, 136.0

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

def translation(tx, ty, tz):
    return numpy.array([
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ])

def perspective(fov, aspect, z_near, z_far):
    f = 1 / numpy.tan(fov / 2)
    return numpy.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (z_far + z_near) / (z_near - z_far), (2 * z_far * z_near) / (z_near - z_far)],
        [0, 0, -1, 0]
    ])

def to_pixel(x, y, width, height):
    x_pixel = int((x + 1) / 2 * width)
    y_pixel = int((1 - y) / 2 * height)  # Flip y for screen coordinates
    return x_pixel, y_pixel

# x
theta = numpy.radians(30) #30
# y
phi = numpy.radians(45) #45
# z
psi = numpy.radians(60) #60

# The 8 vertices of the cube, clockwise from top left, front to back
vertices = numpy.array([
    [-1, 1, 1, 1],
    [1, 1, 1, 1],
    [1, -1, 1, 1],
    [-1, -1, 1, 1],

    [-1, 1, -1, 1],
    [1, 1, -1, 1],
    [1, -1, -1, 1],
    [-1, -1, -1, 1],
]).T

rotation_matrix = rotation_z(psi) @ rotation_y(phi) @ rotation_x(theta)
translation_matrix = translation(0, 0, -4)
transformed_vertices = translation_matrix @ rotation_matrix @ vertices

projection_matrix = perspective(numpy.radians(60), width/height, 0.1, 100.0)
projected_vertices = projection_matrix @ transformed_vertices

projected_vertices /= projected_vertices[3]

x = projected_vertices[0]
y = projected_vertices[1]
z = projected_vertices[2]

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

# Painter's algorithm, https://en.wikipedia.org/wiki/Painter%27s_algorithm
faces.sort(key=lambda x: x[1], reverse=True)

polygons = []
for face in faces:
    coords = []
    for vertex in face[0]:
        coords.append(to_pixel(x[vertex], y[vertex], width, height))
    coords.append(face[2])
    print(coords)
    polygons.append(coords)

# Plött
pyplot.figure(figsize=(8, 8))
pyplot.gca().set_xlim(-1, 1)
pyplot.gca().set_ylim(-1, 1)
#pyplot.gca().set_aspect('equal')
pyplot.grid(True, zorder=0)


i = 0
c = ("red", "green", "blue", "cyan", "magenta", "yellow", "black")

for face in faces:
    #print(face[1], face[0], face[2])
    edge = face[0]
    xys = [(x[edge[0]], y[edge[0]]), (x[edge[1]], y[edge[1]]), (x[edge[2]], y[edge[2]])]
    t = pyplot.Polygon(xys, edgecolor='None', facecolor=c[face[2]], alpha=0.75)
    pyplot.gca().add_patch(t)
    i+=1

pyplot.show()
