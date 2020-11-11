#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import time
import Recaptcha_Lib
from datetime import datetime
from keras.models import load_model
from PIL import Image

#因為要依照數字個別輸出
#所以要把歷史開獎期數存起來
bingoPeriods = {}


def Record():
    #現在的動畫類別與期數
    imageType, bingoNumber = Recaptcha_Lib.GetNextAni()
    print("第{peroids}期，現在要開獎的動畫為：{aniType}".format(
        peroids=bingoNumber, aniType=Ani[str(imageType)]))

    Start_time = time.time()

    # 輸出結果
    print(Start_time)
    # 選擇第2隻攝影機
    cap = cv2.VideoCapture(1)

    file_object = open('recognizeResult.txt', 'a')

    #儲存每期的開獎數字，網站顯示的是上期的，所以這期開獎數字要+1
    bingoPeriods[bingoNumber] = []
    i = 0
    while(True):
        # 從攝影機擷取一張影像
        ret, frame = cap.read()

        # 顯示圖片
        cv2.imshow('frame', frame)

        cv2.waitKey(1)
        i += 1
        #每秒截一次圖
        if i > 30:
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # img = Image.open(str(imageType) + '_{index}.jpg'.format(index = str(j)))
            recognizeResult, secondSplitImg = Recaptcha_Lib.combineResult(img=img,
                                                                          imageType=str(imageType))
            # 顯示圖片
            cv2.imshow('process done', secondSplitImg)

            cv2.waitKey(1)
            filename = "{hour}_{min}_{sec}".format(
                hour=time.localtime().tm_hour, min=time.localtime().tm_min, sec=time.localtime().tm_sec)
            cv2.imwrite("C:\\Users\\NO NAME\\Desktop\\out\\" +
                        filename+".jpg", frame)
            i = 0

            #經過檢查後，可以被加入list的數字
            notRepeatNumber = []
            for num in recognizeResult.split(","):
                if num not in bingoPeriods[bingoNumber]:
                    #如果辨識到的字元不是空值，且單一字元數量為2的話，才算是一個數字
                    if num != "" and len(num)==2:
                        notRepeatNumber.append(num)
            #同時間只有一組數字會被辨識到，超過一個數字辨識都是錯誤
            if len(notRepeatNumber) > 1:
                #設定跳出迴圈再進來一次
                continue
            for number in notRepeatNumber:
                bingoPeriods[bingoNumber].append(number)
            print(str(bingoNumber) + ":" + ','.join(bingoPeriods[bingoNumber]))

        #現在時間與啟動錄影時間>65秒就離開
        now = time.time()
        if now - Start_time > 55:
            try:
                #寫Log紀錄檔 期數與開獎號碼（不重複）
                file_object.write(str(bingoNumber) + "," +
                                  ','.join(bingoPeriods[bingoNumber])+"\n")
                file_object.close()
            except:
                import pdb
                pdb.set_trace()
            break
    # 釋放攝影機
    cap.release()
    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()


Ani = {"0": "格狀列表",
            "1": "打地鼠",
            "2": "動物農場",
            "3": "賽車",
            "4": "套圈圈",
            "5": "舞龍舞獅",
            "6": "彩球",
            "7": "魚"}


while True:
    # 轉換為 struct_time 格式的本地時間
    result = time.localtime(time.time())

    # 輸出結果
    print("目前分鐘:" + str(result[4]))

    #可以被5分鐘整除
    time.sleep(1)

    if result[4] % 5 == 0:
        #秒數為25
        if result[5] == 30:
            #開始錄影
            Record()
