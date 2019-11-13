import cv2
def drawNewCircle(i, j, image):
    cv2.circle(image, (i, j), 5, (40, 40, 40), 3)
    cv2.imshow('image', image)
    cv2.waitKey(1000)

def drawNewLine(start_point, end_point, width, image):
    image = cv2.line(image, start_point, end_point, (0, 0, 0), 7)
    cv2.imshow('image', image)
    cv2.waitKey(100)