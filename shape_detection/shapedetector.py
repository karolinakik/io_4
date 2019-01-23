import sys
# sys.path.append('C:\\Users\\Iza\\PycharmProjects\\opecv-test\\venv\\Lib\\site-packages')
import cv2
import cmath


class ShapeDetector:
    def __init__(self):
        pass

    def detect(self, contour):
        # initialize the shape name and approximate the contour
        shape_name = "unidentified"
        perimeter_of_the_contur = cv2.arcLength(contour, True)
        contour_approximation = cv2.approxPolyDP(contour, 0.04 * perimeter_of_the_contur, True)

        # if the shape is a triangle, it will have 3 vertices
        if len(contour_approximation) == 3:
            shape_name = "triangle"

        # if the shape has 4 vertices, it is either a square or a rectangle
        elif len(contour_approximation) == 4:
            # compute the bounding box of the countour and use the bounding box to compute aspect ratio
            (x, y, w, h) = cv2.boundingRect(contour_approximation)
            aspect_ratio = w / float(h)

            # a square will have an aspect ratio that is approximately equal to one, otherwise, the shape i rectangle
            if aspect_ratio >= 0.95 and aspect_ratio <= 1.05:
                shape_name = "square"
            else:
                shape_name = "rectangle"

        # if the shape is a pentagon, it will have 5 vertices
        elif len(contour_approximation) == 5:
            shape_name = "pentagon"

        # otherwise, we assume the shape is a circle
        else:
            shape_name = "circle"

        print("Shape: " + shape_name)
        print("Type of coordinates collection: ")
        print(type(contour_approximation))
        print(contour_approximation.tolist())
        list = contour_approximation.tolist()
        print("Amount of vertex coordinates: ")
        print(len(list))
        print("Coordinates X,Y of one vertex: ")
        print(list[1][0][0])
        print(list[1][0][1])
        print("List of vertex coordinates: ")
        print(contour_approximation)

        coordinates = []

        for i in range(len(list)):
            print(i)
            x = list[i][0][0]
            y = list[i][0][1]
            print('X = ' + str(x))
            print('Y = ' + str(y))

            coordinates.append([x, y])

        print(coordinates)

        shape_size = 0

        print("shape_size before calculation = " + str(shape_size))

        if shape_name == "square":
            print('x2 = ' + str(coordinates[1][0]))
            print('x1 = ' + str(coordinates[0][0]))
            print('y2 = ' + str(coordinates[1][1]))
            print('y1 = ' + str(coordinates[0][1]))
            print('x difference = ' + str(abs(coordinates[1][0] - coordinates[0][0])))
            print('y difference = ' + str(abs(coordinates[1][1] - coordinates[0][1])))
            print('potegowanie x = ' + str(abs(coordinates[1][0] - coordinates[0][0])**2))
            print('potegowanie y = ' + str(abs(coordinates[1][1] - coordinates[0][1])**2))
            shape_size = cmath.sqrt(((abs(coordinates[1][0] - coordinates[0][0]))**2) + ((abs(coordinates[1][1] - coordinates[0][1]))**2))

        print("shape_size after calculation = " + str(shape_size))

        # return the name of the shape
        return shape_name, shape_size

