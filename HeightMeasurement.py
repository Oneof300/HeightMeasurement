import cv2 as cv
import numpy as np
import glob

drawColor = (255, 0, 0)
drawThickness = 2
fontFace = None
fontScale = 0.75

givenSize = 26
calculatedSizes = []
unit = "cm"
imageFilenames = glob.glob("./data/table_bottle_??.jpg")

def calculateVanishingPoint(pt1, pt2, pt3, pt4):
  cross1 = np.cross(a = np.array([pt1[0], pt1[1], 1]), b = np.array([pt2[0], pt2[1], 1]))
  cross2 = np.cross(a = np.array([pt3[0], pt3[1], 1]), b = np.array([pt4[0], pt4[1], 1]))
  cross3 = np.cross(a = cross1, b = cross2)
  cross3 = cross3 / cross3[2]
  return cross3[:2]

def calculateIntersection(pt1, pt2, pt3, pt4):
  # solving pt1 + s1(pt1 - pt2) = pt3 + s2(pt3 - pt4)
  coefficientMatrix = np.stack((pt1 - pt2, -(pt3 - pt4)), axis = 1)
  ordinateValues = pt3 - pt1
  s = np.linalg.solve(coefficientMatrix, ordinateValues)
  return pt1 + s[0] * (pt1 - pt2)

def drawLine(img, pt1, pt2):
  pt1 = pt1.astype(np.int32)
  pt2 = pt2.astype(np.int32)
  cv.line(img = img, pt1 = pt1, pt2 = pt2, color = drawColor, thickness = drawThickness)

def drawMeasurementLine(img, pt1, pt2, value):
  pt1 = pt1.astype(np.int32)
  pt2 = pt2.astype(np.int32)
  xMax = max(pt1[0], pt2[0])
  cv.line(img = img, pt1 = pt1, pt2 = (xMax + 30, pt1[1]), color = drawColor, thickness = drawThickness)
  cv.line(img = img, pt1 = pt2, pt2 = (xMax + 30, pt2[1]), color = drawColor, thickness = drawThickness)
  cv.line(img = img, pt1 = (xMax + 20, pt1[1]), pt2 = (xMax + 20, pt2[1]), color = drawColor, thickness = drawThickness)
  cv.putText(img = img, text = "{0}{1}".format(value, unit), org = (xMax + 25, (pt1[1] + pt2[1]) // 2), fontFace = fontFace,
    fontScale = fontScale, color = drawColor, thickness = drawThickness)

def convertPnt(pt):
  return (pt[0], pt[1])

def fitImage(img, currentImgPts):
  height, width, _ = img.shape
  vanishingPts = [convertPnt(currentImgPts[4]), convertPnt(currentImgPts[5])]
  cornerPts = [convertPnt(currentImgPts[0]), convertPnt(currentImgPts[1]), convertPnt(currentImgPts[2]), convertPnt(currentImgPts[3])]

  new_min_x = round(min(min(vanishingPts)[0], 0))
  new_max_x = round(max(max(vanishingPts)[0], width))
  new_min_y = round(min(min(vanishingPts, key=lambda x: x[1])[1], 0))
  new_max_y = round(max(max(vanishingPts, key=lambda x: x[1])[1], height))

  border = 50
  new_width = new_max_x - new_min_x + (border * 2)
  temp_height = new_max_y - new_min_y + (border * 2)

  ratio = new_width/width
  new_height = round(height * ratio)

  if new_height < temp_height:
    ratio = new_height/height
    new_width = round(width * ratio)
    new_height = temp_height

  new_image = np.zeros((new_height, new_width, 3), np.uint8)
  origin = (abs(new_min_x) + border, abs(new_min_y) + border)
  new_image[origin[1] : origin[1] + height, origin[0] : origin[0] + width, :] = img
        
  vanishingPt1 =  (round(vanishingPts[0][0] + origin[0]), round(vanishingPts[0][1] + origin[1]))
  vanishingPt2 =  (round(vanishingPts[1][0] + origin[0]), round(vanishingPts[1][1] + origin[1]))
  
  cv.line(img = new_image, pt1 = vanishingPt1, pt2 = vanishingPt2, color = drawColor, thickness = drawThickness)
  cv.circle(img = new_image, center = vanishingPt1, radius = 5, color = (0, 0, 255), thickness = -1)
  cv.circle(img = new_image, center = vanishingPt2, radius = 5, color = (0, 0, 255), thickness = -1)

  for index in range(4):
    cornerPts[index] = ((round(cornerPts[index][0] + origin[0]), round(cornerPts[index][1] + origin[1])))

  cv.line(img = new_image, pt1 = cornerPts[0], pt2 = vanishingPt1, color = drawColor, thickness = drawThickness)
  cv.line(img = new_image, pt1 = cornerPts[2], pt2 = vanishingPt1, color = drawColor, thickness = drawThickness)
  cv.line(img = new_image, pt1 = cornerPts[0], pt2 = vanishingPt2, color = drawColor, thickness = drawThickness)  
  cv.line(img = new_image, pt1 = cornerPts[1], pt2 = vanishingPt2, color = drawColor, thickness = drawThickness)

  currentImg = cv.resize(src = new_image, dsize = (0, 0), fx = 0.5, fy = 0.5)
  return currentImg

# calculate mug size for every image
for imageFilename in imageFilenames:
  currentImg = cv.resize(src = cv.imread(filename = imageFilename), dsize = (0, 0), fx = 0.5, fy = 0.5)
  currentImgPts = np.empty(shape = (12, 2), dtype = np.float32)
  currentImgPtsCount = 0

  def hndMouse(event, x, y, flags, userData):
    global currentImg, currentImgPts, currentImgPtsCount
    if event == cv.EVENT_LBUTTONDOWN and currentImgPtsCount < len(currentImgPts):
      # on click add new image point and visualize it
      currentImgPts[currentImgPtsCount] = np.array([x, y])
      currentImgPtsCount += 1
      cv.circle(img = currentImg, center = (x, y), radius = 5, color = (0, 0, 255), thickness = -1)

      if currentImgPtsCount == 4:
        # index 0-3 := table corners, index 4-5 := vanishing points
        currentImgPts[currentImgPtsCount] = calculateVanishingPoint(*currentImgPts[:4])
        currentImgPts[currentImgPtsCount + 1] = calculateVanishingPoint(*currentImgPts[[0, 2, 1, 3]])
        currentImgPtsCount += 2
        # draw lines towards vanishing points and vanishing line
        drawLine(currentImg, *currentImgPts[[0, 4]])
        drawLine(currentImg, *currentImgPts[[2, 4]])
        drawLine(currentImg, *currentImgPts[[0, 5]])
        drawLine(currentImg, *currentImgPts[[1, 5]])
        drawLine(currentImg, *currentImgPts[[4, 5]])

      if currentImgPtsCount == 8:
        # index 6 := bottle bottom, index 7 := bottle top
        drawMeasurementLine(currentImg, *currentImgPts[[6, 7]], value = givenSize)

      if currentImgPtsCount == 10:
        # index 8 := mug bottom, index 9 := mug top, index 10 := new vanishing point, index 11 := t
        currentImgPts[currentImgPtsCount] = calculateIntersection(*currentImgPts[[4, 5, 6, 8]])
        currentImgPts[currentImgPtsCount + 1] = calculateIntersection(*currentImgPts[[6, 7, 9, 10]])
        currentImgPtsCount += 2
        # index 11 := t, index 6 := b, index 7 := r
        imageCrossRatio = (
          np.linalg.norm(currentImgPts[11] - currentImgPts[6]) *
          np.linalg.norm(np.array([0, 1]) - currentImgPts[7])
        ) / (
          np.linalg.norm(currentImgPts[7] - currentImgPts[6]) *
          np.linalg.norm(np.array([0, 1]) - currentImgPts[11])
        )
        calculatedSize = givenSize * imageCrossRatio
        drawMeasurementLine(currentImg, *currentImgPts[[8, 9]], value = calculatedSize)
        calculatedSizes.append(calculatedSize)

        # resize image to display vanising points & vanishing line       
        currentImg = fitImage(currentImg, currentImgPts)

      cv.imshow(winname = "Image Point Selection", mat = currentImg)

  cv.imshow(winname = "Image Point Selection", mat = currentImg)
  cv.setMouseCallback(window_name = "Image Point Selection", on_mouse = hndMouse)

  while True:
    key = cv.waitKey(delay = 10)
    # quit program
    if key == ord("q"):
      exit()
    # next image
    if key == ord("n"):
      break

# print average of all calculated mug sizes
print(np.sum(calculatedSizes) / len(calculatedSizes))