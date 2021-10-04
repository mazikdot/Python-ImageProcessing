import cv2
import numpy as np
# To Dilate:
img2 =  np.array([
		[0,0,0,0,0,0],
		[1,0,0,1,1,0],
		[0,0,0,0,0,0],
		[1,0,0,0,0,1]
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
print(cv2.dilate(img2, struct_element))

# To Erode:
img =  np.array([
		[1,0,1,1,1,0],
		[1,1,1,1,1,1],
		[1,1,1,1,1,1],
		[0,1,0,1,0,1]
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
print(cv2.erode(img, struct_element))