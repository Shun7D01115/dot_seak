from cmath import pi
from pickletools import uint8
from re import I
from turtle import Turtle, width
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

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

#解析ファイル読み込み
def file_read():
    #解析ファイル読み込み
    fTyp = [("Data file","*")]
    iDir =os.path.abspath(os.path.dirname(__file__))
    file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir)
    return(file_name)


def ImgData(img_gray):
    height,width = img_gray.shape[0],img_gray.shape[1]
    all_areas = height * width
    return(height,width,all_areas)

#各ドット情報格納
def GetContours(contours,img_gray,img_bit,img_height,img_width):
    Num = []
    Areas_pixel = []
    Areas_calculate = []
    #Diameters = []
    Long_axis = []
    Short_axis = []
    Density = []
    Height = []
    Volume = []

    mask_base = np.zeros((img_height,img_width),np.uint8)
    mask_base = cv2.threshold(mask_base,100,255,cv2.THRESH_BINARY)

    for i in range(0,len(contours)):
        Areas_pixel[i] = cv2.contourArea(contours)
        Num[i] = i + 1
        rect = contours[i]
        x, y, w, h = cv2.boundingRect(rect)

        if w > h:
            Long_axis[i] = w
            Short_axis[i] = h
        else:
            Long_axis[i] = h
            Short_axis[i] = w
        
        Areas_calculate[i] = np.pi * w * h * 4
        mask = cv2.drawContours(mask_base,contours,-1,color=255,thickness=2)
        #マスク内のエリアでの最小値を取得，高さを推定する．

def none(x):
    pass

#トラックバーUI
def Trackbar():
    #閾値変化トラックバー
    cv2.namedWindow("Threshold")
    cv2.resizeWindow("Threshold",640,240)
    cv2.createTrackbar("Gaussian","Threshold",7,100,none)
    cv2.createTrackbar("Threshold","Threshold",2,5,none)

#トラックバーの値
def Adaptive():
    gaussian = cv2.getTrackbarPos("Gaussian","Threshold")
    threshold = cv2.getTrackbarPos("Threshold","Threshold")
    blocksize = 2 * gaussian + 3
    return(threshold,blocksize)

#画像のグレースケール
path = file_read()
file_name,ext = os.path.splitext(os.path.basename(path))

#トラックバー描画
Trackbar()

#画像ファイル読み込み
img = cv2.imread(path)
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
openkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
img_gray = cv2.morphologyEx(img_gray,cv2.MORPH_OPEN,openkernel)
kernel = np.ones((5,5),np.uint8)
img_copy = img.copy()

#画像の反復処理
while True:

    img_copy = img.copy()

    if cv2.waitKey(1) == 13: #Enter key
        break

    #閾値等の変化
    threshold,blocksize = Adaptive()
    img_bit = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,blocksize,threshold)
    contours, _ = cv2.findContours(img_bit,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    #エッジ等の描画処理
    for i in range(0,len(contours)):
        if len(contours[i]) > 0:

            #remove small objects
            if cv2.contourArea(contours[i]) < 200:
                continue

            rect = contours[i]
            x,y,w,h = cv2.boundingRect(rect)
            cv2.polylines(img_copy,contours[i],True,(255,0,0),1)
            cv2.rectangle(img_copy,(x,y),(x+w,y+h),(0,255,0),1)

    cv2.imshow("img_th",img_copy)

img_height,img_width,all_areas = ImgData(img_gray)
labels  = cv2.connectedComponentsWithStats(img_bit)
data = np.delete(labels[2],0,0)
center = np.delete(labels[3],0,0)

#画像処理の結果
for i in range(0,len(contours)):
    if len(contours[i])>0:

        if cv2.contourArea(contours[i]) < 200:
            continue

    rect = contours[i]
    x,y,w,h = cv2.boundingRect(rect)
    cv2.polylines(img_copy,contours[i],True,(255,0,0),1)
    cv2.rectangle(img_copy,(x,y),(x+w,y+h),(0,255,0),1)
    text_x = int(round(x+w/3))
    text_y = int(round(y+h/2))
    cv2.putText(img_copy,str(i+1), (text_x,text_y),cv2.FONT_HERSHEY_PLAIN,1,(0,120,200))
    
cv2.imshow("test",img_bit)
    




cv2.imshow("img_exp",img_copy)
cv2.waitKey()
cv2.destroyAllWindows()
