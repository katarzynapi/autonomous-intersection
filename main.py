import cv2
import numpy as np
import autonomousIntersection as autointer
import mapDrawing as mapdraw

# import map image
img = cv2.imread('armii_krajowej_road_circles.png')
clean_img = img.copy()
height, width, channels = img.shape

#create model for imported map
model = autointer.IntersectionModel(0, 0, width, height)
model.image = img

street_color = [248, 209, 7]

# add cells for road fragment (based on centers of drawn circles = cells)
for i, row in enumerate(img):
    for j, col in enumerate(row):
        if np.array_equal(street_color, col):
            #cv2.circle(img, (j, i), 5, (0, 0, 0), 3)
            #cv2.imshow('image', img)
            #cv2.waitKey(10)
            model.grid.addCell(j, i, autointer.CellType.ROAD)

# add default agent to model
model.addAgent()
# simulate agent movement along the road
for start_cell, end_cell in zip(model.grid.getCells()[:-3], model.grid.getCells()[3:]):
    model.image = clean_img.copy()
    model.showAgentMovement(0, 8, start_cell.getCoords(), end_cell.getCoords())

cv2.destroyAllWindows()