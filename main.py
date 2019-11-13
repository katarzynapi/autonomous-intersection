import cv2
import numpy as np
import autonomousIntersection as autointer
import mapDrawing as mapdraw

# import map image
img = cv2.imread('armii_krajowej_road_circles.png')
clean_img = img.copy()
height, width, channels = img.shape

#create grid for map
map_grid = autointer.Grid(0, 0, width, height)

#cv2.imshow('image', img)
#cv2.waitKey(1000)
street_color = [248, 209, 7]

# add cells for road fragment (based on centers of drawn circles = cells)
for i, row in enumerate(img):
    for j, col in enumerate(row):
        if np.array_equal(street_color, col):
            #cv2.circle(img, (j, i), 5, (0, 0, 0), 3)
            #cv2.imshow('image', img)
            #cv2.waitKey(10)
            map_grid.addCell(j, i, autointer.CellType.ROAD)
#print(map_grid.getCells()[0].getCoords())

# create agent
first_agent = autointer.GeneralAgent()
for start_cell, end_cell in zip(map_grid.getCells()[:-3], map_grid.getCells()[3:]):
    first_agent.head = start_cell.getCoords()
    first_agent.tail = end_cell.getCoords()
    image = clean_img.copy()
    mapdraw.drawNewLine(first_agent.head, first_agent.tail, 8, image)

'''
for start_point, end_point in zip(locations[:-3], locations[3:]):
    image = clean.copy()
    drawNewLine(start_point, end_point, 8, image)

cv2.destroyAllWindows()'''