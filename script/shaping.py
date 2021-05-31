import numpy as np
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--image", required=True,
	help="/images/inputs")
args = vars(ap.parse_args())

image = cv2.imread(args["image"],255)
original = image.copy()
img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([22, 93, 0], dtype="uint8")
upper = np.array([45, 255, 255], dtype="uint8")
mask = cv2.inRange(img, lower, upper)

kernel = np.ones((5,5),np.uint8)
dilation = cv2.dilate(mask,kernel,iterations = 2)
blur=cv2.medianBlur(dilation,9)


cnts = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
print(len(cnts))

cnts = cnts[0] if len(cnts) == 2 else cnts[1]
   
for cnt in cnts:
    epsilon = 0.04*cv2.arcLength(cnt, True)
    approx = cv2.approxPolyDP(cnt, epsilon, True)
 
    if len(approx) == 3:
        print("shape: triangle,", "c1:{x}, c2:{y}".format(x=x, y=y))

    elif len(approx) == 4:
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
        print("shape: rectangle,", "length:{w}, breadth:{h}".format(w=w, h=h))
        
    
    elif len(approx)>5:
        ellipse = cv2.fitEllipse(cnt)
        (x,y),(d1,d2),radius = ellipse
        x, y, d1, d2 = int(x), int(y), int(d1), int(d2)
        aprox_radius = int(abs(d1-d2))
        cv2.ellipse(image ,ellipse ,(0,255,0),2)
        if(aprox_radius<3):
            print("shape: circle,", "center:({x},{y}),radius:{r}".format(x=x,y=y,r=d1))
        
        else:      
            print("shape: ellipse,", "majorAxis:{d1}, minorAxis:{d2} center:({x},{y})".format(d1=d1,d2=d2, x=x, y=y))
    
            
    else:
        print("!!shapes not detected in an image!!")

cv2.imshow('output', image)
cv2.waitKey(0)


