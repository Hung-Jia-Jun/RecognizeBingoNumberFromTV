#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import pytesseract
from bs4 import BeautifulSoup
import requests
from PIL import Image
from matplotlib import pyplot as plt
import re
import time
import os
import cv2
import numpy as np
from keras.models import load_model
# import pytesseract
from math import *
from PIL import Image
from matplotlib import pyplot as plt
import re
import cv2
import numpy as np
import configparser
import random
model = load_model('Models/model.h5')


def PredictImg(img):
    # 載入模型
    #縮放圖片大小
    Max_Width = 20
    Max_Hight = 20
    x_test = []
    # for img in imgs:
    try:
        img = cv2.resize(img, (Max_Width, Max_Hight),
                         interpolation=cv2.INTER_CUBIC)
    except:
        return None
    x_test.append(img)
    x_test = np.array(x_test)
    x_test = x_test.reshape(x_test.shape[0], Max_Width, Max_Hight, 1)
    x_test = 255 - x_test
    x_test = x_test.astype('float32')
    x_test /= 255
    pred = model.predict(x_test, batch_size=25)
    outdict = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    pred_result = outdict[np.argmax(pred)]
    return pred_result

#去除掉圖片的雜訊，使用filter來決定可不可以用


def ImageFilter(width, height, widthMin, heightMin, widthMax, heightMax):
    # 面積太小就算雜訊
    if width <= widthMin or width > widthMax or height <= heightMin or height > heightMax or height - width < 5:
        return False
    else:
        return True
    # if width <= widthMin or width > widthMax or width*height < 70 \
    #         or width*height > 400 or height <= widthMax or height > heightMax or height - width < 5:


def boundleSort(contours, columnLength, imageType,
                widthMin,
                heightMin,
                widthMax,
                heightMax,):

    
    #x軸（橫向）
    #y軸（直向）
    #只有第一個格狀列表不用做排序
    # 做X軸排序（直向）
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

    #做Y軸排序（橫向）
    contours = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[1])

    boundle = []
    for i in range(0, len(contours)):
        x, y, width, height = cv2.boundingRect(contours[i])
        # 面積太小就算雜訊
        if ImageFilter(width, height, widthMin, heightMin, widthMax, heightMax) == False:
            continue
        # print (x, y, width, height)
        #把符合規則的邊界存起來
        boundle.append([x, y, width, height])

    #格狀列表要另外處理
    # if imageType == "0":
    #兩兩配對的點
    pairPoint = []
    #把每個框點依照距離兩兩分組
    for startBound in boundle:
        distance = []
        for endBound in boundle:
            #點跟點做自己比較距離皆為0
            if startBound != endBound:
                #sqrt((X-X1)**2 + (Y-Y2)**2)
                distance.append(sqrt((startBound[0]-endBound[0])**2\
                                    + (startBound[1]-endBound[1])**2))
        try:
            #此次比較中，最短的距離是多少
            minDistance = min(distance)
            #距離太遠就不要配對了，代表這可能是雜訊
            if minDistance > 30:
                continue
        except:
            continue
        for endBound in boundle:
            #點跟點做自己比較距離皆為0
            if startBound != endBound:
                #依照最短距離得出跟現在這個點最短的是誰
                if sqrt((startBound[0]-endBound[0])**2 \
                        + (startBound[1]-endBound[1])**2) == minDistance:
                    #依照X軸大小決定誰在前誰在後
                    if startBound[0] < endBound[0]:
                        #檢查這組配對有沒有在List裡面出現
                        inList = False
                        for pairBound in pairPoint:
                            if startBound == pairBound[0]:
                                inList = True
                        if inList == False:
                            pairPoint.append([startBound, endBound])
                    else:
                        #檢查這組配對有沒有在List裡面出現
                        inList = False
                        for pairBound in pairPoint:
                            if endBound == pairBound[0]:
                                inList = True
                        if inList == False:
                            pairPoint.append([endBound , startBound])
    totalPoint = []
    #把所有配對好的點位，變成一維的list
    for point in pairPoint:
        totalPoint.append(point[0])
        totalPoint.append(point[1])

    #複寫掉原本的boundle的記憶體位置
    boundle = totalPoint
   
    #list 分群
    splitRows = [boundle[i:i+columnLength] for i in range(0, len(boundle), columnLength)]
   
    if imageType=="0":
        boundles = []
        for bound in splitRows:
            # 使用Ｘ軸來排序
            boundles.append(sorted(bound, key=lambda bound: bound[0]))
        splitRows = boundles
    return splitRows


def DrawBoundle(boundle, img, columnLength):
    k = 0
    for i in range(0, len(boundle)):
        for j in range(len(boundle[i])):
            x, y, width, height = boundle[i][j]
            # print (x, y, width, height)
            cv2.rectangle(img, (x, y),
                          (x + width,
                           y + height), (153, 153, 0), 2)
            cv2.putText(img, str(k), (x,y), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 255), 1, cv2.LINE_AA)
            k+=1
    return img


def imageProcess(img, THRESH_BINARY_TYPE, threshValue, area, columnLength, imageType,
                                                                    widthMin,
                                                                    heightMin,
                                                                    widthMax,
                                                                    heightMax):

    #（left, upper, right, lower）
    #(x_start,y_start,x_end,y_end)
    #切割掉不重要的區域
    crop_img = img.crop(area)

    # plt.imshow(crop_img)
    # plt.title('crop_img picture')
    # plt.show()

    img = cv2.cvtColor(np.asarray(crop_img), cv2.COLOR_RGB2BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    originalImg = img.copy()
    originalImg = cv2.GaussianBlur(originalImg, (1, 1), 1)

    if THRESH_BINARY_TYPE == "THRESH_BINARY_INV":
        #二值化
        ret, originalImg = cv2.threshold(originalImg, threshValue, 255,
                                         cv2.THRESH_BINARY_INV)
    else:
        #二值化
        ret, originalImg = cv2.threshold(originalImg, threshValue, 255,
                                         cv2.THRESH_BINARY)
    #x軸（橫向）
    #y軸（直向）
    #保存圖像處理好的圖片
    #膨脹
    imageProcessDone = cv2.erode(originalImg, (1, 2), iterations=2)
    # plt.imshow(imageProcessDone)
    # plt.title('imageProcessDone')
    # plt.show()

    secondSplitImg = imageProcessDone.copy()
    #把完全看不到文字只剩下填滿黑色的色塊版本去做輪廓辨識
    Splitcontours, hierarchy = cv2.findContours(
        secondSplitImg, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]

    #送去做Boundle排序，並傳送輪廓限制
    boundle = boundleSort(contours=Splitcontours,
                          columnLength=columnLength,
                          imageType=imageType,
                            widthMin = widthMin,
                            heightMin = heightMin,
                            widthMax = widthMax,
                            heightMax = heightMax,)

    secondSplitImg = DrawBoundle(boundle=boundle,
                                 img=secondSplitImg,
                                 columnLength=20)
    return boundle, imageProcessDone, secondSplitImg

#顯示辨識結果
def showRecognizeResult(img, THRESH_BINARY_TYPE, threshValue, area, columnLength, imageType,
                                                            widthMin,
                                                            heightMin,
                                                            widthMax,
                                                            heightMax):

    boundle, imageProcessDone, secondSplitImg = imageProcess(img=img,
                                                             THRESH_BINARY_TYPE=THRESH_BINARY_TYPE,
                                                             threshValue=threshValue,
                                                             area=area,
                                                             columnLength=columnLength,
                                                             imageType=imageType,
                                                             widthMin = widthMin,
                                                             heightMin = heightMin,
                                                             widthMax = widthMax,
                                                             heightMax = heightMax)

    #儲存所有號碼圖的辨識結果
    output = []
    _originalImg = imageProcessDone.copy()
    for i in range(0, len(boundle)):
        for j in range(len(boundle[i])):
            x, y, width, height = boundle[i][j]
            # 面積太小就算雜訊
            if ImageFilter(width, height, widthMin, heightMin, widthMax, heightMax) == False:
                continue
            newImage = _originalImg[y:y+height,
                                    x:x+width]
            predValue = PredictImg(newImage)
            output.append(predValue)
            # plt.imshow(newImage)
            # plt.title(predValue+":"+str(x)+","+str( y)+","+str( width)+","+str( height))
            # plt.show()
            input_dir = ("cut_image/")
            if not os.path.isdir(input_dir):
                os.makedirs(input_dir)
            result = time.localtime(time.time())
            cv2.imwrite("./cut_image/{i}_{predValue}_{random}.jpg".format(i=str(i),
                                                                 predValue=predValue,
                                                                 random=str(random.randint(1,10))), newImage)
    return output, secondSplitImg

def combineResult(img, imageType):
    config = configparser.ConfigParser()
    config.read('config.ini')
    # print("Type:" + str(imageType))
    #圖片要辨識的類型，共八種

    #x軸（橫向）
    #y軸（直向）
    _config = config[imageType]

    #讀取切割區域的座標範圍
    area = tuple(int(value) for value in _config["area"].split(","))

    #讀取二值化閥值
    threshValue = int(_config["threshValue"])
    #二值化方案（THRESH_BINARY_INV,THRESH_BINARY_INV_INV）
    TYPE = _config["THRESH_BINARY_TYPE"]
    #橫行直列的數量
    columnLength = int(_config["columnLength"])

    #輪廓框區域限制
    widthMin = int(_config["widthMin"])
    heightMin = int(_config["heightMin"])
    widthMax = int(_config["widthMax"])
    heightMax = int(_config["heightMax"])
    # img = Image.open(imageType + '_3.jpg')
    output, secondSplitImg = showRecognizeResult(img=img, THRESH_BINARY_TYPE=TYPE, threshValue=threshValue,
                                                 area=area, columnLength=columnLength, imageType=imageType,
                                                 widthMin = widthMin,
                                                 heightMin =heightMin,
                                                 widthMax = widthMax,
                                                 heightMax =heightMax)
    #每兩個數字為一排
    step = 2
    _output = [output[i:i+step] for i in range(0, len(output), step)]
    
    #賽車與套圈圈的數字要做特別處理
    if imageType == "3" or imageType == "4":
        #因為有兩排，現在想先知道切片要切第一排與第二排要留多少
        otherRowItemIndex = 10 - (20 - len(_output))
        outFirstLine = []
        outSecondLine = []

        for i in range(len(_output)):
            try:
                #輸出1,3,5,7,9 行，因為數字是直列下來的
                if i % 2 == 1:
                    outSecondLine.append(_output[i])
                    # print (ele[0]+ele[1]+",",end='')
                else:
                    if len(outFirstLine) < otherRowItemIndex:
                        outFirstLine.append(_output[i])
                    else:
                        #第二排的數字出來了，那就順位繼續
                        outSecondLine.append(_output[i])
            except:
                continue
        _output = outSecondLine+outFirstLine
        if len(_output)==0:
            # 轉換為 struct_time 格式的本地時間
            result = time.localtime(time.time())
            _img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            _img = cv2.cvtColor(cv2.UMat(_img), cv2.COLOR_RGB2GRAY)
            cv2.imwrite(".\\nonRecognize_image\\{i}_{time}.jpg".format(i=str(
                imageType), time=str(result[3])+"-"+str(result[4])+"-"+str(result[5])), _img)

    if imageType == "bingoNumberRecognize":
        return "".join(output), secondSplitImg

    outputStr = ""
    for ele in _output:
        try:
            outputStr += ele[0]+ele[1] + ","
        except:
            continue
    return outputStr, secondSplitImg

#取得下一次開獎的動畫


def GetNextAni():
    #現在動畫  109063595%8 + 3 = 5(套圈圈)
    r = requests.get(
        "https://www.taiwanlottery.com.tw/Lotto/BINGOBINGO/drawing.aspx")

    soup = BeautifulSoup(r.text, 'html.parser')
    div = soup.find(id="lblBBDrawTerm")
    bingoNumber = int(div.text)

    #返回現在動畫的類別與期數
    return bingoNumber


def fromBingoNumberGetImageType(bingoNumber):
    config = configparser.ConfigParser()
    config.read('config.ini')
    nextBingoAniType = (bingoNumber + 2) % 8
    #因為每個動畫結束時間不一樣，所以要有一個config來設定要錄影多久
    #從啟動錄影這個Process開始要13秒才能正式啟動Opencv的imshow
    #所以要依照不同動畫調整recordTime這個設定
    _config = config[str(nextBingoAniType)]
    recordTime = int(_config["recordTime"])
    return nextBingoAniType, recordTime
if __name__ == "__main__":
    pass