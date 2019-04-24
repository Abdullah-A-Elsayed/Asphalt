import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = cv2.imread('tst - Copy.jpg')
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,img = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
cv2.imshow('image',img)

tst= pytesseract.image_to_string(img,lang='ara')


if(pytesseract.image_to_string(img)):
    print(pytesseract.image_to_string(img,lang='ara'))
else:
    print ("error")

file = open("copy.txt", mode="w" ) 
file.write(tst.encode('utf-8')) 
file.close() 


cv2.waitKey(0)

cv2.DestoryAllwindows()
