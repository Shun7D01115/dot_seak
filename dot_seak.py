from ast import Num
from fileinput import isfirstline
from multiprocessing.resource_sharer import stop
from pickletools import uint8
from tkinter import filedialog
import tkinter
from PIL import Image,ImageFilter
import os
from sys import flags
import sys
import numpy as np
import cv2
import csv

import random

def Img_input(Flag):
    while True:
        typ = [("Image File", "*.png *.jpg *.jpeg *.tif *.bmp"), ("PNG", "*.png"),
               ("JPEG", "*.jpg *.jpeg"), ("Tiff", "*.tif"), ("Bitmap", "*.bmp"), ("すべて", "*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        if Flag == 0:
            print("ドットのイメージファイルを入力してください:")
        else:
            print("ドットにマーキングしたイメージファイルを入力してください:")

        file_name = filedialog.askopenfilename(filetypes=typ,initialdir=iDir)
        if len(file_name) == 0:
            sys.exit()
        if not os.path.isfile(file_name):
            print("Error: This path does not exist!!")
            continue
        print(".........................................OK")
        break
    return(file_name)


root = tkinter.Tk()
root.withdraw()

img_path = Img_input(0)
marking_path = Img_input(1)
img = cv2.imread(img_path)
marking = cv2.imread(marking_path)

root.destroy()

############################################################

img_length = input("画像の幅を入力して下さい(単位[μm]):")
max_height = input("画像の最大高さを入力してください(単位[nm]):")
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
Areas = []#
Density = []
height_onePix = float(img_length)/float(pixcel_height)
width_onePix = float(img_length)/float(pixcel_width)
pix_areas = height_onePix * width_onePix
z_one = float(max_height)/256.0

for i in range(1,nlabels):
    mask_part = np.zeros((512,512,3),np.uint8)
    height_h = 0
    height_r = 0
    volume = 0
    area_count = 0
    Count = 0
    Num.append(i)
    areas = pix_areas * stats[i][cv2.CC_STAT_AREA]
    Areas.append(areas)
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
            area_count += 1

    mask_gray = cv2.cvtColor(mask_part,cv2.COLOR_BGR2GRAY)
    ret , mask_bin = cv2.threshold(mask_gray,100,255,cv2.THRESH_BINARY)
    contours = cv2.findContours(mask_bin,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    if i == 5:
        con = np.array(contours)
        print(np.array(contours))
        print(con)
    #for l in range(len(contours)):
    #    a = contours[0][0][l]
    #    if a[0][0] == 0 or a[0][1] == 0:
    #        continue
        Count += 1
        height_r += img_gray[a[0][1],a[0][0]]
    #height_r = float(height_r) / float(Count)
    height_res = height_h - height_r
    height_res *= z_one
    volume = (volume * pix_areas - height_r * area_count * pix_areas) * z_one
    Height.append(height_res)
    Volume.append(volume)

    del mask_gray
    del mask_bin
    del contours

Title = ["Num","Height","Volume","Areas"]
Data = np.vstack((Num,Height,Volume,Areas))

f = open("C:/Users/shunk/Downloads/data.csv","w",newline="")
writer = csv.writer(f)
writer.writerow(Title)
writer.writerows(Data.T)
f.close()


#cv2.imshow("mak",)
#cv2.waitKey()
#cv2.destroyAllWindows()

############################################################
#画像保存
#img_ff = Image.fromarray(mask.astype(np.uint8))
#print(img_ff.mode)
#img_ff.save("C:/users/shunk/programfree/_4/gwyddion/img/dafaea.jpg")


#高さ，体積は下の高さからの差分で求める
#直径はちょっと悩むやつ
#度数分布表を作成する
