import cv2 as cv

for n in range(1,6,1):
    img = cv.imread('D:\\koparka\\fisher\\digits\\'+str(n)+'.jpg')
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    thresh = cv.threshold(img, 120, 255, cv.THRESH_BINARY)[1]
    cv.imwrite('D:\\koparka\\fisher\\digits\\'+str(n)+'.png', thresh);
