
# =============================================================================
# FOR THE USER TO TYPE IN
# =============================================================================

# String File name of image 
img_name = '73tif.tif'

# Detected edge within how many pixels of expected edge?
# Larger number is more forgiving to error
accuracy=5

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

# Number of nanomeers per pixel; found in SEM information text file 
PixelSize=11.018

# Number of BMP files you will have
# Note that BMP files should be named 1.bmp 2.bmp 3.bmp etc
num_bmp = 16

# BMP Pixel Size, in nanometers per pixel 
bmp_pixsize = 75

# do not display if match percent is below this filter value
percent_minimum = 0

# =============================================================================
# Read the original image
# =============================================================================
import cv2
import numpy as np 

img = cv2.imread(img_name)imgcopy = img.copy()
cv2.imshow('Original', img)

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

cv2.imshow('Binarize', binarize)

# =============================================================================
# uploading bmp 
# =============================================================================

perfects = []
min_width = width
min_height = height
for k in range(num_bmp):
    bmp = cv2.imread(str(1+k)+'.bmp')
    b_width = int(bmp_pixsize/PixelSize*bmp.shape[1])
    b_height = int(bmp_pixsize/PixelSize*bmp.shape[0])
    dsize = (b_width, b_height)
    bmp_big = cv2.resize(bmp, dsize)
    b_edge = cv2.Canny(bmp_big, 100, 100)
    expect = np.where(b_edge==255)
    y_avg = int(sum(expect[0])/len(expect[0]))
    x_avg = int(sum(expect[1])/len(expect[1]))
    for q in range(len(expect[0])):
        expect[0][q]-=y_avg
        expect[1][q]-=x_avg
    hei = max(expect[0])-min(expect[0]) 
    wid = max(expect[1])-min(expect[1])
    if hei < min_height: 
        min_height = hei
    if wid < min_width:
        min_width = wid
    perfects.append(expect)

# =============================================================================
# Recursive methods to complete a formation 
# =============================================================================

def formation(y,x,bound): 
    '''
    Parameters
    ----------
    y : TYPE            int
        DESCRIPTION.    y coordinate of an edge pixel
    x : TYPE            int
        DESCRIPTION.    x coordinate of an edge pixel 
    bound : TYPE        int
        DESCRIPTION.    expected distance between pixels 

    Returns
    -------
    list
        DESCRIPTION.    list containing all y, all x values of pixels in a formation

    '''
    y_list = []
    x_list = []
    edges[y,x]=150
    y_list.append(y)
    x_list.append(x)
    for j in range(max(0, y-bound), min(height, y+bound)):
        for i in range(max(0,x-bound), min(width, x+bound)):
            if (edges[j,i]==255):
                form = formation(j,i,bound)
                y_list.extend(form[0])
                x_list.extend(form[1])
    return [y_list, x_list]

# =============================================================================
# finding center x and y 
# =============================================================================
def findCenter(form):
    '''
    Parameters
    ----------
    form : TYPE         list of 2 lists 
        DESCRIPTION.    list of x, y coordinates of a form 

    Returns
    -------
        DESCRIPTION.    tuple of 2 ints, y and x values of center of formation

    '''
    top = min(form[0])
    bot = max(form[0])
    left = min(form[1])
    right = max(form[1])
    area=0
    xsum=0
    ysum=0
    for j in range(top, bot):
        for i in range(left, right):
            if binarize[j][i][0] != 0:
                xsum+=i
                ysum+=j
                area+=1
    if area==0:
        return (-1, -1)
    
    return (int(ysum/area), int(xsum/area))

# =============================================================================
# matching
# =============================================================================

def matching(form, perf, bound, y_avg, x_avg):
    """

    Parameters
    ----------
    form : TYPE         List of 2 lists
        DESCRIPTION.    list of y, list of x coordinates of form 
    perf : TYPE         list of 2 lists
        DESCRIPTION.    list of y, list of x coordinates of ideal form 
    bound : TYPE        int
        DESCRIPTION.    within how many pixels of ideal would count?
    y_avg : TYPE        int
        DESCRIPTION.    y coordinate of center 
    x_avg : TYPE        int
        DESCRIPTION.    x coordinate of center

    Returns
    -------
    TYPE                int
        DESCRIPTION.    percent of edge pixels that are close to ideal

    """
    # xthresh and ythresh are a fifth of the width or length of ideal figure
    # if an edge deviates by more than this amount then the shape is surely incorrect
    xthresh = 0.2*(max(perf[1])-min(perf[1]))
    ythresh = 0.2*(max(perf[0])-min(perf[0]))
    
    # placing all of the formation x, y values into a grid 
    arr = np.zeros((height, width), dtype=np.int64)
    for q in range(len(form[0])):
        arr[form[0][q]][form[1][q]] = 1
        if form[0][q]==0 or form[0][q]==height-1 or form[1][q]==0 or form[1][q]==width-1:
            return -1
    
    # going through each pixel to determine if the formation match ideal figure
    counts = 0
    prevx=-1
    prevy=-1
    for q in range(len(perf[0])):
        y_p = perf[0][q]
        x_p = perf[1][q]
        y_p+=y_avg
        if y_p<0 or y_p>=height:
            return -1
        x_p+=x_avg
        if x_p<0 or x_p>=width:
            return -1
        if prevx>0 and prevy>0:
            if abs(x_p-prevx)>xthresh or abs(y_p - prevy)>ythresh: 
                return -1
        add=0
        for j in range(max(0, y_p-bound), min(y_p+bound, height)):
            for i in range(max(0, x_p-bound), min(x_p+bound, width)):
                # if edges[j][i]!=0: 
                #     add=1
                if arr[j][i]==1:
                    add=1
        counts+=add
    return int(100*counts/len(perf[0]))

# =============================================================================
# drawing the best match 
# =============================================================================

def overlayBMP(form, perf, val, bound, y_avg, x_avg):
    if val < percent_minimum:
        return 
    arr = np.zeros((height, width), dtype=np.int64)
    for q in range(len(form[0])):
        arr[form[0][q]][form[1][q]] = 1
    for q in range(len(perf[0])):
        y_p = perf[0][q]
        x_p = perf[1][q]
        y_p+=y_avg
        x_p+=x_avg
        if y_p>0 and y_p<height and x_p>0 and x_p<width:
            color=(0,0,0)
            for j in range(max(0, y_p-bound), min(y_p+bound, height)):
                for i in range(max(0, x_p-bound), min(x_p+bound, width)):
                    if arr[j][i]==1:
                        color = (0,0,255)
            imgcopy[y_p][x_p]=color
    cv2.putText(imgcopy, str(val), (x_avg, y_avg), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255),2)
    
# =============================================================================
# working code
# =============================================================================
for j in range(height):
    for i in range(width):
        if (edges[j][i]==255):
            my_form = formation(j, i, 5)
            if max(my_form[0])-min(my_form[0])>min_height*0.5 and max(my_form[1])-min(my_form[1])>min_width*0.5:
                max_match = 0
                best_bmp = -1
                # find the center of the formation; we will overlay ideal figure on top 
                y_avg = int(sum(my_form[0])/len(my_form[0]))
                x_avg = int(sum(my_form[1])/len(my_form[1]))
                center = findCenter(my_form)
                for k in range(len(perfects)):
                    mat = matching(my_form, perfects[k], accuracy, center[0], center[1])
                    if mat>max_match: 
                        max_match = mat
                        best_bmp = k
                print(str(max_match)+'%', best_bmp+1)
                if best_bmp>-1:
                    overlayBMP(my_form, perfects[best_bmp], max_match, accuracy, center[0], center[1])
cv2.imshow('Results', imgcopy)
