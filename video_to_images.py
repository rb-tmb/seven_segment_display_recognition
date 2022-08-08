import cv2
import os

#Function to get images from video
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite(os.path.join(img_path,"image"+str(count+1)+".jpg"), image)    # save frame as JPG/PNG file
    else:
        print("Read all the Frames")
    return hasFrames

#folder paths
vid_path = 'path to video'
img_path = 'path to image'
#create the image folder if it doesn't exit
if not os.path.exists(img_path):
    os.makedirs(img_path)

vidcap = cv2.VideoCapture('path to video')

sec = 0 #for how many seconds do you want to capture
frameRate = 0.5 #//it will capture image in each 0.5 second
count=0
success = getFrame(sec)
while success:
    count = count + 1
    sec = sec + frameRate
    sec = round(sec, 2)
    success = getFrame(sec)
    
print("No of Images: ",count)