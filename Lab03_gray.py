# Brightness/Contrast Adjustment -> https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html
# Trackbar -> https://www.life2coding.com/change-brightness-and-contrast-of-images-using-opencv-python/
# Python -> https://www.tutorialspoint.com/python/python_command_line_arguments.htm
# * ลักษณะการประมวลผลหรือการทำงานจะคล้าย ๆ กับ color แต่แตกต่างกันตรงที่ gray เป็นการทำภาพขาวเทาขึ้นมาประมวลผลแทนภาพสี
# * เมื่อ bata มากค่าความสว่างของภาพก็จะมากแต่ถ้า alpha เป็น 0 ภาพก็จะมืด alpha มากขึ้นภาพก็จะเพิ่มความสว่างมากขึ้น
# * histogram เมื่อปรับค่า alpha เพิ่มขึ้น histogram ก็จะขยับไปด้านขวา
# * เช่น เมื่อ beta = 33 แล้วทำการปรับค่า alpha ให้เพิ่มขึ้น histogram ก็จะขยับจากซ้ายไปขวา เนื่องจาก ค่า alpha ที่เพิ่มขึ้น
import cv2 as cv #import cv2 โดยใช้ชื่อย่อในการเขียนว่า cv
import numpy as np #import numpy โดยใช้ชื่อย่อในการเขียนว่า np numpy เป็น library เกี่ยวกับการคำนวณ
import sys #import Sys เข้ามาใช้งาน
from matplotlib import pyplot as plt #import library matplotlib ในส่วนย่อย pyplot โดยย่อว่า plt
# Global Variable
beta_brightness_value = 100  #ประกาศตัวแปรเบต้า เอาไว้ปรับค่า Brightness จะมี tag bar เลื่อน ให้เราเลื่อนไปเลื่อนมา และเนื่องจาก tag bar ที่เลื่อน ๆ 
#มันไม่มีด้านลบค่าจริงเท่ากับ 0
alpha_contrast_value = 10 #เอาไว้ปรับค่าแอลฟ้าหรือคอนทราสจะถูกหารด้วย 10 
source_img = np.zeros((10,10,3), dtype=np.uint8) #สร้าง array 2 มิติ มี 3 แผ่น เป็นตัวแปร zeros ทุก ๆ ค่าจะมีค่าเป็น 0 ใช้ไลบรารี่ numpy มีขนาด 10 * 10 
# แถว มี 3 แผ่น dtype คือ data type 10 Column 0 Row 3 แผ่น ตามลำดับ ใช้เก็บภาพที่นำเข้ามา
adjusted_img = np.zeros((10,10,3), dtype=np.uint8)#เก็บภาพผลลัพธ์ที่ทำการปรับ 
hist_img = np.zeros((10,10,3), dtype=np.uint8)  #เก็บภาพ Histogram 

def handler_adjustAlphaBata(x):
    global beta_brightness_value,alpha_contrast_value #ประกาศตัวแปร หรือดึงตัวแปร ที่อยู๋นอกฟังก์ชั่นมาใช้งาน
    global source_img,adjusted_img,hist_img #ประกาศตัวแปร หรือดึงตัวแปร ที่อยู๋นอกฟังก์ชั่นมาใช้งาน
    beta_brightness_value = cv.getTrackbarPos('beta','BrightnessContrast') #เอาแท็กบา beta ไบต์เนสครอนทาส แล้วเอาไปเก็บในตัวแปร เบต้าไบต์เนส value
    alpha_contrast_value = cv.getTrackbarPos('alpha','BrightnessContrast')  #เอาแท็กบา alpha ไบต์เนสครอนทาส แล้วเอาไปเก็บในตัวแปร alpha คอนทาส value
    alpha = alpha_contrast_value / 10 #ประกาศตัวแปร alpha ให้มีค่าเท่ากับ  alpha_contrast_value / 10 
    beta = int(beta_brightness_value - 100)  #มีการลบด้วย 100 เพราะต้องการให้มีด้านที่ติดลบ
    print(f"alpha={alpha} / beta={beta}") #แสดงผลลัพธ์ค่า beta และ alpha เมื่อมีการปรับเปลี่ยนค่า alpha beta
    
    ## loop access each pixel -> too slow
    ''' for y in range(source_img.shape[0]):
        for x in range(source_img.shape[1]):
            adjusted_img[y,x] = np.clip( alpha * source_img[y,x] + beta , 0, 255)
    '''
    # for better performance, pls use -> dst = cv.convertScaleAbs(src1, alpha, beta)
    #เอาภาพมาคูณกับตัวแปร alpha beta adjust_img คือปรับเรียบร้อยแล้ว เอาไปให้ main ทำหน้าที่โชว์
    adjusted_img = cv.convertScaleAbs(source_img, alpha=alpha, beta=beta)

    # Update histogram
    #histogram 3 แท่ง แยกภาพเป็น 3 แผ่นให้มันเป็น BGR 
    bgr_planes = cv.split(adjusted_img) #เอาไว้แยกสีของภาพออกเป็นลิสต์ของค่าแต่ละสี
    histSize = 256 #กำหนดให้ histSize = 256
    histRange = (0, 256) # the upper boundary is exclusive
    accumulate = False #ประกาศ accumulate ให้เป็น False คือค่าเริ่มต้น
     #คำนวณ histogram ในช่องที่ 0 
    gray_hist = cv.calcHist(adjusted_img, [0], None, [histSize], histRange, accumulate=accumulate) #คำนวณ Histogram สีส้ม
    hist_w = 512 #กำหนดความกว้าง histogram
    hist_h = 400 #กำหนดความสูง histogram
    bin_w = int(round( hist_w/histSize )) #round เป็นคำสั่งสำหรับใช้ปัดตัวเลขในระบบจำนวนจริง จะมีการนำเอา hist_w ความกว้างของ histogram หารด้วย histSize
    hist_img = np.zeros((hist_h, hist_w, 3), dtype=np.uint8) #ทำการสร้าง array และเก็บเอาไว้ในตัวแปร hist_img
    cv.normalize(gray_hist, gray_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX) #นอมอลไลฟ์    0 -> 1 เป็นแบบ gray
    for i in range(1, histSize):            #ใช้ Forlooop เพื่อประมวลผลขนาดของภาพ gray 
        cv.line(hist_img, ( bin_w*(i-1), hist_h - int(gray_hist[i-1]) ),
                ( bin_w*(i), hist_h - int(gray_hist[i]) ),
                ( 0, 144, 255), thickness=2)
                                                    #histogram 1 channel จาก 3 channel 

def main():
    global beta_brightness_value,alpha_contrast_value #ตัวแปร global คือตัวแปรที่อยู่นอกฟังก์ชั่นจะต้องประกาศ
    global source_img,adjusted_img,hist_img #ตัวแปร global คือตัวแปรที่อยู่นอกฟังก์ชั่นจะต้องประกาศ

    if(len(sys.argv)>=2):  #มีการนับ sys.argv ว่า ถ้าหากมีค่า มากกว่าหรือเท่ากับ 2 ก็จะให้อ่านค่าภาพที่ส่งผ่าน argument 
        source_img = cv.imread(str(sys.argv[1]))
    else : #ถ้าไม่ใช่ก็จะให้เอาภาพที่มีการ set ตำแหน่งในไฟล์เอาไว้
        source_img = cv.imread("./test.jpg", 1)

    source_img = cv.cvtColor(source_img,cv.COLOR_BGR2GRAY) # convert to GrayScale #เปิดใช้ GrayScale แปลง จาก BGR เป็น GRAY  #อธิบายการทำงาน
    #อธิบายภาพแล้วก็ส่งไม่ต้องยาวมาก
    #named windows 
    #ถ้าเราระบุ cv.WINDOW_NORMAL ก็คือมันจะให้เราปรับได้เล็กใหญ่ ถ้าเราเป็นโหมด Default มันจะปรับไม่ได้ ขนาดเท่าไหนเท่านั้น
    #มีการระบุ 3 ตัวคือ Original BrightnessContrast และ Histogram
    cv.namedWindow("Original", cv.WINDOW_NORMAL) 
    cv.namedWindow("BrightnessContrast", cv.WINDOW_NORMAL)
    cv.namedWindow("Histogram", cv.WINDOW_NORMAL)

    #create trackbar
    #create trackbar แท็กบานี้จะไปเกาะในตัว ไบต์เนสก่อนทาส ก็จะมี 2 ตัวเลื่อนคือ อัลฟ่า กับเบต้า
    cv.createTrackbar('beta', 'BrightnessContrast', beta_brightness_value, 200, handler_adjustAlphaBata)
    cv.createTrackbar('alpha', 'BrightnessContrast', alpha_contrast_value, 50, handler_adjustAlphaBata)
                    # ชื่อแท็กบา     ไปเกาะที่ไหน            ค่าปัจจุบันที่จะส่งไป   ค่าสูงสุด ฟังก์ชั่นสำหรับจัดการเมื่อแท็กบาร์มีการเปลี่ยนแปลงฟังก์ชั่นนี้จะอยู่ข้างบน
    adjusted_img  = source_img.copy()
    #copy ข้อมูลทั้งมี ที่มีใน Source image ก็คือก็อปภาพต้นฉบับไปอยู่ใน Adjust Image เมื่อเปลี่ยนแปลง adjust image ก็จะเปลี่ยนแปลงไป source image
    while(True):
        cv.imshow("Original",source_img)                    #คำสั่งที่จะโชว์ตัวแปร Source_img ที่เก็บภาพไปโชว์ในหน้าต่าง Original 
        cv.imshow("BrightnessContrast",adjusted_img)        #โชว์ภาพ adjusted_img ในหน้าต่าง BrightnessContrast
        cv.imshow("Histogram",hist_img)                     #โชว์ภาพ hist_img ในหน้าต่าง Histogram
        key = cv.waitKey(100) #ต้องมีคำสั่งนี้เสมอถ้าเราใช้ imshow   #รอการกดคีย์ 100 ms ถ้าไม่มีการกดคีย์มาก็จะไปทำคำสั่งถัดไป
        if(key==27): #ESC = Exit Program  key = 27 คือ รหัสแอสกี้ ของ ESC 
            break

    cv.destroyAllWindows() #ทำลาย Window ที่สร้างขึ้นมาที่ name window ได้สร้างมา

if __name__ == "__main__":
    main()