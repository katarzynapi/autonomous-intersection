import cv2
def drawNewCircle(i, j, image):
    cv2.circle(image, (i, j), 5, (0, 0, 255), 15)
    cv2.imshow('image', image)
    cv2.waitKey(100)

def drawNewLine(start_points, end_points, width, image):
    for s, e in zip(start_points, end_points):
        image = cv2.line(image, s, e, (0, 0, 255), width)
    cv2.imshow('image', image)
    cv2.waitKey(1000)