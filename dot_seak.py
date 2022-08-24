from re import I
from turtle import Turtle
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

def file_read():
    #解析ファイル読み込み
    fTyp = [("Data file","*")]
    iDir =os.path.abspath(os.path.dirname(__file__))
    file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir)
    return(file_name)

def Contours(img_gray):

    labels,contours = cv2.findContours(img_gray,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    Areas = []
    Diameters = []
    Density = []



def none(x):
    pass

def Trackbar():
    #閾値変化トラックバー
    cv2.namedWindow("Threshold")
    cv2.resizeWindow("Threshold",640,240)
    cv2.createTrackbar("Low","Threshold",100,255,none)
    cv2.createTrackbar("High","Threshold",255,255,none)
    cv2.createTrackbar("open","Threshold",2,5,none)


#GUI展開
#root = tkinter.Tk()
#root.title("Dot Searcher")
#root.geometry("400x300")

#画像のグレースケール
path = file_read()
file_name,ext = os.path.splitext(os.path.basename(path))
kernel = np.ones((2,2),np.uint8)

Trackbar()

img = cv2.imread(path)
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#img_blur = cv2.GaussianBlur(imgGray,(5,5),0)
imgContour = img.copy()


"""
    画像形式
    グレースケールと二値化画像
    
    二値化画像によりナンバリング，エッジ，直径，面積，密度を求める
    グレースケールによりドットの高さを求める>>高さの最大値の入力が必須
    #高さと直径より楕円体，円柱近似による体積を計算
    
    >_<グレースケールを表示してエッジの閾値を選択>_<

    ナンバリング，エッジ，直径，高さ，面積，密度を.xlsxに出力
    ナンバリング画像を出力したい!!!
"""


while True:
    imgContour = img.copy()
    th_low = cv2.getTrackbarPos("Low","Threshold")
    th_high = cv2.getTrackbarPos("High","Threshold")
    hanpuku = cv2.getTrackbarPos("open","Threshold")

    img_bit = cv2.inRange(img_gray,th_low,th_high)
    opening = cv2.morphologyEx(img_bit,cv2.MORPH_OPEN,kernel,iterations=hanpuku)
    
    stack = np.hstack([img_gray,img_bit,opening])

    cv2.namedWindow("Horizontal Stacking",cv2.WINDOW_NORMAL)
    cv2.imshow("Horizontal Stacking",stack)
    cv2.imshow("contours",imgContour)

    if cv2.waitKey(1) == 13: #Enter key
        break
