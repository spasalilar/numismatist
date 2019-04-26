import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())



image = cv2.imread(args["image"])
output = image.copy()

gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
#cv2.imshow("gray", gray)

gray = cv2.GaussianBlur(gray, (3, 3), 0)
#cv2.imshow("Blurred", gray)

gray = cv2.medianBlur(gray,5)

edged = cv2.Canny(gray, 50, 200, 10)
#cv2.imshow("Canny", edged)


gray = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
            cv2.THRESH_BINARY,11,3.5)
#cv2.imshow("Threshed", gray)

    
kernel = np.ones((1,2,1,5),np.uint8)
gray = cv2.erode(gray,kernel,iterations = 1)


# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20, param1=3,
                                                            param2=65,
                                                            minRadius=1,
                                                            maxRadius=80)
 
# ensure at least some circles were found
if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    x=0
    y=0
    r=0
    coin_number = 0
    total_number = []
    radius_of_circles = []
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        coin_number += 1
        total_number.append(coin_number)
        coin_str = str(coin_number)
        print ('Coin number:' + coin_str)
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        print ("Column Number: ")
        print (x)
        print ("Row Number: ")
        print (y)
        print ("Radius is: ")
        print (r)
        radius_of_circles.append(r)

    print('Total coins: ' + str(total_number))

    # plotting the points 
plt.plot(total_number, radius_of_circles, 'ro') 
# naming the x axis 
plt.xlabel('number of coin') 
# naming the y axis 
plt.ylabel('radius') 
  
# function to show the plot 
plt.show() 

# show the output image
cv2.imshow("output", np.hstack([output]))
cv2.waitKey(0)
