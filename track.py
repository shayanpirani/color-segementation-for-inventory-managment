import cv2
import numpy as np

# Load the image
image = cv2.imread('colortracking\\test1.jpg')

# Resize the image if needed
image = cv2.resize(image, (640, 480))

# Create trackbars and window
cv2.namedWindow("Trackbars")
cv2.createTrackbar("L - H", "Trackbars", 0, 179, lambda x: None)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, lambda x: None)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, lambda x: None)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, lambda x: None)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, lambda x: None)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, lambda x: None)

# Initial mask and result images
mask = np.zeros(image.shape[:2], dtype=np.uint8)
result = np.zeros_like(image)

while True:
    # Get trackbar positions
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Define lower and upper ranges
    lower_blue = np.array([l_h, l_s, l_v])
    upper_blue = np.array([u_h, u_s, u_v])

    # Convert image to HSV and create mask
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply mask to original image
    result = cv2.bitwise_and(image, image, mask=mask)

    # Show thresholded image
    cv2.imshow("mask", mask)
    cv2.imshow("result", result)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

cv2.destroyAllWindows()
