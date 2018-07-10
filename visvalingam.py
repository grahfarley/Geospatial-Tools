import numpy
import pandas
import os

"""This script takes an input of an excel file containing cross-section data (x,z), and simplifies that cross-section
to the desired number of points (q) using visvalingam's algorithm"""


os.chdir('C:\Users\graham.farley\Documents\Documents\Python')


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
of the triangle formed by those three points, then remove the point corresponding to the 
triangle of the smallest area, until we are left with q points"""




n = N
while (n > q):   #loop until q points remain
    i = 1
    B1 =numpy.inf  #set the initial smallest area as infinite, so any calculated area will be smaller
    while (i<=n-2):  #Do not delete the endpoints, so calculate areas from the second point, to the second to last point
        p1 = A[(i-1),:]
        p2 = A[(i),:]
        p3 = A[(i+1),:]
        B2 = TriAreaCalc(p1,p2,p3)

        if B2 < B1:   #If the calculated area is smaller than the previous smallest, make this the new point to be deleted. 
            B1 = B2
            del_pt = i
            print("New Delete pt:")
            print del_pt
        
        i +=1
    A = numpy.delete(A,del_pt,0)
    print("Point {} deleted").format(del_pt)
    n -= 1

print(A)






    
