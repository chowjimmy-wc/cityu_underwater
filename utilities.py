import cv2
import numpy as np
 
def thresholding(img):
    imgHsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lowerWhite = np.array(&#91;80,0,0])
    upperWhite = np.array(&#91;255,160,255])
    maskWhite = cv2.inRange(imgHsv,lowerWhite,upperWhite)
    return maskWhite
 
def warpImg(img,points,w,h,inv = False):
    pts1 = np.float32(points)
    pts2 = np.float32(&#91;&#91;0,0],&#91;w,0],&#91;0,h],&#91;w,h]])
    if inv:
        matrix = cv2.getPerspectiveTransform(pts2, pts1)
    else:
        matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imgWarp = cv2.warpPerspective(img,matrix,(w,h))
    return imgWarp
 
def nothing(a):
    pass
 
def initializeTrackbars(intialTracbarVals,wT=480, hT=240):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 360, 240)
    cv2.createTrackbar("Width Top", "Trackbars", intialTracbarVals&#91;0],wT//2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intialTracbarVals&#91;1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intialTracbarVals&#91;2],wT//2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intialTracbarVals&#91;3], hT, nothing)
 
def valTrackbars(wT=480, hT=240):
    widthTop = cv2.getTrackbarPos("Width Top", "Trackbars")
    heightTop = cv2.getTrackbarPos("Height Top", "Trackbars")
    widthBottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    heightBottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32(&#91;(widthTop, heightTop), (wT-widthTop, heightTop),
                      (widthBottom , heightBottom ), (wT-widthBottom, heightBottom)])
    return points
 
def drawPoints(img,points):
    for x in range(4):
        cv2.circle(img,(int(points&#91;x]&#91;0]),int(points&#91;x]&#91;1])),15,(0,0,255),cv2.FILLED)
    return img
 
def getHistogram(img,minPer=0.1,display= False,region=1):
 
    if region ==1:
        histValues = np.sum(img, axis=0)
    else:
        histValues = np.sum(img&#91;img.shape&#91;0]//region:,:], axis=0)
 
    #print(histValues)
    maxValue = np.max(histValues)
    minValue = minPer*maxValue
 
    indexArray = np.where(histValues >= minValue)
    basePoint = int(np.average(indexArray))
    #print(basePoint)
 
    if display:
        imgHist = np.zeros((img.shape&#91;0],img.shape&#91;1],3),np.uint8)
        for x,intensity in enumerate(histValues):
            cv2.line(imgHist,(x,img.shape&#91;0]),(x,img.shape&#91;0]-intensity//255//region),(255,0,255),1)
            cv2.circle(imgHist,(basePoint,img.shape&#91;0]),20,(0,255,255),cv2.FILLED)
        return basePoint,imgHist
 
    return basePoint
 
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray&#91;0])
    rowsAvailable = isinstance(imgArray&#91;0], list)
    width = imgArray&#91;0]&#91;0].shape&#91;1]
    height = imgArray&#91;0]&#91;0].shape&#91;0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray&#91;x]&#91;y].shape&#91;:2] == imgArray&#91;0]&#91;0].shape &#91;:2]:
                    imgArray&#91;x]&#91;y] = cv2.resize(imgArray&#91;x]&#91;y], (0, 0), None, scale, scale)
                else:
                    imgArray&#91;x]&#91;y] = cv2.resize(imgArray&#91;x]&#91;y], (imgArray&#91;0]&#91;0].shape&#91;1], imgArray&#91;0]&#91;0].shape&#91;0]), None, scale, scale)
                if len(imgArray&#91;x]&#91;y].shape) == 2: imgArray&#91;x]&#91;y]= cv2.cvtColor( imgArray&#91;x]&#91;y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = &#91;imageBlank]*rows
        hor_con = &#91;imageBlank]*rows
        for x in range(0, rows):
            hor&#91;x] = np.hstack(imgArray&#91;x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray&#91;x].shape&#91;:2] == imgArray&#91;0].shape&#91;:2]:
                imgArray&#91;x] = cv2.resize(imgArray&#91;x], (0, 0), None, scale, scale)
            else:
                imgArray&#91;x] = cv2.resize(imgArray&#91;x], (imgArray&#91;0].shape&#91;1], imgArray&#91;0].shape&#91;0]), None,scale, scale)
            if len(imgArray&#91;x].shape) == 2: imgArray&#91;x] = cv2.cvtColor(imgArray&#91;x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver
