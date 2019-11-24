import cv2
def drawNewCircle(i, j, image):
    cv2.circle(image, (i, j), 5, (0, 0, 255), 15)
    cv2.imshow('image', image)
    cv2.waitKey(100)

def drawNewLine(start_point, end_point, width, image):
    image = cv2.line(image, start_point, end_point, (0, 0, 255), width)
    cv2.imshow('image', image)
    cv2.waitKey(3000)