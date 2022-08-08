import cv2
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
from imutils.perspective import four_point_transform
from imutils import contours
import imutils

DIGITS_LOOKUP = {
	(1, 1, 1, 0, 1, 1, 1): 0,
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 0, 1): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
    (1, 1, 1, 0, 0, 1, 0): 7, #Sometimes 7 appears like this in some displays
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}

img_path = 'path to images'

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder,filename),0)
        if img is not None:
            images.append(img)
    return images

def convert(list):
    res = sum(d * 10**i for i, d in enumerate(list[::-1]))
      
    return(res)

images = load_images_from_folder(img_path)#Load all the images
print("No of Images in the folder: ",len(images))
readings = []
for image in images:
    
    crop_img = image[330:400, 925:1075]#Hard coded - Find the right ROI

    ret,thresh = cv2.threshold(crop_img, 30, 255,cv2.THRESH_BINARY_INV) #adjust the values to get just the numbers

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 5))
    dilate = cv2.dilate(thresh, kernel, iterations=1)
    thresh = cv2.morphologyEx(dilate, cv2.MORPH_OPEN, kernel) #The numbers should appear continuous

    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    digitCnts = []
    ws = []
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        # if the contour is sufficiently large, it must be a digit
        if w >= 5 and (h >= 30 and h <= 60): #again these values are hardcoded find the right values by printing x,y,w,h
            digitCnts.append(c)
            ws.append(w)
    digitCnts = contours.sort_contours(digitCnts,method="left-to-right")[0]
    digits = []

    for c in digitCnts:
        # extract the digit ROI
        (x, y, w, h) = cv2.boundingRect(c)
        if(w<10): #This is to compensate for 1 since it's width will be small we need to pad it
            w_temp = max(ws)
            x_temp = x-(w_temp-w)
            x = x_temp
            w = w_temp
        roi = thresh[y:y + h, x:x + w]
        # compute the width and height of each of the 7 segments
        # we are going to examine
        (roiH, roiW) = roi.shape
        (dW, dH) = (int(roiW * 0.25), int(roiH * 0.15))
        dHC = int(roiH * 0.05)
        # define the set of 7 segments
        segments = [
            ((0, 0), (w, dH)),	# top
            ((0, 0), (dW, h // 2)),	# top-left
            ((w - dW, 0), (w, h // 2)),	# top-right
            ((0, (h // 2) - dHC) , (w, (h // 2) + dHC)), # center
            ((0, h // 2), (dW, h)),	# bottom-left
            ((w - dW, h // 2), (w, h)),	# bottom-right
            ((0, h - dH), (w, h))	# bottom
        ]
        on = [0] * len(segments)

        for (i, ((xA, yA), (xB, yB))) in enumerate(segments):
            segROI = roi[yA:yB, xA:xB]
            total = cv2.countNonZero(segROI)
            area = (xB - xA) * (yB - yA)
            if total / float(area) > 0.5:
                on[i]= 1
        # lookup the digit and draw it on the image
        try:
            cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            digit = DIGITS_LOOKUP[tuple(on)]
            digits.append(digit)
            cv2.rectangle(crop_img, (x, y), (x + w, y + h), (0, 255, 0), 1)
            cv2.putText(crop_img, str(digit), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
        except:
            print("Problem Occured during analyzing digit no: ",len(digits)+1)
            print(tuple(on))
            plt.imshow(crop_img) #or use cv2.imshow() & cv2.waitKey(0)
            plt.show()
        
    #print("Reading is: "+u"{}.{}{}{} mA".format(*digits)) #Adjust according to the displayed values
    #print("Reading is: ",digits)
    if len(digits) == 4:
        val = convert(digits) #Convert it to the right values before saving it.
        readings.append(val/1000)
        
print("No of Readings: ",len(readings)) #TO check if no of images and readings match
col1 = "S.No"
col2 = "Readings"
list1 = np.arange(1, len(readings)+1, 1)
data = pd.DataFrame({col1:list1,col2:readings})
data.to_excel('exp_readings.xlsx', sheet_name='sheet1', index=False) #import to excel
#Plot the readings
plt.plot(readings)
plt.title("Current Drawn vs Time")
plt.xlabel('Time (in sec)')
plt.ylabel('Current(in A)')
plt.show()