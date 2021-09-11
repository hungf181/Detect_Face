import cv2
import numpy as np
import os
import pyodbc
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()
face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

recognizer.read('E:/Python/Recognizer/trainning.yml')
def getProfile(id):
    conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=DESKTOP-0C8O8RG\SQLEXPRESS01;"
    "Database=NDKM;"
    "Trusted_Connection=yes"
    )
    cursor = conn.execute('select*from User_Face where ID_user = ' + str(id))
    profile = None
    for row in cursor:
        profile = row
    conn.close()
    return profile

cap = cv2.VideoCapture(0)
while True:

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray)

    for(x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        id, dochinhxac = recognizer.predict(roi_gray)
        if dochinhxac < 40:
            profile = getProfile(id)
            if profile != None:
                cv2.rectangle(frame, (x,y), (x + w, y + h),(0,225,0), 2)
                cv2.putText(frame,'ID User: '+str(profile[0]), (x,y+h+25), cv2.FONT_HERSHEY_SIMPLEX,0.7,((0,0,255)),1)
                cv2.putText(frame,'Name: '+str(profile[1]), (x,y+h+50), cv2.FONT_HERSHEY_SIMPLEX,0.7,((0,0,255)),1)
                cv2.putText(frame,'Address: '+str(profile[2]), (x,y+h+75), cv2.FONT_HERSHEY_SIMPLEX,0.7,((0,0,255)),1)

        else:
            cv2.rectangle(frame, (x,y), (x + w, y + h),(0,0,225), 2)
            cv2.putText(frame,"Unknow!!!",(x,y+h+20), cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,225),1)
           
    cv2.imshow("LE HUNG FACE TOOLS",frame)
    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
#'ID User:' + str(profile[0])+'\nTên User:'+str(profile[1])+'\nĐịa chỉ:'+str(profile[2])