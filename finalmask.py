import cv2 
import numpy as np
from matplotlib import pyplot as plt

#Loading image
img = cv2.imread('mask.png')


# Change colored image into grayscale
grey_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 

#apply otsu threshold method
_, threshold = cv2.threshold(grey_img, 0, 1, cv2.THRESH_OTSU)


contours,heirarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#find coordinates for edges of image
indicies = np.where(threshold != [0])

#indices [0] = y-coordinates
#indices [1] = x-coordinates
coordinates = list(zip(indicies[1],indicies[0]))


#empty lists
center_points = []
areas = []
 
#loop for the contours
for i in contours:
    #find the center point for each contoured region
    M = cv2.moments(i)
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
   #cv2.drawContours(img, [i], -1, (0, 255, 0), 2)
    
    # add center points to a list
    center_points.append((cx,cy))
    
    #find the area for each contoured region
    a = M['m00']
    
    #add areas to a list
    areas.append(a)
    
    
#function to find max area from areas list   
def max_area(nums):
    current_max = nums[0]
    for num in nums:
        if num > current_max:
            current_max = num
    return current_max
test = areas
max_area(test)
print('Greatest Area:',max_area(test))


#position on list where greatest area can be found 
index = areas.index(max_area(test))
print('Index of greatest area:',index)



#draws circle at center of largest area found 
cv2.circle(img, center_points[index], 5, (0, 255, 0), -1)
print('Center Point',center_points[index])

#finds x-coordinates that are within the mask that are equal x center point 
ind_y_needed_1 = np.where(indicies[1]==center_points[index][0])

#new points bound within mask with same with center y coorindate different x 
y_1 = indicies[0][ind_y_needed_1]
# left_border = right_border = 0


#draw verticle line from to the left from the center coordinate
for i in range(0, y_1[-1],((np.size(ind_y_needed_1))//2)): 
    ind_y_needed_1 = np.where(indicies[1]==center_points[index][0]-i)
    y_1 = indicies[0][ind_y_needed_1]
    strt = (center_points[index][0]-i, y_1[0])
    end = (center_points[index][0]-i,y_1[-1])
    print(center_points[index][0]-i)

    # left_border = center_points[index][0]-i
    # top_left = strt
    # bottom_left = end
    cv2.line(img, strt, end, (0, 255, 0), 3)




#finds x-coordinates that are within the mask that are equal x center point 
ind_y_needed_2 = np.where(indicies[1]==center_points[index][0])

#new points bound within mask with same center y coorindate different x 
y_2 = indicies[0][ind_y_needed_2]

#draw verticle line from to the right from the center coordinate
for i in range(0,y_2[-1],((np.size(ind_y_needed_2))//2)): 
    ind_y_needed_2 = np.where(indicies[1]==center_points[index][0]+i)
    y_2 = indicies[0][ind_y_needed_2]
    strt = (center_points[index][0]+i, y_2[0])
    end = (center_points[index][0]+i,y_2[-1])
    
    right_border = center_points[index][0]+i
    
    cv2.line(img, strt, end, (0, 255, 0), 3)


# #IDEA ON HOW TO DRAW HORIZONTAL LINES BUT COULD BE BETTER
# #finds y-coordinates that are within the mask that are equal y center point 
# ind_x_needed_1 = np.where(indicies[0]==center_points[index][1])

# #new points bound within mask with same with center y coorindate different x 
# x_1 = indicies[1][ind_x_needed_1]

# #draw horizontal line from the left of the center coordinate
# print(left_border, right_border)
# for i in range(0,x_1[-1],100):  
#     strt = (left_border,center_points[index][0]-i)
#     end = (right_border,center_points[index][0]-i)
#     cv2.line(img, strt, end, (0, 255, 0), 3)
 

plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title('Center of mask')
plt.show




print('Number of contours detected:', len(contours))