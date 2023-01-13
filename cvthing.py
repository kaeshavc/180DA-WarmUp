from cgitb import reset
import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
while(1):
    # Take each frame
    _, frame = cap.read()
    fgbg = cv.bgsegm.createBackgroundSubtractorMOG()


    # Convert BGR to HSV
    ###hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of red color in HSV
    # upper boundary RED color range values; Hue (160 - 180)
    ###lower_red = np.array([160,100,20])
    ###upper_red = np.array([179,255,255])
    # Threshold the HSV image to get only red colors
    ###mask = cv.inRange(hsv, lower_red, upper_red)
    # Bitwise-AND mask and original image
    ###res = cv.bitwise_and(frame,frame, mask= mask)
    
    grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    #fgmask = fgbg.apply(grayscale)


    #contours,hierarchy = cv.findContours(grayscale,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_SIMPLE)
    ret,thresh = cv.threshold(grayscale,127,255,0)
    contours,hierarchy = cv.findContours(thresh, 1, 2)

    cnt = contours[0]
    x,y,w,h = cv.boundingRect(cnt)
    cv.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    #ret,thresh = cv.threshold(grayscale,127,255,0)
    #contours,hierarchy = cv.findContours(thresh, 1, 2)
    #cnt = contours[0]
    #x,y,w,h = cv.boundingRect(cnt)


    #cv.imshow('frame',frame)
    #cv.imshow('grayscale', grayscale)
    ###cv.imshow('mask',mask)
    #cv.rectangle(grayscale,(x,y),(x+w,y+h),(0,255,0),2)
    #cv.imshow('frame',fgmask)
    cv.imshow("original",frame)

    ###cv.imshow('res',res)
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

    

cv.destroyAllWindows()