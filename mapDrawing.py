import cv2
import random
import enums

def drawNewCircle(agents, image, lights, obstacles):
    if obstacles:
        for o in obstacles:
            obstacle_loc = o.location.getCoords()
            print(obstacle_loc)
            image = cv2.circle(image, (obstacle_loc), 5, (0, 0, 0), 15)
    if lights:
        r0, c0 = lights[0].location.getCoords()
        r1, c1 = lights[1].location.getCoords()
        r2, c2 = lights[4].location.getCoords()
        r3, c3 = lights[5].location.getCoords()
        if lights[0].colour == enums.Colour.GREEN and lights[2].colour == enums.Colour.RED and lights[4].colour == enums.Colour.RED and lights[6].colour == enums.Colour.RED:
            image = cv2.circle(image, (r0-10,c0-30), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r1+10,c1+30), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r2-80,c2+10), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r3+80,c3-10), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r0-37,c0-40), 5, (0, 255, 0), 15)
            image = cv2.circle(image, (r1+37,c1+40), 5, (0, 255, 0), 15)
            image = cv2.circle(image, (r2-95,c2+35), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r3+95,c3-35), 5, (0, 0, 255), 15)
        elif lights[0].colour == enums.Colour.RED and lights[2].colour == enums.Colour.GREEN and lights[4].colour == enums.Colour.RED and lights[6].colour == enums.Colour.RED:
            image = cv2.circle(image, (r0-10,c0-30), 5, (0, 255, 0), 15)
            image = cv2.circle(image, (r1+10,c1+30), 5, (0, 255, 0), 15)
            image = cv2.circle(image, (r2-80,c2+10), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r3+80,c3-10), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r0-37,c0-40), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r1+37,c1+40), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r2-95,c2+35), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r3+95,c3-35), 5, (0, 0, 255), 15)
        elif lights[0].colour == enums.Colour.RED and lights[2].colour == enums.Colour.RED and lights[4].colour == enums.Colour.GREEN and lights[6].colour == enums.Colour.RED:
            image = cv2.circle(image, (r0-10,c0-30), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r1+10,c1+30), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r2-80,c2+10), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r3+80,c3-10), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r0-37,c0-40), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r1+37,c1+40), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r2-95,c2+35), 5, (0, 255, 0), 15)
            image = cv2.circle(image, (r3+95,c3-35), 5, (0, 255, 0), 15)
        elif lights[0].colour == enums.Colour.RED and lights[2].colour == enums.Colour.RED and lights[4].colour == enums.Colour.RED and lights[6].colour == enums.Colour.GREEN:
            image = cv2.circle(image, (r0-10,c0-30), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r1+10,c1+30), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r2-80,c2+10), 5, (0, 255, 0), 15)
            image = cv2.circle(image, (r3+80,c3-10), 5, (0, 255, 0), 15)
            image = cv2.circle(image, (r0-37,c0-40), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r1+37,c1+40), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r2-95,c2+35), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r3+95,c3-35), 5, (0, 0, 255), 15)
        elif lights[0].colour == enums.Colour.RED and lights[2].colour == enums.Colour.RED and lights[4].colour == enums.Colour.RED and lights[6].colour == enums.Colour.RED:
            image = cv2.circle(image, (r0-10,c0-30), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r1+10,c1+30), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r2-80,c2+10), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r3+80,c3-10), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r0-37,c0-40), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r1+37,c1+40), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r2-95,c2+35), 5, (0, 0, 255), 15)
            image = cv2.circle(image, (r3+95,c3-35), 5, (0, 0, 255), 15)
    for a in agents:
        print([i.getCoords() for i in a.location])
        for c in a.location:
            image = cv2.circle(image, (c.getCoords()), 5, a.color, 5)
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