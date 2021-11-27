import numpy as np
import cv2

if __name__ == "__main__":
    #读取图像
    filepath = "./123131.jpg"
    img = cv2.imread(filepath)
    print(np.shape(img))
    imgHeight, imgWidth, channel = np.shape(img)
    # 转灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 转换灰色

    # 计算梯度
    ddepth = cv2.CV_32F

    gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-10)
    gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-10)

    gradient = cv2.subtract(gradX, gradY)
    gradient = cv2.convertScaleAbs(gradient)

    # 模糊和二值化
    blurred = cv2.blur(gradient, (5,5))
    (_, thresh) = cv2.threshold(blurred, 185, 255, cv2.THRESH_BINARY)

    # 形态学处理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    #膨胀和腐蚀操作
    closed = cv2.erode(closed, None, iterations=5)
    closed = cv2.dilate(closed, None, iterations=5)

    #查找连通域
    cnts = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    #绘制轮廓
    #cv2.drawContours(img,cnts[1],-1,(0,0,255),1,lineType=cv2.LINE_AA)  #绘制实际轮廓

    for i in range(0,len(cnts[1])):
        rect = cv2.minAreaRect(cnts[1][i]) # 得到最小外接矩形（中心(x,y), (宽,高), 旋转角度）
        w,h=rect[1]
        if w/h>4 or h/w>4 or h>imgWidth/5 or w>imgWidth/5: #去除长宽比超过4倍的矩形框
            continue

        box = cv2.boxPoints(rect)
        box = np.int0(box)
        # 画出来
        cv2.drawContours(img, [box], 0, (255, 0, 0), 1)

    cv2.imshow("Temp Image",img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
