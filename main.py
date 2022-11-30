import cv2
import time
from faceDetector import faceDetector
import serial

cap = cv2.VideoCapture(0)
time.sleep(2)

arduino = serial.Serial(port='COM11', baudrate=115200)

modelFile = "models/opencv_face_detector.pb"
configFile = "models/config.pbtxt"
net = cv2.dnn.readNet(config=configFile, model=modelFile,
                      framework='TensorFlow')

detector = faceDetector(net)
detectionEnabled = True

while True:
    try:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if ret:
            frame = cv2.resize(frame, (640, 480))

            if(detectionEnabled):
                output, boxes, center = detector.detectFaceOpenCVDnn(frame)
                if(center != []):
                    print(int(center[0] * 180 / 600))
                    servoPos = int(center[0] * 180 / 600)
                    arduino.write(bytes(str(180 - servoPos), 'utf-8'))
                    time.sleep(1/30)

            cv2.imshow('face detection with DNN', frame)

    except Exception as e:
        print(f'exc: {e}')
        pass

    key = cv2.waitKey(1) & 0xFF
    if key == ord("f"):
        detectionEnabled = not detectionEnabled

    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
