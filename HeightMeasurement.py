import cv2 as cv
import numpy as np
import glob

defaultColor = (0, 255, 0)
defaultThickness = 2
fontColor = (255, 0, 0)
fontFace = None
fontScale = 1
pointColor = (0, 0, 255)
pointRadius = 5
labelWidth = 40

givenSize = 26
calculatedSizes = []
unit = "cm"
imgPtNames = ["c1", "c2", "c3", "c4", "vx",
              "vy", "b", "r", "b0", "t0", "v", "t"]
imgFilenames = glob.glob("./data/table_bottle_??.jpg")
winname = "Height Measurement"
cv.namedWindow(winname, cv.WINDOW_AUTOSIZE)


def calculateVanishingPoint(pt1, pt2, pt3, pt4):
    cross1 = np.cross(a=np.array([pt1[0], pt1[1], 1]),
                      b=np.array([pt2[0], pt2[1], 1]))
    cross2 = np.cross(a=np.array([pt3[0], pt3[1], 1]),
                      b=np.array([pt4[0], pt4[1], 1]))
    cross3 = np.cross(a=cross1, b=cross2)
    cross3 = cross3 / cross3[2]
    return cross3[:2]


def calculateIntersection(pt1, pt2, pt3, pt4):
    # solving pt1 + s1(pt1 - pt2) = pt3 + s2(pt3 - pt4)
    coefficientMatrix = np.stack((pt1 - pt2, -(pt3 - pt4)), axis=1)
    ordinateValues = pt3 - pt1
    s = np.linalg.solve(coefficientMatrix, ordinateValues)
    return pt1 + s[0] * (pt1 - pt2)


def drawPoint(img, center, label):
    cv.circle(img, center=center, radius=pointRadius,
              color=pointColor, thickness=-1)
    cv.putText(img=img, text=label, org=center + np.array([10, 10]), fontFace=fontFace,
               fontScale=fontScale, color=fontColor, thickness=defaultThickness)


def drawLine(img, pt1, pt2):
    pt1 = pt1.astype(np.int32)
    pt2 = pt2.astype(np.int32)
    cv.line(img=img, pt1=pt1, pt2=pt2, color=defaultColor,
            thickness=defaultThickness)


def drawMeasurementLine(img, pt1, pt2, value):
    pt1 = pt1.astype(np.int32)
    pt2 = pt2.astype(np.int32)
    xMax = max(pt1[0], pt2[0])
    cv.line(img=img, pt1=pt1, pt2=(
        xMax + 30, pt1[1]), color=defaultColor, thickness=defaultThickness)
    cv.line(img=img, pt1=pt2, pt2=(
        xMax + 30, pt2[1]), color=defaultColor, thickness=defaultThickness)
    cv.line(img=img, pt1=(xMax + 20, pt1[1]), pt2=(xMax + 20,
            pt2[1]), color=defaultColor, thickness=defaultThickness)
    cv.putText(img=img, text="{0}{1}".format(value, unit), org=(xMax + 25, (pt1[1] + pt2[1]) // 2), fontFace=fontFace,
               fontScale=fontScale, color=fontColor, thickness=defaultThickness)


def fitImage(img, imgPts):
    height, width, _ = img.shape
    imgPtsCopy = np.array(imgPts, dtype=np.int32)
    minX = min(min(*imgPtsCopy[:, 0]) - pointRadius, 0)
    maxX = max(max(*imgPtsCopy[:, 0]) + pointRadius + labelWidth, width)
    minY = min(min(*imgPtsCopy[:, 1]) - pointRadius, 0)
    maxY = max(max(*imgPtsCopy[:, 1]) + pointRadius, height)

    # calculate new width, height and offset for the original image
    newWidth = maxX - minX
    newHeight = maxY - minY
    offset = (-minX, -minY)

    # adapt coordinates of image points to the offset
    for i in range(len(imgPtsCopy)):
        imgPtsCopy[i] += offset

    # define new image and draw original image onto it
    newImg = np.zeros((newHeight, newWidth, 3), np.uint8)
    newImg[offset[1]:offset[1] + height, offset[0]:offset[0] + width, :] = img

    # redraw vanishing points and lines towards vanishing points
    drawPoint(img=newImg, center=imgPtsCopy[4], label=imgPtNames[4])
    drawPoint(img=newImg, center=imgPtsCopy[5], label=imgPtNames[5])
    drawPoint(img=newImg, center=imgPtsCopy[10], label=imgPtNames[10])
    drawLine(img=newImg, pt1=min(*imgPtsCopy[[4, 5, 10]], key=lambda v: v[1]),
             pt2=max(*imgPtsCopy[[4, 5, 10]], key=lambda v: v[1]))
    drawLine(img=newImg, pt1=imgPtsCopy[0], pt2=imgPtsCopy[4])
    drawLine(img=newImg, pt1=imgPtsCopy[2], pt2=imgPtsCopy[4])
    drawLine(img=newImg, pt1=imgPtsCopy[0], pt2=imgPtsCopy[5])
    drawLine(img=newImg, pt1=imgPtsCopy[1], pt2=imgPtsCopy[5])
    drawLine(img=newImg, pt1=imgPtsCopy[8], pt2=imgPtsCopy[10])
    drawLine(img=newImg, pt1=imgPtsCopy[9], pt2=imgPtsCopy[10])

    # resize new image and fit it into the original image shape
    factor = min(height / newHeight, width / newWidth)
    newImgResized = cv.resize(src=newImg, dsize=(0, 0), fx=factor, fy=factor)
    img = np.zeros(img.shape, np.uint8)
    newHeightResized, newWidthResized, _ = newImgResized.shape
    offset = ((width - newWidthResized) // 2, (height - newHeightResized) // 2)
    img[offset[1]:offset[1] + newHeightResized, offset[0]:offset[0] + newWidthResized, :] = newImgResized
    return img


# calculate mug size for every image
for imageFilename in imgFilenames:
    currentImg = cv.resize(src=cv.imread(
        filename=imageFilename), dsize=(0, 0), fx=0.5, fy=0.5)
    currentImgPts = np.empty(shape=(12, 2), dtype=np.float32)
    currentImgPtsCount = 0

    def hndMouse(event, x, y, flags, userData):
        global currentImg, currentImgPts, currentImgPtsCount
        if event == cv.EVENT_LBUTTONDOWN and currentImgPtsCount < len(currentImgPts):
            # on click add new image point and visualize it
            currentImgPts[currentImgPtsCount] = np.array([x, y])
            drawPoint(img=currentImg, center=(x, y),
                      label=imgPtNames[currentImgPtsCount])
            currentImgPtsCount += 1

            if currentImgPtsCount == 4:
                # index 0-3 := table corners, index 4-5 := vanishing points
                currentImgPts[currentImgPtsCount] = calculateVanishingPoint(
                    *currentImgPts[:4])
                currentImgPts[currentImgPtsCount +
                              1] = calculateVanishingPoint(*currentImgPts[[0, 2, 1, 3]])
                currentImgPtsCount += 2
                # draw lines towards vanishing points and vanishing line
                drawLine(currentImg, *currentImgPts[[0, 4]])
                drawLine(currentImg, *currentImgPts[[2, 4]])
                drawLine(currentImg, *currentImgPts[[0, 5]])
                drawLine(currentImg, *currentImgPts[[1, 5]])
                drawLine(currentImg, *currentImgPts[[4, 5]])

            if currentImgPtsCount == 8:
                # index 6 := bottle bottom, index 7 := bottle top
                drawMeasurementLine(
                    currentImg, *currentImgPts[[6, 7]], value=givenSize)

            if currentImgPtsCount == 10:
                # i 8 := mug bottom, i 9 := mug top, i 10 := new vanishing point, i 11 := t
                currentImgPts[currentImgPtsCount] = calculateIntersection(
                    *currentImgPts[[4, 5, 6, 8]])
                currentImgPts[currentImgPtsCount +
                              1] = calculateIntersection(*currentImgPts[[6, 7, 9, 10]])
                currentImgPtsCount += 2
                # i 11 := t, i 6 := b, i 7 := r
                vz = calculateVanishingPoint(*currentImgPts[[6, 7, 8, 9]])
                imageCrossRatio = (
                    np.linalg.norm(currentImgPts[11] - currentImgPts[6]) *
                    np.linalg.norm(vz - currentImgPts[7])
                ) / (
                    np.linalg.norm(currentImgPts[7] - currentImgPts[6]) *
                    np.linalg.norm(vz - currentImgPts[11])
                )
                calculatedSize = givenSize * imageCrossRatio
                drawMeasurementLine(
                    currentImg, *currentImgPts[[8, 9]], value=calculatedSize)
                print(calculatedSize)
                calculatedSizes.append(calculatedSize)

                # resize image to display vanising points & vanishing line
                currentImg = fitImage(currentImg, currentImgPts)

            cv.imshow(winname=winname, mat=currentImg)

    cv.imshow(winname=winname, mat=currentImg)
    cv.setMouseCallback(window_name=winname, on_mouse=hndMouse)

    while True:
        key = cv.waitKey(delay=10)
        # quit program
        if key == ord("q"):
            exit()
        # next image
        if key == ord("n"):
            break

# print average of all calculated mug sizes
print(np.sum(calculatedSizes) / len(calculatedSizes))
