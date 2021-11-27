import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from PIL import Image, ImageDraw, ImageFont

cap = cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_PLAIN

while True:
    _, frame = cap.read()

    decodedObjects = pyzbar.decode(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    for obj in decodedObjects:

        (x, y, w, h) = obj.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        barcodeData = obj.data.decode("utf-8")
        barcodeType = obj.type

        cv2.putText(frame, str(obj.data), (x, y-10), font, 2,
                    (0, 255, 0), 3)
        print(barcodeData, barcodeType)
    cv2.imshow("QR Scanner", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.deqstroyAllWindows()