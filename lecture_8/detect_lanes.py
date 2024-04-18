import cv2
import numpy as np

def detect_lanes(image_path):
    # Read the image
    image = cv2.imread(image_path)
    # Resize for consistency
    image = cv2.resize(image, (960, 540))
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply Gaussian blur
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    # Edge detection
    edges = cv2.Canny(blur, 50, 150)

    # Create a masked edges image using cv2.fillPoly()
    mask = np.zeros_like(edges)
    polygon = np.array([[
        (200, 540),
        (760, 540),
        (560, 300),
        (400, 300)
    ]], np.int32)
    cv2.fillPoly(mask, polygon, 255)
    masked_edges = cv2.bitwise_and(edges, mask)

    # Hough Transform to detect lines
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi/180, 50, minLineLength=50, maxLineGap=150)
    
    # Create a copy of the original image to draw lines
    line_image = np.copy(image) * 0  # Creating a blank to draw lines on

    # Draw lines on the image
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 10)

    # Create a color binary image to combine with line image
    color_edges = np.dstack((edges, edges, edges))
    
    # Draw the lines on the original image
    combo = cv2.addWeighted(image, 0.8, line_image, 1, 0)

    # Display the image
    cv2.imshow('Lane Detection', combo)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Example usage
detect_lanes('data/lanes.jpg')
