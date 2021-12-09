# File name of image 
img_name = '73tif.tif'

# Threshold for Canny edge detection; higher number = greater threshold
# Note that when the edge_blur value is high, use lower threshold 
# greater threshold means fewer edges detected but also removes noise
# This number is usually an integer between 10 and 200
threshold= 30

# blur for canny edge detection; Higher number = more blur
# when the SEM image visually looks noisy/blurry, use a higher number
# when the SEM image looks sharp, use a lower number
# This number should be an odd integer 
edge_blur = 13

# blur for binarizing the image; higher number = more blur 
# Keeping the bw_blur value low is fine. This number should be an odd integer
bw_blur = 1

# =============================================================================
# Read the original image
# =============================================================================
import cv2
img = cv2.imread(img_name)
imgcopy = img.copy()

# =============================================================================
# Cropping the image + edge detection + binarized (b/w) image
# =============================================================================
# Getting the height and width of the image 
height = img.shape[0]
width = img.shape[1]

# getting past the black strip at the bottom 
y = height-1 
x = width-1
while img[y,x,0]==0: 
    y-=1
y+=1
height=y

# Cropping the image to remove the bottom stripe 
img_crop = img[0:height]

# Blur the image for better edge detection
img_blur = cv2.GaussianBlur(img_crop, (edge_blur, edge_blur), 100)
img_blur2 = cv2.GaussianBlur(img_crop, (bw_blur, bw_blur), 100)

# Canny Edge Detection
edges = cv2.Canny(img_blur, threshold, threshold) 

# Display Canny Edge Detection Image
cv2.imshow('Canny Edge Detection', edges)

th, binarize = cv2.threshold(img_blur2, 100, 255, cv2.THRESH_TOZERO)

cv2.imshow('Binarized Image', binarize)
