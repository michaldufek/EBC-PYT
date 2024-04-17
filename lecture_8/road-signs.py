import cv2
import numpy as np

# Load an image
image = cv2.imread('data/road.jpg')

# Define the range of colors for road signs (e.g., red)
lower_red = np.array([0, 50, 50])
upper_red = np.array([10, 255, 255])

# Convert to HSV and create a mask
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, lower_red, upper_red)

# Find contours
contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.02*cv2.arcLength(cnt, True), True)
    cv2.drawContours(image, [approx], 0, (0, 255, 0), 5)

# Show the image
cv2.imshow('Road Sign detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
