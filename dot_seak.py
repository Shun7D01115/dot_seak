from ast import Num
from distutils import text_file
from enum import Flag
from fileinput import isfirstline
from multiprocessing.resource_sharer import stop
from pickletools import uint8
from tabnanny import check
from tkinter import filedialog
import tkinter
from PIL import Image,ImageFilter
import os
from sys import flags
import sys
import numpy as np
import pandas as pd
import cv2
import csv
import time
import webbrowser

def EasterEgg():
    print("README を読んでみて...........")
    time.sleep(3)
    url = "https://github.com/Shun7D01115/dot_seak"
    webbrowser.open(url)
    sys.exit()

def Selecting(Flag):
    def File(Flag,iDir):
        typ = [("Image File", "*.png *.jpg *.jpeg *.tif *.bmp"), ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"), ("Tiff", "*.tif"), ("Bitmap", "*.bmp"), ("すべて", "*")]
        while True:
            if Flag == 0:
                print("ドットのイメージファイルを入力してください:")
            elif Flag == 1:
                print("ドットにマーキングしたイメージファイルを入力してください:")

            path_name = filedialog.askopenfilename(filetypes=typ,initialdir=iDir)
            if len(path_name) == 0:
                sys.exit()
            if not os.path.isfile(path_name):
                print("Error: This path does not exist!!")
                continue
            print(".........................................OK")
            break
        return(path_name)

    def Dirct(iDir):
        while True:
            print("CSVファイルの入力先を決定してください:")
            path_name = filedialog.askdirectory(initialdir=iDir)
            if len(path_name) == 0:
                sys.exit()
            if not os.path.isdir(path_name):
                print("Error: This path does not exist!!")
                continue
            print(".........................................OK")
            break
        return(path_name)
    iDir = os.path.abspath(os.path.dirname(__file__))
    if Flag == 2:
        path_name = Dirct(iDir)
    else:
        path_name = File(Flag,iDir)

    return(path_name)

def NanMake(dat, base):
    mat = np.zeros_like(base)
    mat[:] = np.nan
    if dat.size == 0:
        return (mat)
    for i in range(1,dat.size):
        mat[i-1] = dat[i-1]
    return (mat)

def freqDistribute(rank,data):
    data_rank = pd.Series(data)
    data_cut = pd.cut(data_rank,bins=rank)
    data_vc = data_cut.value_counts(sort=False)
    data_numpy = data_vc.values
    return (data_numpy)

def NumCheck(Flag):
    while True:
        if Flag == 0:
            num = input("画像の幅を入力して下さい(単位[μm]):")
        else:
            num = input("画像の最大高さを入力してください(単位[nm]):")

        if len(num) == 0:
            print("Error:数値を入力してください")
            continue
        if not str.isdigit(num):
            try:
                float(num)
            except ValueError:
                print("Error:自然数か小数を入力してください")
                continue
        break
    return(num)

while True:
    root = tkinter.Tk()
    root.withdraw()

    img_path = Selecting(0)
    marking_path = Selecting(1)
    img = cv2.imread(img_path)
    marking = cv2.imread(marking_path)

    root.destroy()

    ############################################################
    
    img_length = NumCheck(0)
    max_height = NumCheck(1)
    pixcel_height , pixcel_width , __ = img.shape

    ############################################################
    #   make mask
    diff = cv2.absdiff(img,marking)
    diff = cv2.cvtColor(diff,cv2.COLOR_BGR2GRAY)
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    __ , mask = cv2.threshold(diff,5,255,cv2.THRESH_BINARY)

    ############################################################
    nlabels,labels,stats, __ = cv2.connectedComponentsWithStats(mask)

    ############################################################
    Num = []#
    Axis = []
    Height = []#
    Volume = []#
    Density = []
    height_onePix = 1000 * float(img_length)/float(pixcel_height)
    width_onePix = 1000 * float(img_length)/float(pixcel_width)
    pix_areas = height_onePix * width_onePix
    z_one = float(max_height)/256.0
    img_result = img.copy()

    for i in range(1,nlabels):
        mask_part = np.zeros((pixcel_height,pixcel_width,3),np.uint8)
        height_h = 0.0
        height_r = 0.0
        volume = 0.0
        area_count = 0
        Count = 0
        Num.append(i)
        area_count = stats[i][cv2.CC_STAT_AREA]
        areas = pix_areas * area_count
        x = stats[i][cv2.CC_STAT_LEFT]
        y = stats[i][cv2.CC_STAT_TOP]
        w = stats[i][cv2.CC_STAT_WIDTH]
        h = stats[i][cv2.CC_STAT_HEIGHT]
        for j in range(0,w):
            for k in range(0,h):
                if labels[y+k][x+j] != i:
                    continue
                mask_part[y+k][x+j] = 255
                if height_h <= img_gray[y+k][x+j]:
                    height_h = img_gray[y+k][x+j]
                volume += img_gray[y+k][x+j]

        mask_gray = cv2.cvtColor(mask_part,cv2.COLOR_BGR2GRAY)
        __ , mask_bin = cv2.threshold(mask_gray,100,255,cv2.THRESH_BINARY)
        contours = cv2.findContours(mask_bin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

        for l in range(1,len(contours[0][0])):
            coordinate = contours[0][0][l]
            if coordinate[0][0] == 0 or coordinate[0][1] == 0:
                continue
            if coordinate[0][0] == pixcel_width or coordinate[0][1] == pixcel_height:
                continue
            Count += 1
            height_r += img_gray[coordinate[0][1],coordinate[0][0]]
        if Count == 0:
            height_row = 0.0
        else :
            height_row = float(height_r) / float(Count)
        height_res = height_h - height_row
        height_res *= z_one
        dot_volume = (volume - height_row * area_count) * pix_areas * z_one
        Height.append(height_res)
        Volume.append(dot_volume)

        img_result = cv2.rectangle(img_result,(x,y),(x+w,y+h),(255,0,0),1)
        text_x = int(round(x+2))
        text_y = int(round(y+10))
        img_result = cv2.putText(img_result,str(i),(text_x,text_y),cv2.FONT_HERSHEY_PLAIN,1,(20,20,255))

        del mask_gray
        del mask_bin
        del contours


    vo_rank = np.arange(0,25000,500)
    hei_rank = np.arange(0,10,0.2)
    hei_vc = freqDistribute(hei_rank,Height)
    vo_vc = freqDistribute(vo_rank,Volume)

    if vo_rank.size >= len(Volume):
        Volume = NanMake(Volume,vo_vc)
        Height = NanMake(Height,vo_vc)
        Num = NanMake(Num,vo_rank)
    else:
        hei_rank_comp = NanMake(hei_rank,Volume)
        vo_rank_comp = NanMake(vo_rank,Volume)
        hei_comp = NanMake(hei_vc,Volume)
        vo_comp = NanMake(vo_vc,Volume)

############################################################
    Title = ["Num","Height","Volume","高さ階級","高さ","体積階級","体積"]
    Data = np.vstack((Num,Height,Volume,hei_rank_comp,hei_comp,vo_rank_comp,vo_comp))
    ############################################################
    root = tkinter.Tk()
    root.withdraw()
    folder_path = Selecting(2)
    root.destroy()

    csvfile_name = "out"
    while True:
        print("保存するCSVファイルのファイル名を決定してください(拡張子.csvは必要ないです)")
        csvfile_name = input("⇒")
        if len(csvfile_name) == 0:
            print("Error:ファイル名を入力してください")
            continue
        check_file = len(csvfile_name.split(".",1))
        if check_file >= 2:
            print("Error:拡張子が記述されています.")
            continue
        break

    file_path_name = folder_path + "/" + csvfile_name
    f = open(file_path_name + ".csv","w",newline="")
    writer = csv.writer(f)
    writer.writerow(Title)
    writer.writerows(Data.T)
    f.close()

    result_path = file_path_name + ".jpg"

    cv2.imshow("Result",img_result)
    print("キー入力で終了します")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(result_path,img_result)
    print("CSVファイルは" + file_path_name + ".csv" + "にあります")
    print("All Complete!!")
    print("\n\n")

    rep = 0
    while True:
        print("\"help\" may save you")
        ques = input("作業を続けますか？ (y/n):")
        if ques == "help":
            EasterEgg()
        elif ques == "y":
            rep = 1
            break
        elif ques == "n":
            break
        else :
            print("Error:Invalid input")
            continue
    if rep == 0:
        print("終了します，しばらくお待ちください..........")
        time.sleep(2)
        sys.exit()
    else:
        continue

################################################################################
####直径を入れてない!!!!!!!!!!!!!!!!!!!!!!!!!!!
################################################################################
