import cv2
import time

from datetime import datetime


def Record():
    Start_time = time.time()
    
    # 輸出結果
    print(Start_time)
    # 選擇第1隻攝影機
    cap = cv2.VideoCapture(0)
    
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
            filename = "{hour}_{min}_{sec}".format(
                hour=time.localtime().tm_hour, min=time.localtime().tm_min, sec=time.localtime().tm_sec)
            cv2.imwrite("C:\\Users\\NO NAME\\Desktop\\out\\"+filename+".jpg", frame)
            i = 0

        #現在時間與啟動錄影時間>100秒就離開
        now = time.time()
        if now - Start_time > 100:
            break
    # 釋放攝影機
    cap.release()
    # 關閉所有 OpenCV 視窗
    cv2.destroyAllWindows()


while True:
    # 轉換為 struct_time 格式的本地時間
    result = time.localtime(time.time())

    # 輸出結果
    print("目前分鐘:" + str(result[4]))

    #可以被5分鐘整除
    time.sleep(1)
    if result[4] % 5 == 0:
        Record()
