import cv2
import random

def drawNewCircle(agents, image):
    for a in agents:
        print([i.getCoords() for i in a.location])
        for c in a.location:
            image = cv2.circle(image, (c.getCoords()), 5, a.color, 15)
    cv2.imshow('image', image)
    cv2.waitKey(500)

#def drawNewLine(start_points, end_points, width, image, color):
def drawNewLine(agents, width, image):
    for a in agents:
        print([i.getCoords() for i in a.location])
        image = cv2.line(image, a.location[0].getCoords(), a.location[-1].getCoords(), a.color, width)
    #for s, e, c in zip(start_points, end_points, color):
        #image = cv2.line(image, s, e, c, width)
    cv2.imshow('image', image)
    cv2.waitKey(500)