# import the necessary packages
from transform import four_point_transform
import numpy as np
import argparse
import cv2

#This will display all the available mouse click events  
events = [i for i in dir(cv2) if 'EVENT' in i]
print(events)

#This variable we use to store the pixel location
refPt = []

#click event function
def click_event(event, x, y, flags, param):
	if event == cv2.EVENT_LBUTTONDOWN:
		print(x,",",y)
		refPt.append([x,y])
		font = cv2.FONT_HERSHEY_SIMPLEX
		strXY = str(x)+", "+str(y)
		cv2.putText(img, strXY, (x,y), font, 0.5, (255,255,0), 2)
		cv2.imshow("image", img)
		if len(refPt) == 4:
			pts = np.array(refPt)
			warped = four_point_transform(img, pts)
			cv2.imshow("Warped", warped)

img = cv2.imread("images/example_01.png")
cv2.imshow("image", img)

cv2.setMouseCallback("image", click_event)

cv2.waitKey(0)
cv2.destroyAllWindows()