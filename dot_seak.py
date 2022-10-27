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

def dataConvert(img,mode):
    def pil2cv(img):
        new_img = np.array(img,dtype=np.uint8)
        if new_img.ndim == 2:
            pass
        elif new_img.shape[2] == 3:
            new_img = cv2.cvtColor(new_img,cv2.COLOR_RGB2BGR)
        elif new_img.shape[2] == 4:
            new_img = cv2.cvtColor(new_img,cv2.COLOR_RGBA2BGRA)
        return new_img
    def cv2pil(img):
        new_img = img.copy()
        if new_img.ndim == 2:
            pass
        elif new_img.shape[2] == 3:
            new_immg = cv2.cvtColor(new_img,cv2.COLOR_BGR2RGB)
        elif new_img.shape[2] == 4:
            new_img = cv2.cvtColor(new_img,cv2.COLOR_BGRA2RGBA)
        new_img = Image.fromarray(new_img)
        return new_img

    if mode == 1:
        new_img = pil2cv(img)
    elif mode == 2:
        new_img = cv2pil(img)
    return new_img

root = tkinter.Tk()
root.withdraw()

img_path = Img_input(0)
marking_path = Img_input(1)
img_pi = np.array(Image.open(img_path))
marking = np.array(Image.open(marking_path))

root.destroy()

############################################################
#   make mask
#差分をRの差が1でいいのかをもう一度再考する必要あり
diff = img_pi.astype(int) - marking.astype(int)
diff = np.abs(diff)
mask = (diff >= 1)*255
img_cv = dataConvert(img_pi,mode=1)

#diff
#mask
#img_pi
#img_cv


############################################################


#画像保存
img_ff = Image.fromarray(mask.astype(np.uint8))
print(img_ff.mode)
img_ff.save("C:/users/shunk/programfree/_4/gwyddion/img/dafaea.jpg")
