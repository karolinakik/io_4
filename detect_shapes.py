from shape_detection.shapedetector import ShapeDetector

import sys
import argparse
import imutils
import cv2

# construct the argument parse and parse the arguments
# argument_parser = argparse.ArgumentParser()
# argument_parser.add_argument("--i", "--image", required=True, help="path to the input image")
# args = vars(argument_parser.parse_args())

argument_parser = argparse.ArgumentParser()
argument_parser.add_argument("-i", "--image", required=True, help="path to the input image")
args = vars(argument_parser.parse_args())

print(args)

# load the image and resize it to a smaller fator so that
# the shapes can be approximater better
image = cv2.imread(args["image"])
resized = imutils.resize(image, width=300)
ratio = image.shape[0] / float(resized.shape[0])

# convert the resized image to grayscale, blur it slightly, and threshold it
gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
threshold = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)[1]

# find contours in the thresholded image and initialize the shape detecctor
contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)
shape_detector = ShapeDetector()

global shape_size_comparator

shape_size_comparator = 0

# loop over the contours
for contour in contours:
    # compute the center of the contour, then detect the name of the
    # shape using only the contour
    M = cv2.moments(contour)
    cX = int((M["m10"] / M["m00"]) * ratio)
    cY = int((M["m01"] / M["m00"]) * ratio)
    shape_name = shape_detector.detect(contour)[0]
    shape_size = shape_detector.detect(contour)[1].real

    if shape_name == "square":
        if shape_size > shape_size_comparator:
            shape_size_comparator = shape_size
            shape_name = shape_name + "!"

    # multiply the contour (x, y)-coordinates by the resize ratio,
    # then draw the contours and the name of the shape on the image
    contour = contour.astype("float")
    contour *= ratio
    contour = contour.astype("int")
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
    cv2.putText(image, shape_name, (cX + 10, cY), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2)

    ############################################
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    # cv2.putText(image, "center", (cX - 20, cY - 20),
    #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    ############################################

    # print(shape)
    # print(contour)

    # show the output image
    cv2.imshow("Image", image)
    cv2.waitKey(0)