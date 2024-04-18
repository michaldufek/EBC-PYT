import cv2
import numpy as np

IMG_PATH = "data/scene.jpg"

def blur_image(image_path):
    image = cv2.imread(image_path)
    blurred_image = cv2.GaussianBlur(image, (21, 21), 0)  # Kernel size and sigma
    cv2.imshow('Blurred Image', blurred_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def sharpen_image(image_path):
    image = cv2.imread(image_path)
    # Sharpening kernel
    kernel = np.array([[-1, -1, -1], 
                       [-1, 9, -1],
                       [-1, -1, -1]])  
    sharpened_image = cv2.filter2D(image, -1, kernel)
    cv2.imshow('Sharpened Image', sharpened_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def edge_detection(image_path):
    image = cv2.imread(image_path)
    edges = cv2.Canny(image, 100, 200)  # Lower and upper thresholds
    cv2.imshow('Edge Detection', edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    #blur_image(IMG_PATH)
    #sharpen_image(IMG_PATH)
    edge_detection(IMG_PATH)

