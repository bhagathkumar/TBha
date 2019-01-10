import numpy as np
import cv2

threshold = 700  # set threshold as low to detect minor change and vice versa.
font = cv2.FONT_HERSHEY_SIMPLEX


def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)


video_path = "/home/makka/Videos/thf.mp4"
dpath="/work/work1/out/"
cam = cv2.VideoCapture(video_path)
ct = 2

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

frame = 0
while True:
    if(ct == 140):
        ct = 1
    cv2.imshow("out", diffImg(t_minus, t, t_plus))
    frame = frame + 1
    diff = diffImg(t_minus, t, t_plus)
    diff = cv2.GaussianBlur(diff, (7, 7), 0)
    diff[diff > 3] = 255  # Read next image
    diff[diff < 3] = 0
    count = np.count_nonzero(diff == 255)
    t_minus = t
    t = t_plus
    Image = cam.read()[1]
    time_stamp = cam.get(cv2.CAP_PROP_POS_MSEC) / 1000
    time_stamp_text = "{:3f} sec".format(time_stamp)
    t_plus = cv2.cvtColor(Image, cv2.COLOR_RGB2GRAY)
    disp_image = Image
    if count > threshold:
        print(ct)
        if(ct == 1):
            print("wr", ct)
            cv2.putText(disp_image, "Movement Detected", (70, 70), font, 1, (255, 0, 255), 1,
                        cv2.LINE_AA)
            cv2.imwrite(dpath+"img"+time_stamp_text+"_"+str(frame)+".jpg", disp_image)
            ct += 1
        else:
            ct += 1

    cv2.imshow("out", disp_image)
    key = cv2.waitKey(10)
    if key == 27:
        break
