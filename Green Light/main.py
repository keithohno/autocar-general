import cv2
import numpy as np
kernel_size = 5      #for guassian filter

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
    mask = cv2.inRange(hsv, (40, 40, 40), (70, 255, 255))

    kernel = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(erosion, cv2.MORPH_OPEN, kernel)

    #contour
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # calculate Area
    for c in contours:
        #area from contours
        area = cv2.contourArea(c)

        #calculated area
        (x, y), radius = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        radius = int(radius)
        area2 = 3.14 * radius * radius

        x, y, w, h = cv2.boundingRect(c)
        areaRect = (int(w) * int(h))

        #compare areas - if similar, ping
        if area > 300 and area / area2 > 0.6:
            img = cv2.circle(image, center, radius, (255, 0, 0), 2)

            cv2.putText(img, 'Area: ' + str(area),
                        center,
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 0))
            if area/areaRect > 0.25:
                # draw a green rectangle to visualize the bounding rect
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    if ret == 1:

        #display frame
        cv2.imshow('Image', image)
        cv2.imshow('Frame', mask)

        #press q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    else:
        break

vid.release()
cv2.destroyAllWindows()




