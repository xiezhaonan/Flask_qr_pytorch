import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
from PIL import Image, ImageDraw, ImageFont

img_path = "gree1.jpg"

font = cv2.FONT_HERSHEY_PLAIN

frame = cv2.imread(img_path)

decodedObjects = pyzbar.decode(frame)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
for obj in decodedObjects:

    (x, y, w, h) = obj.rect
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    barcodeData = obj.data.decode("utf-8")
    barcodeType = obj.type

    result = cv2.putText(frame, str(obj.data), (x, y-10), font, 2,(0, 255, 0), 3)
    print(barcodeData, barcodeType)
print(x, y, w, h)
# frame.save('02.jpg', 'jpeg')
im = Image.fromarray(result)
im.save("result.jpg", 'jpeg')
cv2.imshow("result",result)
cv2.waitKey()