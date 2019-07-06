
# coding: utf-8

# In[1]:


import cv2
import numpy as np

cap = cv2.VideoCapture(0)

def nothing(x):
    pass

cv2.namedWindow('trackbars')
cv2.namedWindow('frame')

cv2.createTrackbar('l-H','trackbars',0,179,nothing)
cv2.createTrackbar('l-S','trackbars',84,255,nothing)
cv2.createTrackbar('l-V','trackbars',178,255,nothing)
cv2.createTrackbar('u-H','trackbars',16,179,nothing)
cv2.createTrackbar('u-S','trackbars',224,255,nothing)
cv2.createTrackbar('u-V','trackbars',255,255,nothing)

bg = np.zeros((480, 640, 3),dtype=np.uint8)

while True:
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    
    l_h = cv2.getTrackbarPos('l-H','trackbars')
    l_s = cv2.getTrackbarPos('l-S','trackbars')
    l_v = cv2.getTrackbarPos('l-V','trackbars')
    
    lower_blue = np.array([l_h,l_s,l_v])
    
    u_h = cv2.getTrackbarPos('u-H','trackbars')
    u_s = cv2.getTrackbarPos('u-S','trackbars')
    u_v = cv2.getTrackbarPos('u-V','trackbars')
    
    upper_blue = np.array([u_h,u_s,u_v])
    obj = cv2.inRange(hsv,lower_blue,upper_blue)
    
    
    
    _,mask = cv2.threshold(obj,50,255,cv2.THRESH_BINARY)   
    new_fr_fg = cv2.bitwise_and(frame,frame,mask=cv2.bitwise_not(mask))
    new_fr_bg = cv2.bitwise_and(bg,bg,mask=mask)
    
    invisible = cv2.add(new_fr_fg,new_fr_bg)
    
    cv2.imshow('frame',frame)
    cv2.imshow('hsv',hsv)
    cv2.imshow('mask',obj)
    cv2.imshow('foreground',new_fr_fg)
    cv2.imshow('background',new_fr_bg)
    cv2.imshow('detected bg',bg)
    cv2.imshow('magic window',invisible)
    
    key = cv2.waitKey(1)
    
    if key==ord('c'):
        bg = frame
    elif key==27:
        break

cap.release()
cv2.destroyAllWindows()

