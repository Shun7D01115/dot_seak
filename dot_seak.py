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
    root = tkinter.TK()
    root.withdraw()
    fTyp = [("",".gwy")] #ファイルタイプ変更
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo('あ','い')
    file = tkinter.filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)

    return(file)

def file_write(filename):
    root = tkinter.Tk()
    root.withdraw()
    fTyp = [("gwy","*.gwy")]
    iDir = os.path.abspath(os.path.dirname(__file__))
    tkinter.messagebox.showinfo('う','え')
    file = tkinter.filedialog.asksaveasfilename(filetypes = fTyp,initialdir=iDir,initialfile= filename)
    
    return(file)

def empty(a):
    pass



###########################
path = file_read()
filename,ext = os.path.splitext(os.path.basename(path))
kernel = np.ones((2,2),no.uint8)
