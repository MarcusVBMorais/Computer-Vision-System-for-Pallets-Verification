#A Computer Vision System for Pallets Verification in Quality Control#

#This project has been developed based on image processing and machine learning techniques. 
#Image processing parameters of Canny and Hough Transform have been adjusted.
#Support-Vector Machines (SVM) parameters' have been optmized using the grid function.

#Authors
#Marcus Vinicius Barbosa de Morais
#Sara Dereste dos Santos
#Ricardo Pires
#
#Federal Institute of Education, Science Technology of Sao Paulo
#Electrical Department

#Import libraries
import numpy as np
import math
import cv2
import time
from svmutil import *

#Variables#
x = []
y = []
a = []
a1 = 0
a2 = 0
a3 = 0
c = []
c1 = 0
c2 = 0
c3 = 0
pal = 0

#Parameters#
MLL = 300 #Hough minLineLength
MLG = 155 #Hough maxLineGap
L = 255   #Hough Threshold
i = 90    #Canny lower threshold
s = 100   #Canny upper threshold

print "Beginning training data processing"
arq = open("Training", "w")
print "Processing data  from good pallets"

while (pal < 105):
    #Clear variables
    x = []
    y = []
    a = []
    a1 = 0
    a2 = 0
    a3 = 0
    c = []
    c1 = 0
    c2 = 0
    c3 = 0
    #Import pallet image
    pal = pal + 1
    fig = 'Palete (' + str( pal ) + ').jpg'
    img = cv2.imread(fig)
    gray = cv2.imread(fig,0)
    #Call Canny
    edges = cv2.Canny(gray,i,s)
    #Call Hough
    lines = cv2.HoughLinesP(edges,1,np.pi/180,L,minLineLength=MLL,maxLineGap=MLG)

    for t in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[t]:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            x.append(x2-x1)
            y.append(float(-(y2-y1)))
            if x[t] == 0:
                a.append(90.0)
            else:
                a.append(math.degrees(math.atan(y[t]/x[t])))
            c.append(np.sqrt((x[t]**2)+(y[t]**2)))

        #Classify Angles
        if a[t] <= -30:
            a1 = a1 + 1
        elif a[t] > -30 and a[t] <= 30:
            a2 = a2 + 1
        elif a[t] > 30:
            a3 = a3 + 1
        else:
            print "Angle value out of range"
            print a[t]

        #Classify Lenght
        if c[t] <= 800:
            c1 = c1 + 1
        elif c[t] > 800 and c[t] <= 1600:
            c2 = c2 + 1
        elif c[t] > 1600:
            c3 = c3 + 1
        else:
            print "Lenght value out of range"
            print c[t]
    
    #Generate label
    if pal <= 60:
        classe = '+1'
    else:
        classe = '-1'
    #Generate histogram
    h = classe + ' 1:' + str( a1 ) + ' 2:' + str( a2 ) + ' 3:' + str( a3 ) + ' 4:' + str( c1 ) +  ' 5:' + str( c2 ) + ' 6:' + str( c3 )

    #Print pallet number
    print pal
    #Print histogram
    print h
    #Write histogram to file
    arq.write(h)
    arq.write("\n")
    #Check if all 45 good pallets were processed
    if pal == 45:
        pal = 60
        print "Processing data from bad pallets"
    else:
        pal = pal
arq.close()
print "Training data processing finished"

pal = 45

print "Beginning test data processing"
arq = open("Test", "w")
print "Processing data  from good pallets"

while (pal < 120):
    #Clear variables
    x = []
    y = []
    a = []
    a1 = 0
    a2 = 0
    a3 = 0
    c = []
    c1 = 0
    c2 = 0
    c3 = 0
    #Import pallet image
    pal = pal + 1
    fig = 'Palete (' + str( pal ) + ').jpg'
    img = cv2.imread(fig)
    gray = cv2.imread(fig,0)
    #Call Canny
    edges = cv2.Canny(gray,i,s)
    #Call Hough
    lines = cv2.HoughLinesP(edges,1,np.pi/180,L,minLineLength=MLL,maxLineGap=MLG)

    for t in range(0, len(lines)):
        for x1,y1,x2,y2 in lines[t]:
            cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
            x.append(x2-x1)
            y.append(float(-(y2-y1)))
            if x[t] == 0:
                a.append(90.0)
            else:
                a.append(math.degrees(math.atan(y[t]/x[t])))
            c.append(np.sqrt((x[t]**2)+(y[t]**2)))

        #Classify Angles
        if a[t] <= -30:
            a1 = a1 + 1
        elif a[t] > -30 and a[t] <= 30:
            a2 = a2 + 1
        elif a[t] > 30:
            a3 = a3 + 1
        else:
            print "Angle value out of range"
            print a[t]

        #Classify Lenght
        if c[t] <= 800:
            c1 = c1 + 1
        elif c[t] > 800 and c[t] <= 1600:
            c2 = c2 + 1
        elif c[t] > 1600:
            c3 = c3 + 1
        else:
            print "Lenght value out of range"
            print c[t]
    
    #Generate label
    if pal <= 60:
        classe = '+1'
    else:
        classe = '-1'
    #Generate histogram
    h = classe + ' 1:' + str( a1 ) + ' 2:' + str( a2 ) + ' 3:' + str( a3 ) + ' 4:' + str( c1 ) +  ' 5:' + str( c2 ) + ' 6:' + str( c3 )

    #Print pallet number
    print pal
    #Print histogram
    print h
    #Write histogram to file
    arq.write(h)
    arq.write("\n")
    #Check if all 15 good pallets were processed
    if pal == 60:
        pal = 105
        print "Processing data from bad pallets"
    else:
        pal = pal
arq.close()
print "Test data processing finished"

#SVM
print "Defining Support Vector Machine"
y, x = svm_read_problem('Training')
prob = svm_problem(y, x)
param = svm_parameter('-g 0.0078125 -c 2')

print "Training Support Vector Machine"
m = svm_train(prob, param)
p_label, p_acc, p_val = svm_predict(y, x, m)

print "Testing Support Vector Machine"
y, x = svm_read_problem('Test')
p_label, p_acc, p_val = svm_predict(y, x, m)

print "Good Bye"

cv2.waitKey(0)
cv2.destroyAllWindows()

