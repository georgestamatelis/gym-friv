import cv2
while True:
    key = cv2.waitKey(10)# & 0xFF
    if key!=-1:
        print("key=",key)