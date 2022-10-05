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

"""
/必要な機能/
    二値化画像によりナンバリング，エッジ，直径，面積，密度を求める
    グレースケールによりドットの高さを求める>>高さの最大値の入力が必須
    #高さと直径より楕円体，円柱近似による体積を計算
    ナンバリング，エッジ，直径，高さ，面積，密度,taisekiを.xlsxに出力
    ナンバリング画像を出力したい!!!
"""

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

def remove_object(img_bit,lower=None,upper=None):
    nlabels,labels,stats,centroids = cv2.connectedComponentsWithStats(img_bit)

    sizes = stats[1:, -1]
    _img = np.zeros((labels.shape))

    for i in range(1,nlabels):
        if(lower is not None) and (upper is not None):
            _img[labels == i] = 255
        elif(lower is not None) and (upper is None):
            if lower < sizes[i-1]:
                _img[labels == i] = 255
        elif(lower is None) and (upper is None):
            if sizes[i-1] < upper:
                _img[labels == i] = 255
    
    return _img



def Expdata(nlabels,labels,contours,num,L_axis,S_axis,img_height,img_width,all_areas):
    Num = []
    Long_axis = []
    Short_axis = []
    Height = []
    Volume = []
    Density = []
    Areas_pixcel = []
    Areas_calculate = []
    Flag = 1

    for i in range(1,nlabels):
        if len(contours[i]) > 0:
            if cv2.contourArea(contours[i]) < 200:
                continue

        rect = contours[i]
        x, y, w, h = cv2.boundingRect(rect)
        if w > h:
            Long_axis.append(w)
            Short_axis.append(h)
        else:
            Long_axis.append(h)
            Short_axis.append(w)
        Num.append(Flag)

        #make contours mask
        base_img = np.zeros((img_height, img_width, 1))
        mask = base_img
        cv2.fillPoly(mask,contours[135],255)
        #輪郭のみが検出されているため，塗りつぶし処理をもう一度する
        
        contours_sub , _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(mask,contours_sub,-1,color=255,thickness=-1)

        Flag += 1





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
    img_copy = img.copy()
    if cv2.waitKey(1) == 13: #Enter Key
        break

    #Threshold valiable
    threshold,blocksize = Adaptive()
    img_bit = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,blocksize,threshold)
    contours , _ = cv2.findContours(img_bit,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    #edge etc... processor
    for i in range(0,len(contours)):
        #remove small objects
        if len(contours[i]) > 0:
            if cv2.contourArea(contours[i]) < 200:
                continue
            
            #show green and blue edges
            rect = contours[i]
            x,y,w,h = cv2.boundingRect(rect)
            cv2.polylines(img_copy,contours[i],True,(255,0,0),1)
            cv2.rectangle(img_copy,(x,y),(x+w,y+h),(0,255,0),1)

    cv2.imshow("Threshold img",img_copy)

cv2.destroyAllWindows()

img_result = img_copy

for i in range(0,len(contours)):
    if len(contours[i]) > 0:
        if cv2.contourArea(contours[i]) < 200:
            continue
#除外したものもcontoursとしては残っているためその部分の改造が必須
    rect = contours[i]
    x,y,w,h = cv2.boundingRect(rect)
    img_result = cv2.polylines(img_copy,contours[i],True,(255,0,0),1)
    img_result = cv2.rectangle(img_copy,(x,y),(x+w,y+h),(0,255,0),1)
    text_x = int(round(x+w/3))
    text_y = int(round(y+h/2))
    img_result = cv2.putText(img_copy,str(i+1),(text_x,text_y),cv2.FONT_HERSHEY_PLAIN,1,(0,120,200))

#show result
cv2.imshow("Result",img_result)
cv2.waitKey(0)
cv2.destroyAllWindows()

#get pixcel info
img_height,img_width,all_areas = Imgdata(img_gray)
nlabels, labels, stats, _ = cv2.connectedComponentsWithStats(img_bit)


base_img = np.zeros((img_height, img_width, 3))
mask = base_img
mask[labels == 135] = (255,255,255)
cv2.imshow("show",mask)
cv2.waitKey(0)
cv2.destroyAllWindows()
