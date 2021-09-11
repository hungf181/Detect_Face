import cv2
import numpy as np
import os
from PIL import Image

recognizer = cv2.face.LBPHFaceRecognizer_create()

path = 'dataSet'

def getPath(path):
    pathImages = [os.path.join(path,f) for f in os.listdir(path)]
    faces = []
    IDs = []
    for image in pathImages:
        FaceImg = Image.open(image).convert('L')
        FaceNP = np.array(FaceImg,'uint8')
        Id = int(image.split('.')[1])
        faces.append(FaceNP)
        IDs.append(Id)
        cv2.imshow('Tranning',FaceNP)
        cv2.waitKey(10)
    return faces, IDs

faces, IDs = getPath(path)

recognizer.train(faces, np.array(IDs))

if not os.path.exists('Recognizer'):
    os.makedirs('Recognizer')

recognizer.save('Recognizer/trainning.yml') 
cv2.destroyAllWindows()