# Brightness/Contrast Adjustment -> https://docs.opencv.org/3.4/d3/dc1/tutorial_basic_linear_transform.html
# Trackbar -> https://www.life2coding.com/change-brightness-and-contrast-of-images-using-opencv-python/
# Python -> https://www.tutorialspoint.com/python/python_command_line_arguments.htm
# ! โจทย์ ทดลองปรับค่า alpha / beta แล้วอธิบายผลลัพธ์ พร้อมภาพประกอบ เช่น ปรับ alpha = 0.8 ภาพมี 
# ! contrast น้อยลง เนื่องจาก .... ซึ่งสังเกตุได้จาก ... มาการบีบหดลง เนื่องจากการคูณของค่า 
# !  alpha กับทุก Pixel ของทั้งภาพ
# * อธิบาย 
# * เมื่อ beta มีค่ามากขึ้นกราฟของ Histogram จะมีการขยับไปทางขวา เนื่องจาก beta ที่เพิ่มขึ้นแต่ alpha นั้นยังเท่าเดิม
# * ผลลัพธ์ของภาพเมื่อทำการปรับค่า beta เพิ่มชึ้นภาพก็จะขาวขึ้น 
# * และเมื่อ alpha น้อย ๆ จะทำให้กรากฟ histogram มีการขยับไปทางซ้าย ถ้า alpha มากขึ้นภาพก็จะสว่างขึ้น
# * alpha น้อยภาพก็จะมืดลง
#* ตัวอย่างเช่น ถ้าค่า beta = 42 แต่ alpha = 0 ก็จะเท่ากับว่าภาพมืดต้องทำการปรับค่า alpha ขึ้นมาเพื่อให้มองเห็นภาพ
#* แต่ในทางกลับกัน ถ้าเมื่อไหร่ที่ beta = -100 แต่ยังมีค่า alpha อยู่ตั้งแต่ 0.1 ขึ้นไป พบว่าภาพก็ยังจะมองเห็นได้
#* สรุปสั้น ๆ  alpha = 0  beta เท่าไหร่ภาพก็จะมืด 
#* beta = -100 แต่ alpha มากกว่า 0.1 ภาพก็จะมองเห็น 
import cv2 as cv #import library opencv โดยย่อ 
import numpy as np #import library numpy โดยใช้ชื่อย่อ เป็น np 
import sys #import library sys เข้ามาใช้งาน ใช้ในการรับ Argument ภายนอก from Command Line  (Recive image Path)
from matplotlib import pyplot as plt #import library matplotlib ในส่วนย่อย pyplot โดยย่อว่า plt
# Global Variable
beta_brightness_value = 100 #ประกาศตัวแปรเบต้าเอาไว้ปรับค่า Brightness จะมี tag barเลื่อนให้เราเลื่อนไปเลื่อนมาและเนื่องจาก tag bar ที่เลื่อน ๆ มันไม่มีด้านลบค่าจริงเท่ากับ 0
alpha_contrast_value = 10 #เอาไว้ปรับค่าแอลฟ้าหรือคอนทราสจะถูกหารด้วย 10 
source_img = np.zeros((10,10,3), dtype=np.uint8) #สร้าง array 2 มิติ มี 3 แผ่น เป็นตัวแปร zeros ทุก ๆ ค่าจะมีค่าเป็น 0 ใช้ไลบรารี่ numpy มีขนาด 10 * 10 แถว มี 3 แผ่น
#dtype คือ data type 10 Column 0 Row 3 แผ่น ตามลำดับ ใช้เก็บภาพที่นำเข้ามา
adjusted_img = np.zeros((10,10,3), dtype=np.uint8) #เก็บภาพผลลัพธ์ที่ทำการปรับ 
hist_img = np.zeros((10,10,3), dtype=np.uint8) #เก็บภาพ Histogram 

def handler_adjustAlphaBeta(x):
    global beta_brightness_value,alpha_contrast_value #ประกาศตัวแปร หรือดึงตัวแปร ที่อยู๋นอกฟังก์ชั่นมาใช้งาน
    global source_img,adjusted_img,hist_img #ประกาศตัวแปร หรือดึงตัวแปร ที่อยู๋นอกฟังก์ชั่นมาใช้งาน
    beta_brightness_value = cv.getTrackbarPos('beta','BrightnessContrast') #เอาแท็กบา beta ไบต์เนสครอนทาส แล้วเอาไปเก็บในตัวแปร เบต้าไบต์เนส value
    alpha_contrast_value = cv.getTrackbarPos('alpha','BrightnessContrast') #เอาแท็กบา alpha ไบต์เนสครอนทาส แล้วเอาไปเก็บในตัวแปร alpha คอนทาส value
    alpha = alpha_contrast_value / 10 #ประกาศตัวแปร alpha เพื่อเก็บค่า  alpha_contrast_value / 10 
    beta = int(beta_brightness_value - 100) #ที่ทำแบบนี้เพราะต้องการให้มีด้านที่ติดลบ
    print(f"alpha={alpha} / beta={beta}")
    
    ## loop access each pixel -> too slow     #ตรงนี้จะเข้าถึงทั้ง x และ y ต้องบอก c ด้วย เข้าไปในทีละ pixel เลย clip กำหนดช่วงไม่ให้เกิน 255
    ''' for y in range(source_img.shape[0]):    
        for x in range(source_img.shape[1]):
            for c in range(source_img.shape[2]):
                adjusted_img[y,x,c] = np.clip( alpha * source_img[y,x,c] + beta , 0, 255)
    '''
    # for better performance, pls use -> dst = cv.addWeighted(src1, alpha, src2, beta, 0.0)
    #เอาภาพมาคูณกับตัวแปร alpha beta adjust_img คือปรับเรียบร้อยแล้ว เอาไปให้ main ทำหน้าที่โชว์
    adjusted_img = cv.convertScaleAbs(source_img, alpha=alpha, beta=beta)

    # Update histogram 
    #จะเห็นได้ว่ามี histogram 3 แท่ง แยกภาพเป็น 3 แผ่นให้มันเป็น BGR 
    bgr_planes = cv.split(adjusted_img) #เอาไว้แยกสีของภาพออกเป็นลิสต์ของค่าแต่ละสี
    histSize = 256  #กำหนดให้ histSize = 256
    histRange = (0, 256) # the upper boundary is exclusive
    accumulate = False #ประกาศ accumulate ให้เป็น False คือค่าเริ่มต้น
    #คำนวณ histogram ในช่องที่ 0 ที่แผ่นสีน้ำเงิน 1 เขียว 2 แดง 
    b_hist = cv.calcHist(bgr_planes, [0], None, [histSize], histRange, accumulate=accumulate) #คำนวณ histogram สีน้ำเงิน
    g_hist = cv.calcHist(bgr_planes, [1], None, [histSize], histRange, accumulate=accumulate) #คำนวณ histogram สีเขียว
    r_hist = cv.calcHist(bgr_planes, [2], None, [histSize], histRange, accumulate=accumulate) #คำนวณ histogram สีแดง
    hist_w = 512  #กำหนดความกว้าง histogram
    hist_h = 400  #กำหนดความสูง histogram
    bin_w = int(round( hist_w/histSize )) #round เป็นคำสั่งสำหรับใช้ปัดตัวเลขในระบบจำนวนจริง จะมีการนำเอา hist_w ความกว้างของ histogram หารด้วย histSize
    hist_img = np.zeros((hist_h, hist_w, 3), dtype=np.uint8)
    cv.normalize(b_hist, b_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX) #นอมอลไลฟ์    0 -> 1
    cv.normalize(g_hist, g_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX) #นอมอลไลฟ์    0 -> 1
    cv.normalize(r_hist, r_hist, alpha=0, beta=hist_h, norm_type=cv.NORM_MINMAX) #นอมอลไลฟ์    0 -> 1
    for i in range(1, histSize): #มีการใช้ for loop เป็นวนหาขนาดของ histogram
        cv.line(hist_img, ( bin_w*(i-1), hist_h - int(b_hist[i-1]) ),
                ( bin_w*(i), hist_h - int(b_hist[i]) ),
                ( 255, 0, 0), thickness=2)
        cv.line(hist_img, ( bin_w*(i-1), hist_h - int(g_hist[i-1]) ),
                ( bin_w*(i), hist_h - int(g_hist[i]) ),
                ( 0, 255, 0), thickness=2)
        cv.line(hist_img, ( bin_w*(i-1), hist_h - int(r_hist[i-1]) ),
                ( bin_w*(i), hist_h - int(r_hist[i]) ),
                ( 0, 0, 255), thickness=2)


def main():
    global beta_brightness_value,alpha_contrast_value #ตัวแปร global คือตัวแปรที่อยู่นอกฟังก์ชั่นจะต้องประกาศ
    global source_img,adjusted_img,hist_img

    if(len(sys.argv)>=2):                                #ถ้านับ argument มามากกว่า หรือเท่ากับ 2 ก็จะให้ มันอ่านภาพ และเก็บไว้ใน sys.argv[1]
        source_img = cv.imread(str(sys.argv[1]))
    else :
        source_img = cv.imread("./test.jpg", 1) #ก็คือถ้าใส่ argument ก็จะอ่านจาก argument แต่ถ้าไม่ใส่ก็จะอ่านจากไฟล์ภาพที่เรากำหนดไว้

    #source_img = cv.cvtColor(source_img,cv.COLOR_BGR2GRAY) # convert to GrayScale

    #named windows สร้าง window ขึ้นมา แท็กบา ที่เลื่อนไปมา ก็จะมาเกาะ
    cv.namedWindow("Original", cv.WINDOW_NORMAL) #ถ้าเราระบุ cv.WINDOW_NORMAL ก็คือมันจะให้เราปรับได้เล็กใหญ่ ถ้าเราเป็นโหมด Default มันจะปรับไม่ได้ ขนาดเท่าไหนเท่านั้น
    cv.namedWindow("BrightnessContrast", cv.WINDOW_NORMAL)
    cv.namedWindow("Histogram", cv.WINDOW_NORMAL)

    #create trackbar แท็กบานี้จะไปเกาะในตัว ไบต์เนสก่อนทาส ก็จะมี 2 ตัวเลื่อนคือ อัลฟ่า กับเบต้า
    cv.createTrackbar('beta', 'BrightnessContrast', beta_brightness_value, 200, handler_adjustAlphaBeta)
    cv.createTrackbar('alpha', 'BrightnessContrast', alpha_contrast_value, 50, handler_adjustAlphaBeta)
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