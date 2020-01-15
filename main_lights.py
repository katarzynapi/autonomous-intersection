import cv2
import numpy as np
import autonomousIntersection as autointer
import mapDrawing as mapdraw
import random
import dill
import sys
import enums
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
print("green")
for i, row in enumerate(img):
    for j, col in enumerate(row):
        if np.array_equal(green, col) or np.array_equal(nw, col) or np.array_equal(sw, col):
            print(counter)
            counter+=1
            cv2.circle(clean_img, (j, i), 3, (0, 0, 0), 2)
            cv2.imshow('image', clean_img)
            cv2.waitKey(1)
            model.grid.addCell(j, i, autointer.enums.CellType.ROAD)
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
            model.grid.addCell(j, i, autointer.enums.CellType.ROAD)

cells_number = len(model.grid.cells)
model.grid.cells[0].if_border = autointer.enums.IfBorder.INPUT
model.grid.cells[int(cells_number/2)-1].if_border = autointer.enums.IfBorder.OUTPUT
model.grid.cells[int(cells_number/2):] = reversed(model.grid.cells[int(cells_number/2):])
model.grid.cells[int(cells_number/2)].if_border = autointer.enums.IfBorder.INPUT
model.grid.cells[-1].if_border = autointer.enums.IfBorder.OUTPUT

# add cells' f and b neighbours
for i, cell in enumerate(model.grid.cells):
    if cell.if_border == autointer.enums.IfBorder.INPUT:
        cell.f_neighbour = model.grid.cells[i+1]
    elif cell.if_border == autointer.enums.IfBorder.NOT:
        cell.f_neighbour = model.grid.cells[i+1]
        cell.b_neighbour = model.grid.cells[i-1]
    elif cell.if_border == autointer.enums.IfBorder.OUTPUT:
        cell.b_neighbour = model.grid.cells[i-1]

# add cells' l and r neighbours
#for o_cell, g_cell in zip (model.grid.cells[:92], model.grid.cells[92:]):
    #o_cell.l_neighbour = g_cell
    #g_cell.r_neighbour = o_cell

# _________________________________________________________
# blue cells
print("blue")
for i, row in enumerate(img):
    for j, col in enumerate(row):
        if np.array_equal(blue, col) or np.array_equal(nw, col) or np.array_equal(ne, col):
            print(counter)
            counter+=1
            cv2.circle(clean_img, (j, i), 3, (0, 0, 0), 2)
            cv2.imshow('image', clean_img)
            cv2.waitKey(1)
            model.grid.addCell(j, i, autointer.enums.CellType.ROAD)
model.grid.cells[184:286] = reversed(model.grid.cells[184:286]) 
# yellow cells
print("yellow")
for i, row in enumerate(img):
    for j, col in enumerate(row):
        if np.array_equal(yellow, col) or np.array_equal(sw, col) or np.array_equal(se, col):
            print(counter)
            counter+=1
            cv2.circle(clean_img, (j, i), 3, (0, 0, 0), 2)
            cv2.imshow('image', clean_img)
            cv2.waitKey(1)
            model.grid.addCell(j, i, autointer.enums.CellType.ROAD)

model.grid.cells[184].if_border = autointer.enums.IfBorder.INPUT
model.grid.cells[285].if_border = autointer.enums.IfBorder.OUTPUT
model.grid.cells[286].if_border = autointer.enums.IfBorder.INPUT
model.grid.cells[-1].if_border = autointer.enums.IfBorder.OUTPUT

# add cells' f and b neighbours
for i, cell in enumerate(model.grid.cells[184:]):
    if cell.if_border == autointer.enums.IfBorder.INPUT:
        cell.f_neighbour = model.grid.cells[184+i+1]
    elif cell.if_border == autointer.enums.IfBorder.NOT:
        cell.f_neighbour = model.grid.cells[184+i+1]
        cell.b_neighbour = model.grid.cells[184+i-1]
    elif cell.if_border == autointer.enums.IfBorder.OUTPUT:
        cell.b_neighbour = model.grid.cells[184+i-1]

# add cells' l and r neighbours
#for o_cell, g_cell in zip (model.grid.cells[184:286], reversed(model.grid.cells[286:])):
    #o_cell.l_neighbour = g_cell
    #g_cell.l_neighbour = o_cell


# add to list of inputs and iutputs
for cell in model.grid.cells:
    if cell.if_border == autointer.enums.IfBorder.INPUT:
        model.grid.inputs.append(cell)
    if cell.if_border == autointer.enums.IfBorder.OUTPUT:
        model.grid.outputs.append(cell)

model.grid.cells[45].r_neighbour = model.grid.cells[236]
model.grid.cells[234].r_neighbour = model.grid.cells[139]
model.grid.cells[336].r_neighbour = model.grid.cells[47]
model.grid.cells[137].r_neighbour = model.grid.cells[338]

model.grid.cells[45].l_neighbour = None
model.grid.cells[234].l_neighbour = None
model.grid.cells[336].l_neighbour = None
model.grid.cells[137].l_neighbour = None

model.grid.cells[46].l_neighbour = None
model.grid.cells[235].l_neighbour = None
model.grid.cells[337].l_neighbour = None
model.grid.cells[138].l_neighbour = None

model.grid.cells[45].fl_neighbour = model.grid.cells[337]
model.grid.cells[234].fl_neighbour = model.grid.cells[46]
model.grid.cells[336].fl_neighbour = model.grid.cells[138]
model.grid.cells[137].fl_neighbour = model.grid.cells[235]
'''
#dill.dump( model, open( "model.d", "wb" ) )
model = dill.load( open( "model.d", "rb" ) )
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

# add blockade
#model.obstacles.append(autointer.Blockade())
#model.obstacles[-1].location = model.grid.cells[20]
#model.grid.cells[20].obstacles.append(model.obstacles[-1])

#create one direction path (one road)
#current_cell = model.grid.inputs[0]
#straight_path = [current_cell]
#while current_cell.if_border != autointer.IfBorder.OUTPUT:
    #straight_path.append(current_cell.f_neighbour)
    #current_cell = current_cell.f_neighbour
#model.paths[(model.grid.inputs[0], current_cell)] = autointer.Path(autointer.PathType.MAIN, straight_path)

print("Komórki z prawymi sąsiadami:")
for c in model.grid.cells:
    if c.r_neighbour:
        print(c.getCoords())
print("")

#create one direction path (all roads)
for inp in model.grid.inputs:
#add paths for straight roads
    print("prosto")
    current_cell = inp
    straight_path = [current_cell]
    print(current_cell.getCoords())
    while current_cell.if_border != autointer.enums.IfBorder.OUTPUT:
        straight_path.append(current_cell.f_neighbour)
        current_cell = current_cell.f_neighbour
        print(current_cell.getCoords())
    model.paths[(inp, current_cell)] = autointer.Path(autointer.enums.PathType.MAIN, straight_path)

#add path with turning left
    print("lewo")
    current_cell = inp
    left_path = [current_cell]
    print(current_cell.getCoords())
    while current_cell.if_border != autointer.enums.IfBorder.OUTPUT:
        if current_cell.fl_neighbour:
            left_path.append(current_cell.f_neighbour)
            left_path.append(current_cell.fl_neighbour)
            current_cell = current_cell.fl_neighbour
            left_path.append(current_cell.f_neighbour)
            current_cell = current_cell.f_neighbour
        else:
            left_path.append(current_cell.f_neighbour)
            current_cell = current_cell.f_neighbour
        print(current_cell.getCoords())
    model.paths[(inp, current_cell)] = autointer.Path(autointer.enums.PathType.MAIN, left_path)

#add path with turning right
    print("prawo")
    current_cell = inp
    right_path = [current_cell]
    print(current_cell.getCoords())
    while current_cell.if_border != autointer.enums.IfBorder.OUTPUT:
        if current_cell.r_neighbour:
            right_path.append(current_cell.r_neighbour)
            current_cell = current_cell.r_neighbour
        else:
            right_path.append(current_cell.f_neighbour)
            current_cell = current_cell.f_neighbour
        print(current_cell.getCoords())
    model.paths[(inp, current_cell)] = autointer.Path(autointer.enums.PathType.MAIN, right_path)
    
'''for p, c in model.paths.items():
    print(p)
    for c_ in c.cells:
        print(c_.getCoords())'''
# create paths in two directions (parallel)
'''for inp in model.grid.inputs:
    #add path with going straight
    current_cell = inp
    straight_path = [current_cell]
    while current_cell.if_border != autointer.enums.IfBorder.OUTPUT:
        straight_path.append(current_cell.f_neighbour)
        current_cell = current_cell.f_neighbour
    model.paths[(inp, current_cell)] = autointer.Path(autointer.enums.PathType.MAIN, straight_path)
model.paths[(inp, current_cell)].type = autointer.PathType.ALTERNATIVE'''

# add lights
up_down_SR_paths = [k for k, v in model.paths.items() if (v.cells[0].getCoords() == (1506, 49) and v.cells[-1].getCoords() == (967, 1045)) or \
                    (v.cells[0].getCoords() == (1506, 49) and v.cells[-1].getCoords() == (688, 321)) or \
                    (v.cells[0].getCoords() == (978, 1049) and v.cells[-1].getCoords() == (1517, 54)) or \
                    (v.cells[0].getCoords() == (978, 1049) and v.cells[-1].getCoords() == (1793, 773))]
up_down_L_paths = [k for k, v in model.paths.items() if (v.cells[0].getCoords() == (1506, 49) and v.cells[-1].getCoords() == (1793, 773)) or \
                    (v.cells[0].getCoords() == (978, 1049) and v.cells[-1].getCoords() == (688, 321))]
left_right_SR_paths = [k for k, v in model.paths.items() if (v.cells[0].getCoords() == (1799, 762) and v.cells[-1].getCoords() == (688, 321)) or \
                    (v.cells[0].getCoords() == (1799, 762) and v.cells[-1].getCoords() == (1517, 54)) or \
                    (v.cells[0].getCoords() == (682, 332) and v.cells[-1].getCoords() == (1793, 773)) or \
                    (v.cells[0].getCoords() == (682, 332) and v.cells[-1].getCoords() == (967, 1045))]
left_right_L_paths = [k for k, v in model.paths.items() if (v.cells[0].getCoords() == (1799, 762) and v.cells[-1].getCoords() == (967, 1045)) or \
                    (v.cells[0].getCoords() == (682, 332) and v.cells[-1].getCoords() == (1517, 54))]
#0
model.lights.append(autointer.Lights())
model.lights[-1].location = model.grid.cells[44]
model.lights[-1].connected_paths = up_down_SR_paths
model.grid.cells[44].obstacles.append(model.lights[-1])
#1
model.lights.append(autointer.Lights())
model.lights[-1].location = model.grid.cells[136]
model.lights[-1].connected_paths = up_down_SR_paths
model.grid.cells[136].obstacles.append(model.lights[-1])
#2
model.lights.append(autointer.Lights())
model.lights[-1].location = model.grid.cells[44]
model.lights[-1].connected_paths = up_down_L_paths
model.lights[-1].colour = enums.Colour.RED
model.grid.cells[44].obstacles.append(model.lights[-1])
#3
model.lights.append(autointer.Lights())
model.lights[-1].location = model.grid.cells[136]
model.lights[-1].connected_paths = up_down_L_paths
model.lights[-1].colour = enums.Colour.RED
model.grid.cells[136].obstacles.append(model.lights[-1])
#_______________________________________________________
#4
model.lights.append(autointer.Lights())
model.lights[-1].location = model.grid.cells[233]
model.lights[-1].connected_paths = left_right_SR_paths
model.lights[-1].colour = enums.Colour.RED
model.grid.cells[233].obstacles.append(model.lights[-1])
#5
model.lights.append(autointer.Lights())
model.lights[-1].location = model.grid.cells[335]
model.lights[-1].connected_paths = left_right_SR_paths
model.lights[-1].colour = enums.Colour.RED
model.grid.cells[335].obstacles.append(model.lights[-1])
#6
model.lights.append(autointer.Lights())
model.lights[-1].location = model.grid.cells[233]
model.lights[-1].connected_paths = left_right_L_paths
model.lights[-1].colour = enums.Colour.RED
model.grid.cells[233].obstacles.append(model.lights[-1])
#7
model.lights.append(autointer.Lights())
model.lights[-1].location = model.grid.cells[335]
model.lights[-1].connected_paths = left_right_L_paths
model.lights[-1].colour = enums.Colour.RED
model.grid.cells[335].obstacles.append(model.lights[-1])

# simulate agent movement along the road
destination_reached = False
i = 0
while True:
    print("")
    print(i)
    print("Światło:")
    print(model.lights[0].colour)
    print(model.lights[2].colour)
    #print("Lokalizacja przeszkody:")
    #print(model.grid.cells[20].getCoords())
    if i%3==0:
        colors = [(0, 0, 255), (0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 0, 255), (255, 255, 0), (255, 255, 255), (0, 0, 0)]
        color = random.choice(colors)
        #paths = [1]
        path = random.choice(list(model.paths.keys()))
        path_in, path_out = path
        lengths = [2, 3, 4, 5]
        length = random.choice(lengths)
        # add default agent to model
        model.generateAgent()
        model.agents[-1].color = color
        model.agents[-1].length = length
        model.agents[-1].ascribe_paths(model.paths)
        model.agents[-1].destination = path_out
        model.agents[-1].place_on_grid(path_in, path)
        #model.agents[-1].path.extend(model.paths[(model.grid.inputs[0], model.grid.outputs[0])][5:])
    model.image = clean_img.copy()
    model.step()
    model.showAgentMovement(5)
    #destination_reached = model.agents[0].reached_destination()
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