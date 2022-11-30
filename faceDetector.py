import cv2


class faceDetector:
    def __init__(self, net):
        self.__net = net

    def detectFaceOpenCVDnn(self, frame, threshold=0.7):
        frameHeight = frame.shape[0]
        frameWidth = frame.shape[1]
        blob = cv2.dnn.blobFromImage(
            frame, 1.0, (300, 300), [104, 117, 123], True, False,
        )
        center = []

        self.__net.setInput(blob)
        detections = self.__net.forward()
        boxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > threshold:
                x1 = int(detections[0, 0, i, 3] * frameWidth)
                y1 = int(detections[0, 0, i, 4] * frameHeight)
                x2 = int(detections[0, 0, i, 5] * frameWidth)
                y2 = int(detections[0, 0, i, 6] * frameHeight)
                center = [int((x1+x2)/2), int((y1+y2)/2)]
                boxes.append([x1, y1, x2, y2])
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 0),
                    int(round(frameHeight / 150)),
                    8,
                )
                cv2.circle(frame, (center[0], center[1]),
                           4, (0, 0, 255), -1)
        return frame, boxes, center
