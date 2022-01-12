# Metasurface SEM characterization - arbitrary geometry layout
Measures the accuracy of fabricating a metaatom by comparing the SEM image with the original design

## Sample output
The numbers represent the percentage of pixel edges that match up with the BMP file 
<img src="https://github.com/yitianzhu/Metasurface_SEM_v4/blob/main/images/results1.PNG" width=50% height=50%> 

## How to use
### Download and setup
1) Download [Threshold_finder.py](https://github.com/yitianzhu/Metasurface_SEM_v4/blob/main/Threshold_finder.py) and [Metasurface-IMG-Processing.py](https://github.com/yitianzhu/Metasurface_SEM_v4/blob/main/Metasurface-IMG-Processing.py) in the same folder. 
2) Copy all your BMP files into the same folder. They should be named "1.bmp", "2.bmp", etc. 
3) Copy all your SEM images into the same folder. 

### Preparing thresholds
4) Open Threshold_finder.py 
5) Fill in the following information:
```
# File name of image, string for text file name 
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
```
6) Run the program. Change the values for threshold, edge_blur, and bw_blur according to the resulting images' appearance. They should be clear, with minimal noise. See the example images below.
<img src="https://github.com/yitianzhu/Metasurface_SEM_v4/blob/main/images/Example-Binarized.PNG" width=50% height=50%>
<img src="https://github.com/yitianzhu/Metasurface_SEM_v4/blob/main/images/Example-Canny.PNG" width=50% height=50%> 

### Running the program 
7) Open Metasurface-IMG-Processing.py
8) Fill in the following information. You already determined the first four values, i.e. img_name, threshold, edge_blur, bw_blur. 
```
# String File name of image 
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

# Detected edge within how many pixels of expected edge?
# Larger number is more forgiving to error
# This is an integer
accuracy=5

# Number of nanomeers per pixel; found in SEM information text file 
# This can be a floating point number
PixelSize=11.018

# Number of BMP files you will have
# Note that BMP files should be named 1.bmp 2.bmp 3.bmp etc
# Integer 
num_bmp = 16

# BMP Pixel Size, in nanometers per pixel 
# Can be floating point number or integer
bmp_pixsize = 75

# do not display results for a metaatom if its match percent is below this filter value
percent_minimum = 0
```
9) The computer will generate multiple images: Original SEM, Binarized image, Canny Edge Detection, Results. See a sample of the Results image below: 
<img src="https://github.com/yitianzhu/Metasurface_SEM_v4/blob/main/images/Example-Results.PNG" width=50% height=50%>

