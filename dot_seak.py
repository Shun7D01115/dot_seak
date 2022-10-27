from fileinput import isfirstline
from multiprocessing.resource_sharer import stop
from tkinter import filedialog
import tkinter
from PIL import Image
import os
from sys import flags
import sys
import numpy as np
import csv

#mask = input("Input mask image file")

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
        print(file_name)
        if len(file_name) == 0:
            sys.exit()
        if not os.path.isfile(file_name):
            print("Error: This path does not exist!!")
            continue
        break
    return(file_name)

root = tkinter.Tk()
root.withdraw()

img_path = Img_input(0)
marking_path = Img_input(1)
img = np.array(Image.open(img_path))
marking = np.array(Image.open(marking_path))

root.destroy()
#差分をRの差が1でいいのかをもう一度再考する必要あり
diff = img.astype(int) - marking.astype(int)
diff = np.abs(diff)
diff_bin = (diff > 1)*255

#画像保存
img_ff = Image.fromarray(diff_bin.astype(np.uint8))
print(img_ff.mode)
img_ff.save("C:/users/shunk/programfree/_4/gwyddion/img/dafaea.jpg")
