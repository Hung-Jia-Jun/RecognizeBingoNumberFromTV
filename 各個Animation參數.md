各個Animation參數

彩球
area = (180, 300,
        600, 400)
ret,thresh1 = cv2.threshold(img,210,255,cv2.THRESH_BINARY)

魚
#二值化
ret,thresh1 = cv2.threshold(img,60,255,cv2.THRESH_BINARY)

打地鼠(可能會有雜值出現)
#二值化
ret,thresh1 = cv2.threshold(img,130,255,cv2.THRESH_BINARY)

舞龍舞獅
#二值化反轉
ret,thresh1 = cv2.threshold(img,200,255,cv2.THRESH_BINARY_INV)

動物農場
#二值化
ret,thresh1 = cv2.threshold(img,130,255,cv2.THRESH_BINARY_INV)