import pyodbc
import cv2
import numpy as np
import os

def connect_db():
    conn = pyodbc.connect(
    "Driver={SQL Server};"
    "Server=DESKTOP-0C8O8RG\SQLEXPRESS01;"
    "Database=NDKM;"
    "Trusted_Connection=yes"
    )
    return conn

def check(key):
    curr = connect_db().cursor()
    curr.execute("select*from User_Face where ID_user = '{0}'".format(key))
    d=0
    for i in curr:
        d = d+1
    if d==0:
        return True
    return False

def insert(id, name, adress):
    if check(id):
        cursor = connect_db().cursor()
        cursor.execute("insert into User_Face values('{0}','{1}','{2}')".format(id, name, adress))
        cursor.commit()
        print('Thêm thành công!')
        connect_db().close()
    else:
        print('Đã tồn tại ' + id)

id = input('Nhập ID: ')
name = input('Nhập tên: ')
address = input('Nhập địa chỉ: ')
insert(id, name, address)

face = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cap = cv2.VideoCapture(0)
index = 0
while True:
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray,1.3,5)
    for(x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x + w, y + h), (0,225,0), 2)
        if not os.path.exists('dataSet'):
            os.makedirs('dataSet')
        index += 1
        cv2.imwrite('dataSet/User.{0}.{1}.jpg'.format(id,index), gray[y:y + h,x:x + w])

    cv2.imshow("LE HUNG FACE TOOLS",frame)
    cv2.waitKey(1)
    if index > 400:
        break

cap.release()
cv2.destroyAllWindows()