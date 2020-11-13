#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import traceback
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Recaptcha_Lib import *
from PIL import Image
class Slider(QWidget):
	def __init__(self,parent=None):
		self.Ani = {"格狀列表": "0",
                    "打地鼠": "1",
                    "動物農場": "2",
                    "賽車": "3",
                    "套圈圈": "4",
                    "舞龍舞獅": "5",
                    "彩球": "6",
                    "魚": "7"}
		self.config = configparser.ConfigParser()
		#讀取/修改Config檔
		self.config.read('config.ini')
		
		super().__init__(parent)
		self.area = (165, 320, 180, 385)

		self.setWindowTitle("image process tool")
		self.resize(300,100)
		
		self.layout = QVBoxLayout()

		self.comboBox = QComboBox(self)
		self.comboBox.addItems(["格狀列表",
                    "打地鼠",
                    "動物農場",
                    "賽車",
                    "套圈圈",
                    "舞龍舞獅",
                    "彩球",
                    "魚"])
        
		self.comboBox.currentIndexChanged.connect(self.valuechange)
		self.layout.addWidget(self.comboBox)

		#讀取圖片
		self.loadFile = QPushButton("Load File")
		self.loadFile.clicked.connect(self.getFiles)
		self.layout.addWidget(self.loadFile)

		#二值化拉桿
		self.threshValuebar = self.createQSliderBar(
			callbackfunction=self.valuechange, max_value=255, labelText="thresh Value")
		




		#------------------切圖區域設定------------------------------------------------------------------------------------------------------------------------------------------------
		self.areaX_Start = self.createQSliderBar(
										callbackfunction=self.valuechange,
										currentValue=self.area[0], 
										max_value=1000, 
										labelText="areaX_Start")
		
		self.areaX_End = self.createQSliderBar(callbackfunction=self.valuechange,
												currentValue =self.area[1],
												max_value = 1000,
												labelText="areaX_End")
		
	
		self.areaY_Start = self.createQSliderBar(callbackfunction=self.valuechange,
													currentValue =self.area[2],
													max_value = 1000,
													labelText="areaY_Start")
		
	
		self.areaY_End = self.createQSliderBar(callbackfunction = self.valuechange,
													currentValue =self.area[3],
													max_value = 1000,
													labelText="areaY_End")
		#------------------切圖區域設定------------------------------------------------------------------------------------------------------------------------------------------------


		#------------------輪廓框限制設定------------------------------------------------------------------------------------------------------------------------------------------------
		self.widthMin = self.createQSliderBar(
					callbackfunction=self.valuechange,
		  										currentValue=self.area[0],
		  										max_value=100,
					labelText="widthMin")

		self.heightMin = self.createQSliderBar(callbackfunction=self.valuechange,
										 currentValue=self.area[1],
										 max_value=100,
										 labelText="heightMin")

		self.widthMax = self.createQSliderBar(callbackfunction=self.valuechange,
										   currentValue=self.area[2],
										   max_value=100,
										   labelText="widthMax")

		self.heightMax = self.createQSliderBar(callbackfunction=self.valuechange,
										 currentValue=self.area[3],
										 max_value=100,
										 labelText="heightMax")
		#------------------切圖區域設定------------------------------------------------------------------------------------------------------------------------------------------------

		self.checkboxValue = self.createCheckbox(callback=self.valuechange)
		
		self.TYPE = "THRESH_BINARY_INV"
		self.imageType = 0
		self.columnLength = 20
		
		
		self.valueTextLabel = QLabel("")
		self.valueTextLabel.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.valueTextLabel)



		self.loadButton = QPushButton("load")
		self.loadButton.move(64, 64)
		self.loadButton.clicked.connect(self.loadValue)
		self.layout.addWidget(self.loadButton)

		self.saveButton = QPushButton("Save")
		self.saveButton.move(64, 64)
		self.saveButton.clicked.connect(self.saveConfig)
		self.layout.addWidget(self.saveButton)

	def getFiles(self):
		global view
		self.view = view
		fname = QFileDialog.getOpenFileName(self, 'Open file',
                                      '.', "Image files (*.jpg)")
		cv2.destroyAllWindows()
		try:
			self.img = Image.open(fname[0])
		except:
			pass
		#更新介面
		self.view.update()
	#存到Config檔裡面
	def saveConfig(self):
		
		imageType = self.comboBox.currentText()
		imageType = self.Ani[imageType]
		_config = self.config[imageType]

		threshValue = self.threshValuebar.value()
		areaX_Start = self.areaX_Start.value()
		areaX_End = self.areaX_End.value()
		areaY_Start = self.areaY_Start.value()
		areaY_End = self.areaY_End.value()

		#輪廓框區域限制
		widthMin = self.widthMin.value()
		heightMin = self.heightMin.value()
		widthMax = self.widthMax.value()
		heightMax = self.heightMax.value()

		#圖像色彩反相
		if self.checkboxValue.isChecked():
			self.TYPE = "THRESH_BINARY_INV"
		else:
			self.TYPE = "THRESH_BINARY"

		thresh_binary_type = self.TYPE
		_config["threshValue"] = str(threshValue)
		_config["area"] = str(areaX_Start) + "," + str(areaY_Start) + "," + str(areaX_End) + "," + str(areaY_End)
		_config["widthMin"] = str(widthMin)
		_config["heightMin"] = str(heightMin)
		_config["widthMax"] = str(widthMax)
		_config["heightMax"] = str(heightMax)
		_config["thresh_binary_type"] = thresh_binary_type
		with open('config.ini', 'w') as configfile:    # save
			self.config.write(configfile)
		print ("Save")
		#更新介面
		self.view.update()
	#載入設定檔
	def loadValue(self):
		
		imageType = self.comboBox.currentText()
		imageType = self.Ani[imageType]
		_config = self.config[imageType]
		areaX_Start, areaY_Start, areaX_End, areaY_End = [
			int(value) for value in _config["area"].split(",")]
		threshValue = int(_config["threshValue"])
		self.threshValuebar.setValue(threshValue)

		self.areaX_Start.setValue(areaX_Start)
		self.areaX_End.setValue(areaX_End)
		self.areaY_Start.setValue(areaY_Start)
		self.areaY_End.setValue(areaY_End)


		widthMin = int(_config["widthMin"])
		heightMin = int(_config["heightMin"])
		widthMax = int(_config["widthMax"])
		heightMax = int(_config["heightMax"])
		#輪廓框區域限制
		self.widthMin.setValue(widthMin)
		self.heightMin.setValue(heightMin)
		self.widthMax.setValue(widthMax)
		self.heightMax.setValue(heightMax)

		#圖像色彩反相
		if _config["thresh_binary_type"] == "THRESH_BINARY_INV":
			self.checkboxValue.setChecked(True)
		else:
			self.checkboxValue.setChecked(False)

		#更新介面
		self.view.update()
		#顯示新圖片	
		try:
			boundle, imageProcessDone, secondSplitImg = imageProcess(img=self.img,
                                                            threshValue=threshValue,
                                                            area=self.area,
                                                            THRESH_BINARY_TYPE=self.TYPE,
                                                            columnLength=self.columnLength,
                                                            imageType=self.imageType,
                                                            widthMin=widthMin,
                                                            heightMin=heightMin,
                                                            widthMax=widthMax,
                                                            heightMax=heightMax)
			# 顯示圖片
			cv2.imshow('secondSplitImg', secondSplitImg)

			cv2.waitKey(1)
		except Exception as e:
			print(traceback.format_exc())
			print(e)
			pass
	def valuechange(self):
		imageType = self.comboBox.currentText()
		threshValue = self.threshValuebar.value()
		areaX_Start = self.areaX_Start.value()
		areaX_End = self.areaX_End.value()
		areaY_Start = self.areaY_Start.value()
		areaY_End = self.areaY_End.value()

		#輪廓框區域限制
		widthMin = self.widthMin.value()
		heightMin = self.heightMin.value()
		widthMax = self.widthMax.value()
		heightMax = self.heightMax.value()
		#圖像色彩反相
		if self.checkboxValue.isChecked():
			self.TYPE = "THRESH_BINARY_INV"
		else:
			self.TYPE = "THRESH_BINARY"
		thresh_binary_type = self.TYPE
		valueText = "imageType: {imageType}\n\
					 threshValue : {threshValue}\n\
					 areaX_Start : {areaX_Start},\
					 areaX_End : {areaX_End},\
					 areaY_Start : {areaY_Start},\
					 areaY_End : {areaY_End}\n\
					 widthMin : {widthMin},\
					 heightMin : {heightMin},\
					 widthMax : {widthMax},\
					 heightMax : {heightMax},".format(imageType=imageType, threshValue=threshValue, 																							areaX_Start=areaX_Start,
														areaY_Start = areaY_Start,
														areaX_End = areaX_End,
														areaY_End = areaY_End,
														widthMin = widthMin,
														heightMin = heightMin,
														widthMax = widthMax,
														heightMax = heightMax)
																							





		# self.valueTextLabel.setText(valueText)
		#（left, upper, right, lower）
		#(x_start,y_start,x_end,y_end)
		self.area = (areaX_Start, areaY_Start , areaX_End, areaY_End)
		print(self.area)
	
		try:
			boundle, imageProcessDone, secondSplitImg = imageProcess(img=self.img,
																	 threshValue=threshValue,
																	 area=self.area,
																	 THRESH_BINARY_TYPE = self.TYPE,
																	 columnLength=self.columnLength,
																	 imageType=self.imageType,
																	 widthMin=widthMin,
																	 heightMin=heightMin,
																	 widthMax=widthMax,
																	 heightMax=heightMax)
			# 顯示圖片
			cv2.imshow('secondSplitImg', secondSplitImg)

			cv2.waitKey(1)
			self.resize(300, 100)

		except Exception as e:
			print(traceback.format_exc())
			print (e)
			pass
		# plt.imshow(imageProcessDone)
		# plt.title('imageProcessDone')
		# plt.show()

	def createQSliderBar(self, callbackfunction, currentValue=20, max_value=255, labelText = ""):
		ll = QLabel(labelText)
		ll.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(ll)
		#設定水平方向顯示
		sl = QSlider(Qt.Horizontal)
		#設定最小值
		sl.setMinimum(0)
		#設定最大值
		sl.setMaximum(max_value)
		#設定步長
		sl.setSingleStep(1)
		#設定當前值
		sl.setValue(currentValue)
		#設定在水平滑塊下方繪製刻度線
		sl.setTickPosition(QSlider.TicksBelow)
		#設定刻度間隔
		sl.setTickInterval(5)
		self.layout.addWidget(sl)
		sl.valueChanged.connect(callbackfunction)
		self.setLayout(self.layout)
		return sl

	def createCheckbox(self,callback):
		checkBox = QCheckBox("THRESH_BINARY_INV")
		checkBox.setChecked(True)
		checkBox.stateChanged.connect(callback)
		self.layout.addWidget(checkBox)
		self.setLayout(self.layout)
		return checkBox


view = None
if __name__ == '__main__':
	app = QApplication(sys.argv)
	view = Slider()
	view.show()
	
	sys.exit(app.exec_())
