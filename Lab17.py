import cv2 as cv
 
# BG Substraction Algorithm
backSub = cv.createBackgroundSubtractorMOG2(history=None,varThreshold=None,detectShadows=True)
#backSub = cv.createBackgroundSubtractorKNN()
 
 
capture = cv.VideoCapture('CarDrive.mp4')
print(f"getHistory={backSub.getHistory()}")
print(f"getNMixtures={backSub.getNMixtures()}")
print(f"getDetectShadows={backSub.getDetectShadows()}")
print(f"varThreshold={backSub.getVarThreshold()}")
while True:
    ret, frame = capture.read()
    if frame is None:
        break
    
    fgMask = backSub.apply(frame,learningRate = 0.05)
    
    cv.rectangle(frame, (10, 2), (100,20), (255,255,255), -1)
    cv.putText(frame, str(capture.get(cv.CAP_PROP_POS_FRAMES)), (15, 15),
               cv.FONT_HERSHEY_SIMPLEX, 0.5 , (0,0,0))
    
    cv.imshow('Frame', frame)
    cv.imshow('FG Mask', fgMask)
    
    keyboard = cv.waitKey(30)
    if keyboard == 'q' or keyboard == 27:
        break