#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Recaptcha_Lib import *
from PIL import Image
class Slider(QWidget):
	def __init__(self,parent=None):
		super().__init__(parent)
		self.area = (165, 320, 180, 385)

		self.setWindowTitle("image process tool")
		self.resize(300,100)
		
		self.layout = QVBoxLayout()
		self.ll = QLabel("threshValue")
		self.ll.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.ll)

		#create 二值化拉桿
		self.threshValuebar = self.createQSliderBar(callbackfunction = self.valuechange,max_value = 255)
		
		
		self.ll = QLabel("areaX_Start")
		self.ll.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.ll)
		self.areaX_Start = self.createQSliderBar(callbackfunction = self.valuechange,currentValue =self.area[0],max_value = 1000)
		
		self.ll = QLabel("areaX_End")
		self.ll.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.ll)
		self.areaX_End = self.createQSliderBar(callbackfunction=self.valuechange,currentValue =self.area[1],max_value = 1000)
		
		self.ll = QLabel("areaY_Start")
		self.ll.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.ll)
		self.areaY_Start = self.createQSliderBar(callbackfunction=self.valuechange,currentValue =self.area[2],max_value = 1000)
											  #create 二值化拉桿
		
		self.ll = QLabel("areaY_End")
		self.ll.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.ll)
		self.areaY_End = self.createQSliderBar(callbackfunction = self.valuechange,currentValue =self.area[3],max_value = 1000)

		self.checkboxValue = self.createCheckbox(callback=self.readCheckboxValue)
		self.TYPE = "THRESH_BINARY_INV"
		self.imageType = 0
		self.columnLength = 20
		self.img = Image.open(str(self.imageType) + '_0.jpg')
		ll = QLabel("Status")
		ll.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(ll)
		self.valueTextLabel = QLabel("")
		self.valueTextLabel.setAlignment(Qt.AlignCenter)
		self.layout.addWidget(self.valueTextLabel)
	def valuechange(self):
		threshValue = self.threshValuebar.value()
		areaX_Start = self.areaX_Start.value()
		areaX_End = self.areaX_End.value()
		areaY_Start = self.areaY_Start.value()
		areaY_End = self.areaY_End.value()
		valueText = "threshValue : {threshValue},areaX_Start : {areaX_Start},areaX_End : {areaX_End},areaY_Start : {areaY_Start},areaY_End : {areaY_End}".format(threshValue = threshValue,
																							areaX_Start = areaX_Start,
																							areaY_Start = areaY_Start,
																							areaX_End = areaX_End,
																							areaY_End = areaY_End)
																							
		
		self.valueTextLabel.setText(valueText)
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
															imageType=self.imageType)
			# 顯示圖片
			cv2.imshow('secondSplitImg', secondSplitImg)

			cv2.waitKey(1)
		except:
			pass
		# plt.imshow(imageProcessDone)
		# plt.title('imageProcessDone')
		# plt.show()

	def createQSliderBar(self, callbackfunction, currentValue=20, max_value=255):
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
	def readCheckboxValue(self):
		if self.checkboxValue.isChecked():
			self.TYPE = "THRESH_BINARY_INV"
		else:
			self.TYPE = "THRESH_BINARY"

		print(self.TYPE)
if __name__ == '__main__':
	app = QApplication(sys.argv)
	demo = Slider()
	demo.show()
	sys.exit(app.exec_())
