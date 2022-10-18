from fileinput import isfirstline
import os
from sys import flags
import numpy as np
import cv2
import csv

#mask = input("Input mask image file")

def Img_input(Flag):
    while True:
        if Flag == 0:
            img = input("Input dot image file:")
        else:
            img = input("Input dot mask image file:")

        if not os.path.isfile(img):
            print("Error: This path does not exist!!")
            continue
        path_tuple = os.path.splitext(img)
        if path_tuple[1] != (".png" or ".tif" or ".jpg" or ".jpeg"):
            print("Error: This file not image file!!")
            continue
        break
    return(img,path_tuple)

img_path,path_tuple = Img_input(0)
mask_path,path_tuple = Img_input(1)
img = cv2.imread(img_path,flags=1)
mask = cv2.imread(mask_path,flags=0)

#maskの色付き部分が判定できれば完成
