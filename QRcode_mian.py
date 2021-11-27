import os
import io
import json

import numpy
import torch
import time
import cv2
import pyzbar.pyzbar as pb
from PIL import Image
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 解决跨域问题
# now = ""

font = cv2.FONT_HERSHEY_PLAIN

def QRcode(frame):
    try:
        now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
        barcodeData = []
        barcodeType = []
        c = []
        decodedObjects= pb.decode(frame)
        frame = numpy.array(frame)
        for obj in decodedObjects:
            # print("#############1")
            (x, y, w, h) = obj.rect

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            barcodeData.append(obj.data.decode("utf-8"))
            barcodeType.append(obj.type)

            result = cv2.putText(frame, str(obj.data), (x, y - 10), font, 2, (0, 255, 0), 3)

        for i in range(len(barcodeData)):
            c.append(barcodeData[i] + ' ' + barcodeType[i])
        print(c)
        im = Image.fromarray(result)

        return_info = {"result": c, "address": now}

        print(return_info)

    except Exception as e:
        return_info = {"result": [str(e)],"address": now}
    return return_info, im


@app.route("/predict", methods=["POST"])
@torch.no_grad()
def predict():
    now = time.strftime("%Y-%m-%d-%H_%M_%S", time.localtime(time.time()))
    image = request.files["file"]
    picture = image.read()
    frame = Image.open(io.BytesIO(picture))
    # barcodeData = []
    # barcodeType = []
    # info = get_prediction(image_bytes=img_bytes)
    # return jsonify(info)
    # decodedObjects = pb.decode(frame)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # print("#############11")

    final, im = QRcode(frame)
    im = im.convert('RGB')
    # cv2.imshow("result", result)
    # cv2.waitKey()
    im.save("./static/picture/"+now+".jpg", 'jpeg')
    # im.save("./static/picture/" +"result" + ".jpg", 'jpeg')
    print(now)
    # print(final)
    return final

@app.route("/", methods=["GET", "POST"])
def root():
    return render_template("QR_1.html")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)




