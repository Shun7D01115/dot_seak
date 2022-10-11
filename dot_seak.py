from cProfile import label
from cmath import e, pi
from distutils.cmd import Command
from pickletools import uint8
from re import I
from turtle import Turtle, color, width
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
import random
import csv
import re

import os
import tkinter
from tkinter import StringVar, messagebox
from tkinter import filedialog
from tkinter import ttk


#############################################################################################
#ボタンがクリックされたら実行
def gui():
    file_name = ""
    img_length = ""
    max_height = ""

    def file_select():
        nonlocal file_name
        fTyp = [("Image File", "*.png *.jpg *.jpeg *.tif *.bmp"), ("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg"), ("Tiff", "*.tif"), ("Bitmap", "*.bmp"), ("すべて", "*")]  # 拡張子の選択
        iDir = os.path.abspath(os.path.dirname(__file__))
        file_name = tkinter.filedialog.askopenfilename(
            filetypes=fTyp, initialdir=iDir)
        input_box1.insert(tkinter.END, file_name)

    def isnumber(s):
        try:
            float(s)
        except:
            return False
        else:
            return True

    def ok_click():
        nonlocal img_length
        nonlocal max_height
        if not os.path.isfile(file_name):
            messagebox.showerror("エラー","画像アドレスが間違っています")
            return
        if not (isnumber(input_box2.get()) and isnumber(input_box3.get())):
            messagebox.showerror("エラー","数字を入力してください")
            return

        img_length = float(input_box2.get())
        max_height = float(input_box3.get())
        root.destroy()

    def close_click():
        if tkinter.messagebox.askokcancel(" ","プログラムを終了しますか？"):
            root.destroy()
            quit()

    root = tkinter.Tk()

    root.title("Information")
    root.geometry("360x240")

    root.protocol("WM_DELETE_WINDOW",close_click)

    #入力欄の作成
    input_box1 = tkinter.Entry(width=40)
    input_box1.place(x=10, y=170)

    #ラベルの作成
    input_label = tkinter.Label(text="ファイル入力")
    input_label.place(x=10, y=140)

    #ボタンの作成
    button1 = tkinter.Button(text="参照", command=file_select)
    button1.place(x=260, y=167)

    button2 = tkinter.Button(text="OK", command=ok_click)
    button2.place(x=180, y=200)

    #img length
    input_box2 = tkinter.Entry(width=25)
    input_box2.place(x=10, y=40)
    input_label2 = tkinter.Label(text="AFM画像の長さ[μm]を入力してください")
    input_label2.place(x=10, y=10)
    #dot max height
    input_box3 = tkinter.Entry(width=25)
    input_box3.place(x=10, y=100)
    input_label3 = tkinter.Label(text="ドットの最大高さ[nm]を入力してください")
    input_label3.place(x=10, y=70)

    root.mainloop()
    return (file_name, img_length, max_height)

#pixcel data
def Imgdata(img_gray):
    height, width = img_gray.shape[0], img_gray.shape[1]
    all_areas = height * width
    return (height, width, all_areas)

def none(x):
    pass

#Trackbar UI
def Trackbar():
    cv2.namedWindow("Threshold")
    cv2.resizeWindow("Threshold", 640, 240)
    cv2.createTrackbar("Gaussian", "Threshold", 7, 100, none)
    cv2.createTrackbar("Threshold", "Threshold", 2, 30, none)

#Trackbar UI
def Adaptive():
    gaussian = cv2.getTrackbarPos("Gaussian", "Threshold")
    threshold = cv2.getTrackbarPos("Threshold", "Threshold")
    blocksize = 2 * gaussian + 3
    return (threshold, blocksize)

def outDir():
    dir_path = ""
    csv_name = "out.csv"
    img_name = "out.tif"
    def file_select():
        nonlocal dir_path
        iDir = os.path.abspath(os.path.dirname(__file__))
        dir_path = filedialog.askdirectory(initialdir=iDir)
        input_box1.insert(tkinter.END,dir_path)

    def ok_click():
        nonlocal csv_name
        nonlocal img_name
        img_name = input_box2.get()
        csv_name = input_box3.get()
        if not os.path.basename(csv_name):
            csv_name += ".csv"
        if not os.path.basename(img_name):
            img_name += ".tif"
        if not os.path.isdir(dir_path):
            messagebox.showerror("エラー", "ディレクトリが存在しません")
            return
        root.destroy()

    def close_click():
        if tkinter.messagebox.askokcancel(" ", "保存していません，プログラムを終了しますか？"):
            root.destroy()
            quit()

    root = tkinter.Tk()

    root.title("Output Directory")
    root.geometry("360x240")

    root.protocol("WM_DELETE_WINDOW", close_click)

    #入力欄の作成
    input_box1 = tkinter.Entry(width=40)
    input_box1.place(x=10, y=40)

    #ラベルの作成
    input_label = tkinter.Label(text="保存先を決定してください")
    input_label.place(x=10, y=10)

    #ボタンの作成
    button1 = tkinter.Button(text="参照", command=file_select)
    button1.place(x=260, y=37)

    #入力欄の作成
    input_box2 = tkinter.Entry(width=40)
    input_box2.place(x=10, y=110)

    #ラベルの作成
    input_label2 = tkinter.Label(text="解析結果の画像名を入力してください")
    input_label2.place(x=10, y=80)

    #入力欄の作成
    input_box3 = tkinter.Entry(width=40)
    input_box3.place(x=10, y=170)

    #ラベルの作成
    input_label3 = tkinter.Label(text="CSVファイル名を入力してください")
    input_label3.place(x=10, y=140)

    button2 = tkinter.Button(text="OK", command=ok_click)
    button2.place(x=180, y=210)

    root.mainloop()
    return(dir_path,csv_name,img_name)

#############################################################################################
#path,画像長さ，ドット最大高さ取得
path, img_length, max_height = gui()

#show trackbar
Trackbar()

#RGB to GRAY
img = cv2.imread(path)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

openkernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
img_gray = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, openkernel)
kernel = np.ones((5, 5), np.uint8)
img_copy = img.copy()

while True:
    #Threshold valiable
    threshold, blocksize = Adaptive()
    img_bit = cv2.adaptiveThreshold(
        img_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, blocksize, threshold)
    contours, _ = cv2.findContours(
        img_bit, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    #remove enough small,big dots
    contours = list(filter(lambda small:cv2.contourArea(small)>200,contours))
    contours = list(filter(lambda big: cv2.contourArea(big) < 6000, contours))

    cv2.drawContours(img_copy, contours, -1, color=(255, 0, 0), thickness=1)
    cv2.imshow("Threshold img", img_copy)
    if cv2.waitKey(1) == 13:  # Enter Key
        break
    if cv2.getWindowProperty("Threshold img",cv2.WND_PROP_AUTOSIZE) == -1:
        cv2.destroyAllWindows()
        exit()
    img_copy = img.copy()

cv2.destroyAllWindows()
img_result = img_copy

#draw black, excepting contours
img_height, img_width, all_areas = Imgdata(img_gray)
base_img = np.zeros((img_height, img_width), np.uint8)
mask = base_img
_, mask = cv2.threshold(mask, 100, 255, cv2.THRESH_BINARY)
cv2.fillPoly(mask, contours, 255)

#get pixel info
nlabels, labels, stats, _ = cv2.connectedComponentsWithStats(mask)


#############################################################################################
Num = []#
Long_axis = []#
Short_axis = []#
Height = []#
Volume_pixcel = []#
Volume_cylinder = []
Volume_cone = []
Areas_pixcel = []#
Areas_calculate = []#
Density = 0
white = 255
############################################
pixcel_length = 1000*int(img_length)/float(img_width)
height_dimless = int(max_height)/256.0
############################################

for i in range(1, nlabels):
    #dot_mask = base_mask
    dot_height = 0
    dot_volume = 0
    #input Num
    Num.append(i)
    #every dot data
    ########################################################
    #行列の向きの確認
    x = stats[i][cv2.CC_STAT_LEFT]
    y = stats[i][cv2.CC_STAT_TOP]
    w = stats[i][cv2.CC_STAT_WIDTH]
    h = stats[i][cv2.CC_STAT_HEIGHT]
    area = stats[i][cv2.CC_STAT_AREA]
    for j in range(0, w):
        for k in range(0, h):
            if i != labels[y+k][x+j]:
                continue
            dot_volume += img_gray[x+j][y+k]
            if dot_height >= img_gray[x+j][y+k]:
                continue
            dot_height = img_gray[x+j][y+k]
    #input axis
    w *= pixcel_length
    h *= pixcel_length
    if stats[i][cv2.CC_STAT_WIDTH] > stats[i][cv2.CC_STAT_HEIGHT]:
        Long_axis.append(w)
        Short_axis.append(h)
    else:
        Long_axis.append(h)
        Short_axis.append(w)
    #input height,volume
    dot_height *= height_dimless
    dot_volume = dot_volume*pixcel_length*pixcel_length
    area_count = area*pixcel_length*pixcel_length
    Volume_cylinder.append(dot_height*area_count)
    Height.append(dot_height)
    Volume_pixcel.append(dot_volume)
    Areas_pixcel.append(area)
    Areas_calculate.append(np.pi*w*h)

    img_result = cv2.polylines(img_result,contours[i-1],True,(255,0,0),1)
    img_result = cv2.rectangle(img_result,(x,y),(x+w,y+h),(0,255,0),1)
    text_x = int(round(x+2))
    text_y = int(round(y+10))
    img_result = cv2.putText(img_result,str(i+1),(text_x,text_y),cv2.FONT_HERSHEY_PLAIN,1,(0,255,255))

cv2.imshow("Result",img_result)
cv2.waitKey(0)
cv2.destroyAllWindows()

Title = ["Num","長軸","短軸","高さ","面積","円柱体積","体積(明度)"]
Data = np.vstack((Num, Long_axis, Short_axis, Height, Areas_pixcel, Volume_cylinder, Volume_pixcel))

dir_name,csv_name,img_name = outDir()
if dir_name[-1] != "/":
    dir_name += "/"
csv_path = dir_name + csv_name
img_path = dir_name + img_name
f = open(csv_path, "w", newline="")
writer = csv.writer(f)
writer.writerow(Title)
writer.writerows(Data.T)
f.close()
cv2.imwrite(img_path,img_result)
