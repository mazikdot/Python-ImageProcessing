import cv2
import numpy as np

# def dilate(img, struct_element, origin):
# 	h, w = img.shape
# 	result = img[:,:]
# 	add_y = struct_element.shape[0] - origin[0]
# 	add_x = struct_element.shape[1] - origin[1]
# 	for i in range (h):
# 		for j in range (w):
# 			if bool(img[i][j]) and bool(struct_element[origin[0]][origin[1]]):
# 				x1 = j-origin[1]
# 				x2 = j+add_x
# 				y1 = i-origin[0]
# 				y2 = i+add_y
# 				# structure modification
# 				s_x1 = 0
# 				s_x2 = struct_element.shape[1]
# 				s_y1 = 0
# 				s_y2 = struct_element.shape[0]

# 				if x1 < 0:
# 					s_x1 = s_x1 + (0 - x1)
# 					x1 = 0
# 				if x2 > w:
# 					s_x2 = s_x2 - (x2 - (w-1))
# 					x2 = w-1
# 				if y1 < 0:
# 					s_y1 = s_y1 + (0 - y1)
# 					y1 = 0
# 				if y2 > h-1:
# 					s_y2 = s_y2 - (y2 - (h-1))
# 					y2 = h-1

# 				window = img[y1:y2, x1:x2] | struct_element[s_y1:s_y2, s_x1:s_x2]
# 				result[y1:y2, x1:x2] = window
# 	return result


# def erode(img, struct_element, origin):
# 	h, w = img.shape
# 	result = img[:,:]
# 	add_y = struct_element.shape[0] - origin[0] -1
# 	add_x = struct_element.shape[1] - origin[1] -1

# 	for i in range (h):
# 		for j in range (w):
# 			if bool(img[i][j]) and bool(struct_element[origin[0]][origin[1]]):
# 				x1 = j-origin[1]
# 				x2 = j+add_x
# 				y1 = i-origin[0]
# 				y2 = i+add_y
# 				# structure modification
# 				s_x1 = 0
# 				s_x2 = struct_element.shape[1]
# 				s_y1 = 0
# 				s_y2 = struct_element.shape[0]

# 				if x1 < 0 or x2 > w-1 or y1 < 0 or y2 > h-1:
# 					result[i][j] = 0
# 				else:
# 					window = img[y1:y2, x1:x2]
# 					zero_flag = False
# 					for x in range(window.shape[0]):
# 						for y in range(window.shape[1]):
# 							if img[i][j] is 0:
# 								zero_flag = True
# 					if zero_flag:
# 						result[i][j] = 0		
# 	return result


# To Dilate:
img2 =  np.array([
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,1,1,0,0,1,1,1,1,0,0,0,0,0],
		[0,1,1,1,0,0,1,1,1,0,0,0,1,1,0],
		[0,1,1,1,1,1,1,1,1,0,0,0,1,1,0],
		[0,0,1,0,0,1,1,1,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,1,0,0,0,1,1,0,0,0],
		[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	],dtype=np.uint16)
print("Image:")
print(img2)
struct_element = np.array([
		[0,1,0],
		[1,1,1],
		[0,1,0],
	],dtype=np.uint8)
print("Structure Element:")
print(struct_element)
origin = (1,0)	# (y,x) or origin
print("After Dilation:")
print(cv2.dilate(img2, struct_element, origin))

# To Erode:
img =  np.array([
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,1,1,0,0,1,1,1,1,0,0,0,0,0],
		[0,1,1,1,0,0,1,1,1,0,0,0,1,1,0],
		[0,1,1,1,1,1,1,1,1,0,0,0,1,1,0],
		[0,0,1,0,0,1,1,1,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,1,0,0,0,1,1,0,0,0],
		[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
		[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
	],dtype=np.uint16)
struct_element = np.array([
		[0,1,0],
		[1,1,1],
		[0,1,0],
	],dtype=np.uint8)
print("Image:")
print(img)
print("Structure Element:")
print(struct_element)
print("After Erosion:")
print(cv2.erode(img, struct_element, origin))