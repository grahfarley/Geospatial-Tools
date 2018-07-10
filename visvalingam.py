import numpy
import pandas
import os

os.chdir('C:\Users\graham.farley\Documents\Documents\Python')
#Simplify Morphology



data = pandas.read_excel('testXS.xlsx',headers=None)
A = data.values #Matrix of points, each point is represented by a vector

N = len(A) #Number of points in the original matrix
q = 7 #Number of points you wish to simplify to






def TriAreaCalc(pt1,pt2,pt3):
    #Change reference frame such that pt1 becomes the origin
    AB = pt2 - pt1 
    AC = pt3 - pt1

    #The cross-product of two 2D vectors gives the area of the parallelogram
    #formed by those two vectors, therefore the area of a triangle created
    #by two vectors is:
    Area = (0.5)*numpy.linalg.norm((numpy.cross(AB,AC)))
    return Area




""" What  we want to do is look at sets of three points, calculate the area
of the triangle formed by those three points, then """




n = N
while (n > q):
    i = 1
    B1 =numpy.inf
    while (i<=n-2):
        p1 = A[(i-1),:]
        p2 = A[(i),:]
        p3 = A[(i+1),:]
        B2 = TriAreaCalc(p1,p2,p3)

        if B2 < B1:
            B1 = B2
            del_pt = i
            print("New Delete pt:")
            print del_pt
        
        i +=1
    A = numpy.delete(A,del_pt,0)
    print("Point {} deleted").format(del_pt)
    n -= 1

print(A)






    
