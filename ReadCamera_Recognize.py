#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import cv2
import time
import Recaptcha_Lib
from datetime import datetime
from keras.models import load_model
from PIL import Image

#因為要依照數字個別輸出
#所以要把上個結果存起來
lastOutputStr = ""
def Record(imageType):
    global lastOutputStr
    Start_time = time.time()
    
    # 輸出結果
    print(Start_time)
    # 選擇第1隻攝影機
    cap = cv2.VideoCapture(0)
    
    file_object = open('recognizeResult.txt', 'a')

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
            cv2.imwrite("C:\\Users\\NO NAME\\Desktop\\out\\"+filename+".jpg", frame)
            i = 0

            #定義要寫到Log的字串
            outputStr = ""
            #每兩個數字為一排
            step = 2
             
            #先做Diff運算，取出最新更新的數字
            diffRecognizeResult = recognizeResult.replace(lastOutputStr, "")
            print(diffRecognizeResult)
            lastOutputStr = recognizeResult
            #寫Log紀錄檔
            file_object.write(diffRecognizeResult+"\n")

        #現在時間與啟動錄影時間>100秒就離開
        now = time.time()
        if now - Start_time > 100:
            file_object.close()
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
    imageType = Recaptcha_Lib.GetNextAni()
    print("現在開獎的動畫為："+Ani[str(imageType)])

    #因為動畫的dic從0開始,但是config從 1 開始，所以要+1
    imageType = imageType+1
    if result[4] % 5 == 0:
        #開始錄影
        Record(imageType)
    
