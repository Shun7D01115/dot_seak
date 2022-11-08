from ast import Num
from distutils import text_file
from enum import Flag
from fileinput import isfirstline
from multiprocessing.resource_sharer import stop
from pickletools import uint8
from tabnanny import check
from tkinter import filedialog
import tkinter
from PIL import Image, ImageFilter
import os
from sys import flags
import sys
import numpy as np
import pandas as pd
import cv2
import csv
import time
import webbrowser
import random


def EasterEgg():
    print("README を読んでみて...........")
    time.sleep(3)
    url = "https://github.com/Shun7D01115/dot_seak"
    webbrowser.open(url)
    sys.exit()


def Selecting(Flag):
    def File(Flag, iDir):
        typ = [("Image File", "*.png *.jpg *.jpeg *.tif *.bmp"), ("PNG", "*.png"),
               ("JPEG", "*.jpg *.jpeg"), ("Tiff", "*.tif"), ("Bitmap", "*.bmp"), ("すべて", "*")]
        while True:
            if Flag == 0:
                print("ドットのイメージファイルを入力してください:")
            elif Flag == 1:
                print("ドットにマーキングしたイメージファイルを入力してください:")

            path_name = filedialog.askopenfilename(
                filetypes=typ, initialdir=iDir)
            if len(path_name) == 0:
                sys.exit()
            if not os.path.isfile(path_name):
                print("Error: This path does not exist!!")
                continue
            print(".........................................OK")
            break
        return (path_name)

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
        return (path_name)
    iDir = os.path.abspath(os.path.dirname(__file__))
    if Flag == 2:
        path_name = Dirct(iDir)
    else:
        path_name = File(Flag, iDir)

    return (path_name)


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
    return (num)


root = tkinter.Tk()
root.withdraw()

while True:
    img_path = Selecting(0)
    img = cv2.imread(img_path)
    marking_path = Selecting(1)
    marking = cv2.imread(marking_path)
    if img.size == markinng.size:
        break
    print("Error:ピクセルサイズが異なります．")
    #print("Description:")
    print("\n")

root.destroy()

###########################################################

img_length = NumCheck(0)
max_height = NumCheck(1)
pixcel_height, pixcel_width, __ = img.shape

###########################################################
#   make img mask
diff = cv2.absdiff(img, marking)
diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
__, mask = cv2.threshold(diff, 5, 255, cv2.THRESH_BINARY)

nlabels, labels, stats, __ = cv2.connectedComponentsWithStats(mask)

img_zeros = np.zeros(img.shape[0:3])
height_a, width_a = img.shape[0:2]
cols = []

for i in range(1, nlabels):
    cols.append(np.array([random.randint(0, 255),
                random.randint(0, 255), random.randint(0, 255)]))
for i in range(1, nlabels):
    img_zeros[labels == i, ] = cols[i-1]

cv2.imshow("dafda", img_zeros)
cv2.waitKey()
cv2.destroyAllWindows()
