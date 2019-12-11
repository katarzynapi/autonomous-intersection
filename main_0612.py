import cv2
import numpy as np
import autonomousIntersection as autointer
import mapDrawing as mapdraw
import random
import dill
import sys
sys.setrecursionlimit(10000)

'''def find_nearest_pixel(pixels, init_pixel):
    INIT_PIXEL_COORDS, INIT_PIXEL_ID = init_pixel
    distances = np.sqrt((INIT_PIXEL_COORDS[0] - pixels[:][0]) ** 2 + (INIT_PIXEL_COORDS[1] - pixels[:][1]) ** 2)
    nearest_pixel = np.argmin(distances)
    return pixels[nearest_pixel], nearest_pixel'''

# import map image
img = cv2.imread('Xcross_cell_colors.png')
clean_img = cv2.imread('Xcross_cell_colors.png')
height, width, channels = img.shape

#create model for imported map
model = autointer.IntersectionModel(0, 0, width, height)
model.image = img
cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 1500, 735)

orange = [87, 189, 254]
green = [87, 193, 135]
nw = [10, 29, 148]
ne = [12, 56, 143]
sw = [33, 128, 254]
se = [26, 103, 223]
blue = [222, 179, 6]
yellow = [94, 247, 254]
counter = 0
'''
# add cells for road fragment (based on centers of drawn circles = cells)
# green cells
for i, row in enumerate(img):
    for j, col in enumerate(row):
        if np.array_equal(green, col) or np.array_equal(nw, col) or np.array_equal(sw, col):
            print(counter)
            counter+=1
            cv2.circle(clean_img, (j, i), 3, (0, 0, 0), 2)
            cv2.imshow('image', clean_img)
            cv2.waitKey(1)
            model.grid.addCell(j, i, autointer.CellType.ROAD)
# orange cells
print("orange")
for i, row in enumerate(img):
    for j, col in enumerate(row):
        if np.array_equal(orange, col) or np.array_equal(ne, col) or np.array_equal(se, col):
            print(counter)
            counter+=1
            cv2.circle(clean_img, (j, i), 3, (0, 0, 0), 2)
            cv2.imshow('image', clean_img)
            cv2.waitKey(1)
            model.grid.addCell(j, i, autointer.CellType.ROAD)
print("green")

cells_number = len(model.grid.cells)
model.grid.cells[0].if_border = autointer.IfBorder.INPUT
model.grid.cells[int(cells_number/2)-1].if_border = autointer.IfBorder.OUTPUT
model.grid.cells[int(cells_number/2)].if_border = autointer.IfBorder.INPUT
model.grid.cells[-1].if_border = autointer.IfBorder.OUTPUT

# add cells' f and b neighbours
for i, cell in enumerate(model.grid.cells):
    if cell.if_border == autointer.IfBorder.INPUT:
        cell.f_neighbour = model.grid.cells[i+1]
    elif cell.if_border == autointer.IfBorder.NOT:
        cell.f_neighbour = model.grid.cells[i+1]
        cell.b_neighbour = model.grid.cells[i-1]
    elif cell.if_border == autointer.IfBorder.OUTPUT:
        cell.b_neighbour = model.grid.cells[i-1]

# add cells' l and r neighbours
for o_cell, g_cell in zip (model.grid.cells[:92], model.grid.cells[92:]):
    o_cell.l_neighbour = g_cell
    g_cell.r_neighbour = o_cell

# add to list of inputs and iutputs
for cell in model.grid.cells:
    if cell.if_border == autointer.IfBorder.INPUT:
        model.grid.inputs.append(cell)
    if cell.if_border == autointer.IfBorder.OUTPUT:
        model.grid.outputs.append(cell)
'''
#dill.dump( model, open( "model1.d", "wb" ) )
model = dill.load( open( "model1.d", "rb" ) )
#_______________________________________________________________________
'''for i, cell in enumerate(model.grid.cells):
    print(i)
    print(cell.getCoords())
    print(cell.if_border)
    print("forward")
    if cell.f_neighbour:
        print(cell.f_neighbour.getCoords())
    print("backward")
    if cell.b_neighbour:
        print(cell.b_neighbour.getCoords())
    print("left")
    if cell.l_neighbour:
        print(cell.l_neighbour.getCoords())
    print("right")
    if cell.r_neighbour:
        print(cell.r_neighbour.getCoords())
    print("")
'''

#create one direction path
'''current_cell = model.grid.inputs[0]
straight_path = [current_cell]
while current_cell.if_border != autointer.IfBorder.OUTPUT:
    straight_path.append(current_cell.f_neighbour)
    current_cell = current_cell.f_neighbour
model.paths[(model.grid.inputs[0], current_cell)] = autointer.Path(autointer.PathType.MAIN, straight_path)'''

# add lights
model.lights.append(autointer.Lights())
model.lights[0].location = model.grid.cells[20]
model.grid.cells[20].obstacles.append(model.lights[-1])
# add blockade
#model.obstacles.append(autointer.Blockade())
#model.obstacles[-1].location = model.grid.cells[20]
#model.grid.cells[20].obstacles.append(model.obstacles[-1])

# create paths in two directions (parallel)
for inp in model.grid.inputs:
    #add path with going straight
    current_cell = inp
    straight_path = [current_cell]
    while current_cell.if_border != autointer.IfBorder.OUTPUT:
        straight_path.append(current_cell.f_neighbour)
        current_cell = current_cell.f_neighbour
    model.paths[(inp, current_cell)] = autointer.Path(autointer.PathType.MAIN, straight_path)
model.paths[(inp, current_cell)].type = autointer.PathType.ALTERNATIVE

# simulate agent movement along the road
destination_reached = False
i = 0
while destination_reached == False:
    print("")
    print(i)
    print(model.lights[0].colour)
    if i%100==0:
        # add default agent to model
        model.generateAgent()
        model.agents[-1].ascribe_paths(list(model.paths.values()))
        model.agents[-1].place_on_grid(model.grid.inputs[0])
        #model.agents[-1].path.extend(model.paths[(model.grid.inputs[0], model.grid.outputs[0])][5:])
        model.agents[-1].destination = model.grid.outputs[0]
    model.image = clean_img.copy()
    model.showAgentMovement(0, 8)
    model.step()
    destination_reached = model.agents[0].reached_destination()
    i+=1

cv2.destroyAllWindows()


'''pixels = []
for i in model.grid.cells:
    pixels.add((i.coords.getCoordinates(), i))
init_pixel = pixels[-1]
while pixels:
    nearest_pixel, idx = find_nearest_pixel(pixels, init_pixel)
    init_pixel = nearest_pixel
    del pixels[idx]'''