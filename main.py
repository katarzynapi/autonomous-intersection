import cv2
import numpy as np
import autonomousIntersection as autointer
import mapDrawing as mapdraw

# import map image
img = cv2.imread('armii_krajowej_road_circles.png')
clean_img = cv2.imread('armii_krajowej.png')
height, width, channels = img.shape

#create model for imported map
model = autointer.IntersectionModel(0, 0, width, height)
model.image = img

street_color = [248, 209, 7]

# add cells for road fragment (based on centers of drawn circles = cells)
for i, row in enumerate(img):
    for j, col in enumerate(row):
        if np.array_equal(street_color, col):
            cv2.circle(clean_img, (j, i), 7, (0, 0, 0), 2)
            cv2.imshow('image', clean_img)
            cv2.waitKey(1)
            model.grid.addCell(j, i, autointer.CellType.ROAD)

model.grid.cells[0].if_border = autointer.IfBorder.INPUT
model.grid.cells[-1].if_border = autointer.IfBorder.OUTPUT

# add cells' neighbours
for i, cell in enumerate(model.grid.cells):
    if cell.if_border == autointer.IfBorder.INPUT:
        cell.f_neighbour = model.grid.cells[i+1]
    elif cell.if_border == autointer.IfBorder.NOT:
        cell.f_neighbour = model.grid.cells[i+1]
        cell.b_neighbour = model.grid.cells[i-1]
    elif cell.if_border == autointer.IfBorder.OUTPUT:
        cell.b_neighbour = model.grid.cells[i-1]

x, y = model.grid.cells[30].getCoords()
#mapdraw.drawNewCircle(x, y, clean_img)


# simulate agent movement along the road
destination_reached = False
i = 0
while destination_reached == False:
    if i%100==0:
        # add default agent to model
        idx = int(i/100)
        model.generateAgent()
        model.agents[idx].head = model.grid.cells[2]
        model.agents[idx].tail = model.grid.cells[0]
    model.image = clean_img.copy()
    model.showAgentMovement(0, 15)
    model.step()
    destination_reached = model.agents[0].reached_destination()
    i+=1

cv2.destroyAllWindows()