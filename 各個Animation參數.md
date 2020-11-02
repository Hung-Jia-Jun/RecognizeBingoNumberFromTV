各個Animation參數

彩球
area = (50, 186,150, 380)
ret,thresh1 = cv2.threshold(img,215,255,cv2.THRESH_BINARY_INV)

魚
area = (130, 300,
        580, 400)
#二值化
ret,thresh1 = cv2.threshold(img,50,255,cv2.THRESH_BINARY)

打地鼠(可能會有雜值出現)
area = (187, 340,
        580, 400)
#二值化
ret,thresh1 = cv2.threshold(img,170,255,cv2.THRESH_BINARY_INV)

舞龍舞獅
area = (187, 300,
        580, 380)
#二值化
ret,thresh1 = cv2.threshold(img,180,255,cv2.THRESH_BINARY_INV)

動物農場
area = (180, 340,
        580, 400)
#二值化
ret,thresh1 = cv2.threshold(img,100,255,cv2.THRESH_BINARY_INV)

套圈圈
area = (50, 186,
        150, 380)
#二值化
ret,thresh1 = cv2.threshold(img,160,255,cv2.THRESH_BINARY_INV)

表格顯示
#二值化
area = (200, 110,
        580, 400)
ret,thresh1 = cv2.threshold(img,100,255,cv2.THRESH_BINARY_INV)

賽車
area = (50, 210,
        150, 390)
ret,thresh1 = cv2.threshold(img,230,255,cv2.THRESH_BINARY_INV)
