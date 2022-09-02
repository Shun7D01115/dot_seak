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
画像選択
ドット探索
閾値機能
ドットデータの書き出し
(
    ナンバリング，直径，高さ，面積，体積(円柱，円錐etc)，平均高さ，平均直径，密度
    分布を作るための何か(高さ度数分布，直径度数分布，円柱体積分布)
)
"""

"""
    画像形式
    グレースケールと二値化画像
    
    二値化画像によりナンバリング，エッジ，直径，面積，密度を求める
    グレースケールによりドットの高さを求める>>高さの最大値の入力が必須
    #高さと直径より楕円体，円柱近似による体積を計算

    ナンバリング，エッジ，直径，高さ，面積，密度を.xlsxに出力
    ナンバリング画像を出力したい!!!
"""

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

def GetContours(contours):
    Areas = []
    Diameters = []
    Density = []



def none(x):
    pass

def Trackbar():
    #閾値変化トラックバー
    cv2.namedWindow("Threshold")
    cv2.resizeWindow("Threshold",640,240)
    cv2.createTrackbar("Gaussian","Threshold",7,100,none)
    cv2.createTrackbar("Threshold","Threshold",2,5,none)

def Adaptive():
    gaussian = cv2.getTrackbarPos("Gaussian","Threshold")
    threshold = cv2.getTrackbarPos("Threshold","Threshold")
    blocksize = 2 * gaussian + 3
    return(threshold,blocksize)

#画像のグレースケール
path = file_read()
file_name,ext = os.path.splitext(os.path.basename(path))

Trackbar()

img = cv2.imread(path)
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
openkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
img_gray = cv2.morphologyEx(img_gray,cv2.MORPH_OPEN,openkernel)
kernel = np.ones((5,5),np.uint8)
img_copy = img.copy()

while True:

    img_copy = img.copy()

    if cv2.waitKey(1) == 13: #Enter key
        break

    threshold,blocksize = Adaptive()
    img_bit = cv2.adaptiveThreshold(img_gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,blocksize,threshold)
    contours,hierarchy = cv2.findContours(img_bit,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

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
n = labels[0]-1
print(n)
data = np.delete(labels[2],0,0)
center = np.delete(labels[3],0,0)

#hight,width,all_areas = ImgData(img_gray)

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
    #area = cv2.contourArea(contours[i])
    #area = area/all_areas
    #PixcelAreas.append(area)
    #CulAreas.append(pi()*w*h/4)





cv2.imshow("img_exp",img_copy)
cv2.waitKey()
cv2.destroyAllWindows()
