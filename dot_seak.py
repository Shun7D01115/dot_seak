from re import I
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

#GUI展開
root = tkinter.Tk()
root.title(u"Dot Searcher")
root.geometry("400x300")

#解析ファイル読み込み
fTyp = [("Data file","*")]
iDir =os.path.abspath(os.path.dirname(__file__))
file_name = tkinter.filedialog.askopenfilename(filetypes=fTyp,initialdir=iDir)





root.mainloop()
