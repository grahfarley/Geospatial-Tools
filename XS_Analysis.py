#Analyzes the .csv cross-sections from the stack profile of transects
""" An important feature of this script is that the csv file contains the profiles
 of all transects in that huc. This means that each individual transect has to be extracted
 before it can be analyzed."""
import pandas as pd
import os
import numpy as np
import arcpy
import matplotlib.pyplot as plt #Plotting just to validate results



os.chdir("C:\Users\graham.farley\Downloads\Data\Mountain_Profiles_CSV")
files = os.listdir(os.getcwd())


arcpy.env.workspace=r"C:\Users\graham.farley\Downloads\Data\MountainTransects.gdb"
files = files[14:]


"""The following are the functions used in the main script..."""


"""
This function takes the left half of the cross-section, with the
curvature being at [:,1], and finds the first negative curvature from
the thalweg. It counts backwards through the points along the cross section
"""
def find_left(L):       
    while end>=0:
        d2 = L[end,1]
        if d2<0:
            Left_TOB = int(L[end,0])
            return Left_TOB
        else:
            end -= 1

"""
This function steps through the right half of the cross-section and finds
the first negative values of curvature.
"""


def find_right(R):
    for point in R:
        if point[1]<0:
            Right_TOB = int(point[0])
            return Right_TOB



"""
This function takes an array that represents the cross-section, and the
transect OID for that cross-section. It returns the elevation of
the top of bank and the thalweg.
"""

def find_ToB(Cross_Section,trans_id):
    
    N = Cross_Section.shape[0] #length (number of points) of the cross-section
    i = 0
    L = None
    R = None
    break_pt = None             #Index of the midpoint
    diff = np.zeros((N-1,1))    #create an empty array for first derivative
    diff2 = np.zeros((N-2,2))   #empty array for second derivative
    Thalweg = np.min(Cross_Section[:,1]) #elevation of thalweg

    
    Mid_point = np.max(Cross_Section[N-1,0])/2 #Distance in meters to the midpoint
    
    """
    find the index of the midpoint,
    so as to split the cross-section into left and right.
    """

    while i<=(N-1):      
        x = Cross_Section[i,0]
        if x<Mid_point:
            i += 1
        else:
            break_pt = i
            break
    
    
    break_pt = int(break_pt-Cross_Section[0,0]) #Adjust the break pt using the OID of the first point in the cross-section
    
    L = Cross_Section[0:break_pt,:]
    R = Cross_Section[break_pt:,:]

    L_max = np.max(L[:,1])
    R_max = np.max(R[:,1])

    """
    Insert the lower of the highest point on each bank as the
    top of bank.
    """
    
    if L_max<R_max:         
        Top_of_Bank = L_max
    else:
        Top_of_Bank = R_max


    """
    Use the finite difference to calculate second derivative. This was put in
    with the expectation that more methods for finding the top of bank.
    """
    
    method = "finite_diff"
    if method  == "finite_diff":
        j = 0
        while j<=(N-2): #calculate first derivative
            del_x = Cross_Section[j+1,0]-Cross_Section[j,0]
            del_y = Cross_Section[j+1,1]-Cross_Section[j,1]
            dydx = del_y/del_x
            diff[j] = dydx
            j+=1
        j = 0
        while j<=(N-3): #calculate second derivative
            del_x = Cross_Section[j+1,0]-Cross_Section[j,0]
            del_dy = diff[j+1]-diff[j]
            d2yd2x = del_dy/del_x
            diff2[j,0] = j+1
            diff2[j,1] = d2yd2x
            j+=1



        Ld = diff2[:(break_pt-1),:]
        Rd = diff2[break_pt-1:,:]

        Right_index = find_right(Rd)
        Left_index = find_left(Ld)



        #The index will be None if the cross-section is flat on that side
        if (Right_index == None and Left_index == None):
            if L_max<R_max:
                Top_of_Bank = L_max
            else:
                Top_of_Bank = R_max
            return Top_of_Bank, Thalweg
        


        Right_Top = Cross_Section[Right_index,1]
        Left_Top  = Cross_Section[Left_index,1]

        if Right_index == None:
            Top_of_Bank = Left_Top
            return Top_of_Bank, Thalweg
        if Left_index == None:
            Top_of_Bank = Right_Top
            return Top_of_Bank, Thalweg
        


        
    
        
        if Right_Top<Left_Top:
            Top_of_Bank = Right_Top
        else:
            Top_of_Bank = Left_Top
     
    return Top_of_Bank, Thalweg



    
    
        
        

"""
This part of the code reads from the csv file, and determines where each cross-section
begins and ends. It then runs that cross-section through the above functions to find
the top of bank, and appends that top of bank to the associated transect.
"""


for datafile in files:
    
    trans_file = datafile[:-12]+"Transect"
    trans_file = os.path.join(arcpy.env.workspace,trans_file)
    
    data = pd.read_csv(datafile,header=0)
    A = data.values

    i = 1
    j = 0
    n = A.shape[0]
    XS = np.array(A[0,:])              
                
    TOB = []
    Thals = []
        
    arcpy.AddField_management(trans_file,"Top_of_Bank","Float")
    while (i<n):
        ID = A[j,4]     #The OID of the transect
        try:
            next_ID = A[j+1,4]
        except:
            print("No more")
            next_ID = None


        if next_ID == i:    #If the OID of the next point has the same OID, append it to the cross-section
            XS = np.vstack((XS,A[j+1,:]))
            j += 1
        else:   #append points until you reach the next transect, then find ToB
            Top,Thal = find_ToB(XS,i)
            TOB.append(Top)
            Thals.append(Thal)
            i += 1
            j += 1
            
            try:
                XS =np.array(A[j,:])
            except:
                break
        
    
    j = 0
    
    with arcpy.da.UpdateCursor(trans_file,["OBJECTID","Top_of_Bank"]) as cursor:
        for row in cursor:
            row[1] = 3.28*(TOB[j]-Thals[j]) #Change ToB to the elevation above the thalweg
            cursor.updateRow(row)
            j+=1



    
        
            
        
        
                        
    
        
        
