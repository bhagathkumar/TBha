import time
from datetime import datetime

import cv2 as cv2

video = cv2.VideoCapture("/home/administrator/Videos/f.mp4")

count = 1
imgc = 1


dpath="/work/work1/out/"

a=input("press a key")
fourcc = cv2.VideoWriter_fourcc('F','M','p','4')
w = cv2.VideoWriter("makka.mp4", fourcc, 24, (704, 240),1)

while True:
    count += 1
    check, frame = video.read()
    motion = 0
    motion = 1
    frame=cv2.resize(frame,(1080,720))
    cv2.imshow("Gray Frame", frame)
    print(count)
    if(count > 100):
        print("24th image write-count no",imgc)
        cv2.imwrite(dpath+"img"+str(imgc)+".jpg", frame)
        w.write(frame)
        imgc += 1
        count = 0
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
w.cvReleaseVideoWriter()
video.release()
cv2.destroyAllWindows()

