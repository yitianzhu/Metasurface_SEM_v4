# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 12:27:19 2021

@author: frfty
"""

import cv2

# Threshold for Canny edge detection; higher number = greater threshold
threshold=30
# blur for canny edge detection; Higher number = more blur
edge_blur = 13
# blur for binarizing the image; higher number = more blur 
bw_blur = 1
# File name of image 
img_name = '70tif.tif'

# =============================================================================
# Read the original image
# =============================================================================
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

cv2.imshow('binarize', binarize)
