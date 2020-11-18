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

#現在的動畫類別與期數
bingoNumber = Recaptcha_Lib.GetNextAni()
print("現在期數：{bingoNum}".format(bingoNum=bingoNumber))
def Record():
	global bingoNumber
	GetPeroids = False
	
	Start_time = time.time()

	# 輸出結果
	print(Start_time)
	# 選擇第3隻攝影機
	cap = cv2.VideoCapture(2)

	file_object = open('recognizeResult.txt', 'a')

	#預設等待時間
	recordTime = 60
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
			if GetPeroids == False:
				bingoNumber += 1
				# if len(bingoPeriods)>1:
				# 	#那就校正回下一個開獎號碼
				# 	bingoNumber = int(list(bingoPeriods.keys())[-1])+1

				#如果賓果號碼有要校正，到這邊就已經校正結束了，現在就能判斷最終要用什麼切圖邊界
				imageType, recordTime = Recaptcha_Lib.fromBingoNumberGetImageType(bingoNumber)
				print("第{peroids}期，現在要開獎的動畫為：{aniType},預計錄製{recordTime}秒".format(
					peroids=bingoNumber, aniType=Ani[str(imageType)], recordTime=recordTime))

				bingoPeriods[bingoNumber] = []
				GetPeroids = True

			img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
			# img = Image.open(str(imageType) + '_{index}.jpg'.format(index = str(j)))
			recognizeResult, secondSplitImg = Recaptcha_Lib.combineResult(img=img,
																		  imageType=str(imageType))
			# 顯示圖片
			cv2.imshow('process done', secondSplitImg)

			cv2.waitKey(1)
			
			filename = "{bingoNumber}_{AniName}_{imageType}_{hour}_{min}_{sec}".format(
				bingoNumber=bingoNumber, AniName=Ani[str(imageType)], imageType=imageType, hour=time.localtime().tm_hour, min=time.localtime().tm_min, sec=time.localtime().tm_sec)

			# cv2.imwrite("C:\\Users\\NO NAME\\Desktop\\ReadCamera\\out\\" +
			#             filename+".jpg", frame)

			#因為不支援中文檔名，所以用imencode代替
			cv2.imencode('.jpg', frame)[1].tofile(	"C:\\Users\\NO NAME\\Desktop\\ReadCamera\\out\\" + filename+".jpg")

			i = 0
			# print(recognizeResult)
			#經過檢查後，可以被加入list的數字
			notRepeatNumber = []
			for num in recognizeResult.split(","):
				if num not in bingoPeriods[bingoNumber]:
					#如果辨識到的字元不是空值，且單一字元數量為2的話，才算是一個數字
					if num != "":
						notRepeatNumber.append(num)
			#同時間只有一組數字會被辨識到，超過一個數字辨識都是錯誤
			# if len(notRepeatNumber) > 1:
			# 	bingoPeriods[bingoNumber].append(notRepeatNumber[1])
			# 	continue
			for number in notRepeatNumber:
				bingoPeriods[bingoNumber].append(number)
			print(str(bingoNumber) + ":" +
			      str(len(bingoPeriods[bingoNumber]))+"," + ','.join(bingoPeriods[bingoNumber]))
			#因為辨識的夠清楚了，可以不用做篩選
			# print(str(bingoNumber) + ":" + recognizeResult)

		#現在時間與啟動錄影時間>recordTime秒就離開
		now = time.time()
		if now - Start_time > recordTime:
			print("已錄製{recordTime}秒".format(recordTime=recordTime))
			try:
				#寫Log紀錄檔 期數與開獎號碼（不重複）
				file_object.write("{bingoPeriodsNumber}-{imageName}:{bingoPeriodsLength}_{bingoNumber}\n".format(bingoPeriodsNumber=bingoNumber,
																												imageName=Ani[str(imageType)],
																												bingoPeriodsLength=str(len(bingoPeriods[bingoNumber])),
																												bingoNumber=','.join(bingoPeriods[bingoNumber])))
				# file_object.write(str(bingoNumber) + ":" + recognizeResult+"\n")
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
	time.sleep(1)
	#可以被5分鐘整除
	if result[4] % 5 == 0:
		#秒數為25
		if result[5] == 16:
			#開始錄影
			Record()
