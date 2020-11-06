# 各個Animation參數

1. ##### 格狀列表
>area = (200, 110,
        580, 400)
> #二值化
ret,thresh1 = cv2.threshold(img,100,255,cv2.THRESH_BINARY_INV)
if width<=2 or width>20 or width*height<70 \
        or width*height>400 or height <= 14 or height > 20:
        return False 
        
2. ##### 打地鼠
> area = (187, 340,
        580, 400)
> #二值化
ret,thresh1 = cv2.threshold(img,170,255,cv2.THRESH_BINARY_INV)
if width<=2 or width>20 or width*height<70 \
        or width*height>400 or height <= 14 or height > 20:
        return False 

3. ##### 動物農場
> area = (175, 340,
        580, 400)
> #二值化
ret,thresh1 = cv2.threshold(img,100,255,cv2.THRESH_BINARY_INV)
if width<=2 or width>20 or width*height<70 \
        or width*height>400 or height <= 14 or height > 20:
        return False 

4. ##### 賽車
> area = (45, 215,
        150, 410)
> #二值化
ret,thresh1 = cv2.threshold(img,230,255,cv2.THRESH_BINARY_INV)
if width<=2 or width>20 or width*height<70 \
        or width*height>400 or height <= 14 or height > 20:
        return False 

5. ##### 套圈圈
> area = (45, 190,
        125, 395)
> #二值化
ret,thresh1 = cv2.threshold(img,160,255,cv2.THRESH_BINARY_INV)
if width<=2 or width>20 or width*height<70 \
        or width*height>400 or height <= 14 or height > 20:
        return False 

6. ##### 舞龍舞獅
> area = (185, 300,
        580, 380)
> #二值化
ret,thresh1 = cv2.threshold(img,180,255,cv2.THRESH_BINARY_INV)
if width<=5 or width>20 or width*height<70 \
        or width*height>400 or height <= 14 or height > 22 or height - width < 5:
        return False 
7. ##### 彩球
> area = (170, 320,
        580, 385)
> #二值化
ret,thresh1 = cv2.threshold(img,230,255,cv2.THRESH_BINARY_INV)

8. ##### 魚
> area =  (170, 322,
        580, 390)
> #二值化
ret,thresh1 = cv2.threshold(img,57,255,cv2.THRESH_BINARY)








