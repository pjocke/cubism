# title:   matmult
# author:  pjocke, ChatGPT
# desc:    
# site:    
# license:
# version: 0.1
# script:  python

import math

width, height = 240.0, 136.0

def matrix_multiply(A, B):
    # Validate if multiplication is possible
    if len(A[0]) != len(B):
        raise ValueError("Number of columns in A must equal number of rows in B")
    
    # Get dimensions of the result matrix
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    
    # Initialize the result matrix with zeros
    result = [[0 for _ in range(cols_B)] for _ in range(rows_A)]
    
    # Perform matrix multiplication
    for i in range(rows_A):          # Iterate through rows of A
        for j in range(cols_B):      # Iterate through columns of B
            for k in range(cols_A):  # Iterate through columns of A / rows of B
                result[i][j] += A[i][k] * B[k][j]
    
    return result

def element_wise_division_in_place(arr1, arr2):
    # Ensure the arrays have the same length
    if len(arr1) != len(arr2):
        raise ValueError("Arrays must have the same length")
    
    # Perform element-wise division in place
    for i in range(len(arr1)):
        arr1[i] /= arr2[i]  # Update arr1 in place

def rotation_x(theta):
    return [
        [1, 0, 0, 0],
        [0, math.cos(theta), -math.sin(theta), 0],
        [0, math.sin(theta), math.cos(theta), 0],
        [0, 0, 0, 1]
    ]

def rotation_y(phi):
    return [
        [math.cos(phi), 0, math.sin(phi), 0],
        [0, 1, 0, 0],
        [-math.sin(phi), 0, math.cos(phi), 0],
        [0, 0, 0, 1]
    ]

def rotation_z(psi):
    return [
        [math.cos(psi), -math.sin(psi), 0, 0],
        [math.sin(psi), math.cos(psi), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ]

def translation(tx, ty, tz):
    return [
        [1, 0, 0, tx],
        [0, 1, 0, ty],
        [0, 0, 1, tz],
        [0, 0, 0, 1]
    ]

def perspective(fov, aspect, z_near, z_far):
    f = 1 / math.tan(fov / 2)
    return [
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (z_far + z_near) / (z_near - z_far), (2 * z_far * z_near) / (z_near - z_far)],
        [0, 0, -1, 0]
    ]

def to_pixel(x, y, width, height):
    x_pixel = int((x + 1) / 2 * width)
    y_pixel = int((1 - y) / 2 * height)  # Flip y for screen coordinates
    return x_pixel, y_pixel

# Vertexes for the cube
vertices = [
    [-4,  4,  4, 1],
    [ 4,  4,  4, 1],
    [ 4, -4,  4, 1],
    [-4, -4,  4, 1],
    [-4,  4, -4, 1],
    [ 4,  4, -4, 1],
    [ 4, -4, -4, 1],
    [-4, -4, -4, 1],
]

# Transpose
transposed_vertices = []
for col in range(len(vertices[0])):  # Iterate over columns of the original matrix
    new_row = []
    for row in range(len(vertices)):  # Iterate over rows of the original matrix
        new_row.append(vertices[row][col])  # Collect elements in the new row
    transposed_vertices.append(new_row)

degrees = 0
counter = 0
direction = 1

# This shit is done 60 times a second, rip
def TIC():
    global counter, direction, degrees

    trans_x = (counter / width) * (5 - -5) + -5
    trans_y = 1 * math.sin(trans_x)
    if direction == -1:
     trans_y = -trans_y
    
    zoom = (counter / width) * (-30 - -15) + -15

    # x
    theta = math.radians(degrees%360) #30
    # y
    phi = math.radians(-degrees%360) #45
    # z
    psi = math.radians(60) #60

    # Combine X, Y and Z rotation matrics to one rotation matrix
    rotation_matrix = matrix_multiply(rotation_z(psi), rotation_y(phi))
    rotation_matrix = matrix_multiply(rotation_matrix, rotation_x(theta))

    # Combine the rotation and translation matrices to one transformation matrix
    translation_matrix = translation(trans_x, trans_y, zoom)
    transformation_matrix = matrix_multiply(translation_matrix, rotation_matrix)

    # Do the transformation
    transformed_vertices = matrix_multiply(transformation_matrix, transposed_vertices)

    # Do the projection
    projection_matrix = perspective(math.radians(60), width/height, 0.1, 100.0)
    projected_vertices = matrix_multiply(projection_matrix, transformed_vertices)

    # Normalize by w
    element_wise_division_in_place(projected_vertices[0], projected_vertices[3])
    element_wise_division_in_place(projected_vertices[1], projected_vertices[3])
    element_wise_division_in_place(projected_vertices[2], projected_vertices[3])

    # Yes
    x = projected_vertices[0]
    y = projected_vertices[1]
    z = projected_vertices[2]

    # The six pair of faces of the cube, vertices and average depth
    faces = [
        # Front
        [(0, 1, 3), (z[0]+z[1]+z[3])/3 + (z[3]+z[1]+z[2])/3, 0],
        [(3, 1, 2), (z[0]+z[1]+z[3])/3 + (z[3]+z[1]+z[2])/3, 0],

        # Back
        [(4, 5, 7), (z[4]+z[5]+z[7])/3 + (z[7]+z[5]+z[6])/3, 1],
        [(7, 5, 6), (z[4]+z[5]+z[7])/3 + (z[7]+z[5]+z[6])/3, 1],

        # Left
        [(4, 0, 7), (z[4]+z[0]+z[7])/3 + (z[7]+z[0]+z[3])/3, 2],
        [(7, 0, 3), (z[4]+z[0]+z[7])/3 + (z[7]+z[0]+z[3])/3, 2],

        # Right
        [(1, 5, 2), (z[1]+z[5]+z[2])/3 + (z[2]+z[5]+z[6])/3, 3],
        [(2, 5, 6), (z[1]+z[5]+z[2])/3 + (z[2]+z[5]+z[6])/3, 3],

        # Top
        [(4, 5, 0), (z[4]+z[5]+z[0])/3 + (z[0]+z[5]+z[1])/3, 4],
        [(0, 5, 1), (z[4]+z[5]+z[0])/3 + (z[0]+z[5]+z[1])/3, 4],

        # Bottom
        [(7, 6, 3), (z[7]+z[6]+z[3])/3 + (z[3]+z[6]+z[2])/3, 5],
        [(3, 6, 2), (z[7]+z[6]+z[3])/3 + (z[3]+z[6]+z[2])/3, 5]
    ]

    # Painter's algorithm, https://en.wikipedia.org/wiki/Painter%27s_algorithm
    faces.sort(key=lambda x: x[1], reverse=True)

    # Clear screen
    cls(0)
    
    print(trans_x, 10, 10, 12)
    print(trans_y, 10, 20, 12)

    for face in faces:
        coords = []
        for vertex in face[0]:
            # Convert to pixels
            coords.append(to_pixel(x[vertex], y[vertex], width, height))
        tri(coords[0][0], coords[0][1], coords[1][0], coords[1][1], coords[2][0], coords[2][1], 1+face[2])

    counter += direction

    if counter == width:
        direction = -1
    elif counter == 0:
        direction = 1

    degrees += 1
