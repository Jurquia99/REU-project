import cv2 
import numpy as np
from matplotlib import pyplot as plt

#Loading image
img = cv2.imread('mask.png')

# Change colored image into grayscale
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

#apply otsu threshold method
_, threshold = cv2.threshold(grey_img, 0, 1, cv2.THRESH_OTSU)

#find the contour of the thresholded image
contours,heirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#indices [0] = y-coordinates
#indices [1] = x-coordinates_
indicies = np.where(threshold != [0])

center_points = []
areas = []
 
#loop for the contours
for contour in contours:
    #find the center point for each contoured region and add them to a list
    M = cv2.moments(contour)
    center_x = int(M['m10']/M['m00'])
    center_y = int(M['m01']/M['m00'])
    center_points.append((center_x, center_y))

    area = M['m00']
    areas.append(area)

#function to find max area from areas list   
def max_area(nums):
    current_max = nums[0]
    for num in nums:
        if num > current_max:
            current_max = num
    return current_max

#using greatest area index find centerpoint coordinate of greatest area
greatest_area_index = areas.index(max_area(areas))
greatest_area_center_point = center_points[greatest_area_index]


#find points on edge of mask with same x center coordinate
same_center_x = np.where(indicies[1]==greatest_area_center_point[0])

#find points along same center axis of centerpoint
center_x_axis = indicies[0][same_center_x]

midpoint_length = np.size(same_center_x)

num_splits = 3
