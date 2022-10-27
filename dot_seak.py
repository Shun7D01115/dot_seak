from ast import Num
from fileinput import isfirstline
from multiprocessing.resource_sharer import stop
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
base = np.zeros((pixcel_height,pixcel_width),np.uint8)
pixcel_height = float(img_length)/float(pixcel_height)
pixcel_width = float(img_length)/float(pixcel_height)
pix_areas = pixcel_height * pixcel_width
max_height = float(max_height)/256.0

for i in range(1,nlabels):
    mask_part = base
    height = 0
    volume = 0
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
            if height <= img_gray[y+k][x+j]:
                height = img_gray[y+k][x+j]
            volume += img_gray[y+k][x+j]
    height = max_height * height
    volume = volume * pix_areas * max_height
    Height.append(height)
    Volume.append(volume)

    mask_part = cv2.threshold(mask_part,100,255,cv2.THRESH_BINARY)
    contours , __ = cv2.findContours(mask_part,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

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
