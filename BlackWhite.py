# -*- coding: utf-8 -*-
import cv2
import numpy as np

#Declaring File, please change on your comp
file = "/Users/JuanDa/Documents/Spyder Workspace/EECS 395 Machine Learning/Testing Photos/Hand2.jpg"

def fillholes(gray):
    #Function to fill holes in a gray (or threshed) image
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    res = cv2.morphologyEx(gray,cv2.MORPH_OPEN,kernel)

#Read in image, set to gray and then threshold
InputImage = cv2.imread(file, cv2.IMREAD_COLOR)
gray_image = cv2.cvtColor(InputImage, cv2.COLOR_BGR2GRAY)
ret,fg = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY_INV)

#Elimanting noise
element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
fg= cv2.erode(fg,element)
fillholes(fg)


#Finding the contours
contours, hierarchy = cv2.findContours(fg,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


#Declaring variables to begin finding largest contour
max_area = 0
ci = 0
len_contours = len(contours)
if len_contours != 0:
    cnt = contours[0]
    #Now about to find the largest contour
    for i in xrange(len(contours)):
        cnt=contours[i]
        area = cv2.contourArea(cnt)
        if(area>max_area):
            max_area=area
            ci=i
        cnt=contours[ci]

    #Declaring hull & initializing the drawing image
    hull = cv2.convexHull(cnt)
    drawing = cv2.cvtColor(np.copy(thresh), cv2.COLOR_GRAY2BGR)

    #Drawing contours and hull (contour follows hand, hull is outside)
    cv2.drawContours(drawing,[cnt],0,(0,255,0),2)
    cv2.drawContours(drawing,[hull],0,(0,0,255),2)

    #Initializing moments
    moments = cv2.moments(cnt)
    if moments['m00']!=0:
        #Now finding the center of this hull
        cx = int(moments['m10']/moments['m00']) # cx = M10/M00
        cy = int(moments['m01']/moments['m00']) # cy = M01/M00              
        centr=(cx,cy) #Declaring Center
        cv2.circle(drawing,centr,5,[0,0,255],2) #Drawing the center of the hand in the image
        
        i=0 #Now to find the convex points and drawthem onto the image
        
        #NOT REALLY SURE WHAT IS GOING AFTER HERE. I DID NOT COMMENT WELL THE FIRST TIME
        #I KNOW IT FINDS THE TOP POINT AND ONLY DRAWS THAT POINT. WE NEED TO FIND ALL CONVEX POINTS
        hull = cv2.convexHull(cnt, returnPoints = False)
        if(hull.shape[0] > 3 and cnt.shape[0] > 3):
            defects = cv2.convexityDefects(cnt,hull)
            y_points = []
            if not defects is None:
                for i in range(defects.shape[0]):
                    s,e,f,d = defects[i,0]
                    far = tuple(cnt[f][0])
                    y_points.append([far[1], i])
                y_points.sort()
                indx = y_points[0][1]
                s, e, f , d = defects[indx, 0]
                print defects[indx,0]
                print cnt[f]
                far = tuple(cnt[f][0])
                cv2.circle(drawing,far,5,[255,0,0],-1)
                        
            cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
            hull = cv2.convexHull(cnt,returnPoints = False)
            
            #Show image
            cv2.imshow('drawing', drawing)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
