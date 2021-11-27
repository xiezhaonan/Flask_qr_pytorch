import cv2

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)


cv2.QRCodeDetector()

while True:
    _, img = cap.read()

    data, box, _ = cv2.QRCodeDetector().detectAndDecode(img)
    # print(box)

    if box is not None:

        cv2.line(img, tuple(box[0][0]), tuple(box[1][0]), color=(0, 255, 0), thickness=2)
        cv2.line(img, tuple(box[1][0]), tuple(box[2][0]), color=(0, 255, 0), thickness=2)
        cv2.line(img, tuple(box[2][0]), tuple(box[3][0]), color=(0, 255, 0), thickness=2)
        cv2.line(img, tuple(box[3][0]), tuple(box[4][0]), color=(0, 255, 0), thickness=2)


    if data:
        print("data is", data)

    cv2.imshow("摄像头:", img)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
