import cv2
import time

from datetime import datetime


def Record():
    Start_time = time.time()
    
    # 輸出結果
    print(Start_time)
    # 選擇第1隻攝影機
    cap = cv2.VideoCapture(0)
    # width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # float
    # height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # float

    # # fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # # fourcc = cv2.VideoWriter_fourcc('F', 'L', 'V', '1')
    # # fourcc = cv2.VideoWriter_fourcc('I', '4', '2', '0')
    # fourcc = 0x00000021
    # fps = cap.get(cv2.CAP_PROP_FPS)
    # #每五分鐘拍一段90秒影像
    # out = cv2.VideoWriter(filename + '.mp4', fourcc, 30,
    #                       (int(width), int(height)))

    i = 0
    while(True):
        # 從攝影機擷取一張影像
        ret, frame = cap.read()

        # 顯示圖片
        cv2.imshow('frame', frame)

        cv2.waitKey(1)
        i += 1
        #每0.5秒截一次圖
        if i > 15:
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
