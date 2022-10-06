from cmath import pi
from pickletools import uint8
from re import I
from turtle import Turtle, width
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import random
import json

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

#draw black excepting contours
img_height,img_width,all_areas=Imgdata(img_gray)
base_img = np.zeros((img_height,img_width),np.uint8)
mask = base_img
_,mask = cv2.threshold(mask,100,255,cv2.THRESH_BINARY)
cv2.fillPoly(mask,contours,255)

#get pixel info
nlabels,labels,stats,_=cv2.connectedComponentsWithStats(mask)
