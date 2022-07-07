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
same_center_x = np.where(indicies[1] == greatest_area_center_point[0])

#find points along same center axis of centerpoint
center_x_axis = indicies[0][same_center_x]

midpoint_length = np.size(same_center_x)

num_splits = 3

def draw_vertical_lines(center_axis, mask_border, midpoint_length, num_splits, direction):
  top_edge_mask = center_x_axis[0]
  bottom_edge_mask = center_x_axis[-1]
  for i in range(0, mask_border, midpoint_length_x//num_splits):
      x_axis =  greatest_area_center_point[0] + (i * direction)
      strt = (x_axis, top_edge_mask)
      end = (x_axis, bottom_edge_mask)      
      cv2.line(img, strt, end, (0, 255, 0), 3)   
left_verticle_lines = draw_vertical_lines(center_x_axis, border_x, midpoint_length_x, num_splits, -1)
right_verticle_lines = draw_vertical_lines(center_x_axis, border_x, midpoint_length_x, num_splits, 1)



same_center_y = np.where(indicies[0] == greatest_area_center_point[1])
center_y_axis = indicies[1][same_center_y]
midpoint_length_y = np.size(same_center_y)
border_y = center_y_axis[-1]

def draw_horizontal_lines(center_axis, mask_border, midpoint_length, num_splits, direction):
    left_border = 368
    right_border = 960
    for i in range(0,mask_border,):
        y_axis =  greatest_area_center_point[1] + (i * direction)
        strt = (left_border,y_axis)
        end = (right_border,y_axis)      
        cv2.line(img, strt, end, (0, 255, 0), 3)  
        
horizontal_lines_up = draw_horizontal_lines(center_y_axis, border_y, midpoint_length_y, num_splits, -1)
