import cv2
import numpy as np
import math
kernel_size = 7      #for guassian filter

#function to calculate distance between 2 points
def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist

vid = cv2.VideoCapture(1)
if(vid.isOpened() == False):
    print("Error opening camera")

while(vid.isOpened):
    #capture frame by frame
    ret, image = vid.read()

    # filter with guassian blur
    blur = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)

    #convert to HSV - mask for green
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,(3, 125, 50), (15, 255, 255) )

    #decrease noise
    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)      #opening = erosion + dilation
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)     #close small holes, opposite of opening

    #canny edge filter
    edges = cv2.Canny(closing, 0, 200)

    #contour
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for c in contours:
        # get number of vertices
        vertices = cv2.approxPolyDP(c, 0.1 * cv2.arcLength(c, True), True)
        print(vertices)
        print("-----------------------")
        '''
        if len(vertices) == 3:
            topLine = calculateDistance(vertices[0][0][0], vertices[0][0][1], vertices[3][0][0], vertices[3][0][1])
            print(topLine)
            botLine = calculateDistance(vertices[2][0][0], vertices[2][0][1], vertices[1][0][0], vertices[1][0][1])
            print(botLine)
            print("--------------------")
            ratio = topLine/botLine
        '''
        #calculate area of rectangle
        x, y, w, h = cv2.boundingRect(c)
        area = w * h
        #Distance filter, only ping if rectangle area > 3000 and is triangle
        if area > 3000 and len(vertices) == 3:
            cv2.rectangle(image, (x,y), (x+w, y+h), (0, 255, 0), 2)
            cv2.drawContours(image, [c], 0, (0, 255, 0), 2)

    if ret == 1:

        #display frames
        cv2.imshow('Image', image)
        cv2.imshow('Edges', edges)
        cv2.imshow('Opening', closing)

        #press q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    else:
        break

vid.release()
cv2.destroyAllWindows()




