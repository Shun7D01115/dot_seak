from cProfile import label
from cmath import pi
from pickletools import uint8
from re import I
from turtle import Turtle, color, width
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import random
import json
import csv

import os,tkinter,tkinter.filedialog,tkinter.messagebox
from tkinter import messagebox

#############################################################################################
#file road
def File_read():
    fTyp = [("Data file","*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir)
    return(file_name)

#pixcel data
def Imgdata(img_gray):
    height,width = img_gray.shape[0],img_gray.shape[1]
    all_areas = height * width
    return(height,width,all_areas)

def none(x):
    pass

#Trackbar UI
def Trackbar():
    cv2.namedWindow("Threshold")
    cv2.resizeWindow("Threshold",640,240)
    cv2.createTrackbar("Gaussian","Threshold",7,100,none)
    cv2.createTrackbar("Threshold","Threshold",2,5,none)

#Trackbar UI 
def Adaptive():
    gaussian = cv2.getTrackbarPos("Gaussian","Threshold")
    threshold = cv2.getTrackbarPos("Threshold","Threshold")
    blocksize = 2 * gaussian + 3
    return(threshold,blocksize)

#############################################################################################
#get path
path = File_read()
file_name,text = os.path.splitext(os.path.basename(path))

#show trackbar
Trackbar()

#RGB to GRAY
img = cv2.imread(path)
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

openkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
img_gray = cv2.morphologyEx(img_gray,cv2.MORPH_OPEN,openkernel)
kernel = np.ones((5,5),np.uint8)
img_copy = img.copy()

while True:
    #Threshold valiable
    threshold,blocksize = Adaptive()
    img_bit = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,blocksize,threshold)
    contours , _ = cv2.findContours(img_bit,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    #remove enough small,big dots
    contours = list(filter(lambda small:cv2.contourArea(small)>200,contours))
    contours = list(filter(lambda big:cv2.contourArea(big)<6000,contours))

    cv2.drawContours(img_copy,contours,-1,color=(255,0,0),thickness=1)
    cv2.imshow("Threshold img",img_copy)
    if cv2.waitKey(1) == 13: #Enter Key
        break
    img_copy = img.copy()

cv2.destroyAllWindows()
img_result = img_copy

#draw black, excepting contours
img_height,img_width,all_areas=Imgdata(img_gray)
base_img = np.zeros((img_height,img_width),np.uint8)
mask = base_img
_,mask = cv2.threshold(mask,100,255,cv2.THRESH_BINARY)
cv2.fillPoly(mask,contours,255)

#get pixel info
nlabels,labels,stats,_=cv2.connectedComponentsWithStats(mask)

#############################################################################################

Num = []
Long_axis = []
Short_axis = []
Height = []
Volume_pixcel = []
Volume_cylinder = []
Volume_cone = []
Areas_pixcel = []
Areas_calculate = []
Density = 0
white = 255
############################################
pixcel_length = 1
############################################

for i in range(1, nlabels):
    #dot_mask = base_mask
    dot_height = 0
    dot_volume = 0
    area_count = 0
    #input Num
    Num.append(i)
    #input axis
    if stats[i][2] > stats[i][3]:
        Long_axis.append(stats[i][2])
        Short_axis.append(stats[i][3])
    else:
        Long_axis.append(stats[i][3])
        Short_axis.append(stats[i][2])
    #every dot data
    x = stats[i-1][0]
    y = stats[i-1][1]
    w = stats[i-1][2]
    h = stats[i-1][3]
    for j in range(0, w):
        for k in range(0, h):
            if labels[x+j][y+k] == i-1:
                dot_volume += img_gray[x+j][y+k]
                area_count += 1
                if dot_height < img_gray[x+j][y+k]:
                    dot_height = img_gray[x+j][y+k]
    #input height,volume
    dot_volume = dot_volume*pixcel_length*pixcel_length
    area_count = area_count*pixcel_length*pixcel_length
    Height.append(dot_height)
    Volume_pixcel.append(dot_volume)
    Areas_pixcel.append(area_count)
    Areas_calculate.append(np.pi*w*h)


#Data = np.vstack((Num,Long_axis,Short_axis,Height,Volume_pixcel,Areas_pixcel,Areas_calculate))
#D = Data.T
# = open("out.csv","w",newline="")
#writer = csv.writer(f)
#writer.writerows(D)
#f.close()

for i, row in enumerate(stats):
    print(f"label {i}")
    print(f"* topleft: ({row[cv2.CC_STAT_LEFT]}, {row[cv2.CC_STAT_TOP]})")
    print(f"* size: ({row[cv2.CC_STAT_WIDTH]}, {row[cv2.CC_STAT_HEIGHT]})")
    print(f"* area: {row[cv2.CC_STAT_AREA]}")
