from pickletools import uint8
from re import I
from turtle import Turtle
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math

import os
import tkinter
import tkinter.filedialog
import tkinter.messagebox
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
    
    >_<グレースケールを表示してエッジの閾値を選択>_<

    ナンバリング，エッジ，直径，高さ，面積，密度を.xlsxに出力
    ナンバリング画像を出力したい!!!
"""


def file_read():
    #解析ファイル読み込み
    fTyp = [("Data file", "*")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    file_name = tkinter.filedialog.askopenfilename(
        filetypes=fTyp, initialdir=iDir)
    return (file_name)


def Contours(img_gray):

    labels, contours = cv2.findContours(
        img_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    Areas = []
    Diameters = []
    Density = []


def none(x):
    pass


def Trackbar():
    #閾値変化トラックバー
    cv2.namedWindow("Threshold")
    cv2.resizeWindow("Threshold", 640, 240)
    cv2.createTrackbar("Low", "Threshold", 100, 255, none)


#画像のグレースケール
path = file_read()
file_name, ext = os.path.splitext(os.path.basename(path))

Trackbar()


img = cv2.imread(path)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
kernel = np.ones((5, 5), np.uint8)
img_copy = img.copy()

while True:

    img_copy = img.copy()

    if cv2.waitKey(1) == 13:
        break

    threshold = cv2.getTrackbarPos("Low", "Threshold")
    ret, img_bit = cv2.threshold(img_gray, threshold, 255, cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(
        img_bit, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    #th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

    for i in range(0, len(contours)):
        if len(contours[i]) > 0:
            if cv2.contourArea(contours[i]) < 500:
                continue
            rect = contours[i]
            x, y, w, h = cv2.boundingRect(rect)
            cv2.polylines(img_copy, contours[i], True, (255, 0, 0), 1)
            cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 1)

    cv2.imshow("img_th", img_copy)

##branchできてるかな?


cv2.waitKey()
cv2.destroyAllWindows()
