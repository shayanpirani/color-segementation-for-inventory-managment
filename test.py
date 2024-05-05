import cv2
import numpy as np

# Load the image
image = cv2.imread('test1.jpg')

# Resize the image if needed
image = cv2.resize(image, (680, 480))

# Define the lower and upper ranges for each color in HSV format
color_ranges = {
    'cyan-blue': ([90, 102, 64], [109, 255, 255]),
    'dark-blue': ([0, 51, 0], [179, 255, 66]),
    # 'red': ([0, 100, 100], [10, 255, 255]),
    # 'yellow': ([20, 100, 100], [40, 255, 255]),
    'white': ([0, 0, 200], [179, 20, 255]),
    'pink': ([169, 77, 77], [169, 255, 255]),
}

# Convert image to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Initialize counts for each color
color_counts = {color: 0 for color in color_ranges}

# Process each color
for color, (lower_range, upper_range) in color_ranges.items():
    # Create a mask using the defined ranges
    mask = cv2.inRange(hsv, np.array(lower_range), np.array(upper_range))

    # Apply thresholding to the mask
    _, mask1 = cv2.threshold(mask, 254, 255, cv2.THRESH_BINARY)

    # Find contours in the thresholded image
    cnts, _ = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Process each contour
    for c in cnts:
        if cv2.contourArea(c) > 400:  # Adjust area threshold as needed
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 255), 2)
            cv2.putText(image, color.upper(), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            color_counts[color] += 1

# Display the processed image
cv2.imshow("Processed Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Display the quantities of each color on the screen
for color, count in color_counts.items():
    print(f"Quantity of {color.upper()}: {count}")
