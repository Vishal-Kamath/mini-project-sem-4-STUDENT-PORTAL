import tkinter as tk
from tkinter import messagebox
import cv2
import os
from PIL import Image
import numpy as np
import time
from database_connection import DBHelper

#Detect face
def detect_face(student_id):
    global face_found
    face_found = False


    db_con = DBHelper()
    student = db_con.fetch_student_info(student_id)
    student_name = student[0][1] + " " + student[0][2]
    def found():
        global face_found
        face_found = True

    def draw_boundary(img, classifier, scaleFactor, minNeighbors, color, text, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        coords = []


        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y ), (x + w, y + h), (255,0,255), 2)
            cv2.rectangle(img, (x, y - 35), (x + w, y), (255,0,255), cv2.FILLED)
            id, pred = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int(100 * (1 - pred / 300))

            if confidence > 75:
                if id == int(student_id):
                    cv2.putText(img,student_name, (x + 5, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)
                    found()

            else:
                cv2.putText(img, "UNKNOWN", (x + 5, y - 5), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)

            coords = [x, y, w, h]

    def recognize(img, clf, faceCascade):
        draw_boundary(img, faceCascade, 1.1, 10, (255, 255, 255), "Face", clf)
        return img



    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    clf = cv2.face.LBPHFaceRecognizer_create()
    clf.read("classifier.xml")

    video_capture = cv2.VideoCapture(0)


    t_end = time.time() + 10

    while time.time() < t_end:
        ret, img = video_capture.read()
        img = recognize(img, clf, faceCascade)
        cv2.imshow("face detection", img)


        if cv2.waitKey(1) == 13:
            break


    video_capture.release()
    cv2.destroyAllWindows()

    if not face_found:
        messagebox.showinfo("result", "face recognition unsuccessfull")
    elif face_found:
        messagebox.showinfo("result", "face recognition successfull")

    return face_found


def mark_attendance_exam(student_id, exam_id):
    if detect_face(student_id):
        db_con = DBHelper().mark_exam(student_id, exam_id)
        return True
    else:
        return False

def mark_attendance_lec(student_id, lec_id):
    if detect_face(student_id):
        db_con = DBHelper().mark_lec(student_id, lec_id)
        return True
    else:
        return False