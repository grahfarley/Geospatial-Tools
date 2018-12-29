import arcpy
import os
arcpy.env.overwriteOutput = True

#Database Utility
"""This tool acts as a shortcut for several common ArcPy tools, especially those
used in the post-processing of the streams/wetlands"""


class wrkspace(object):
    def __init__(self, path):
        self.w_space = path
        arcpy.env.workspace = path
        self.ListOfFeatures = arcpy.ListFeatureClasses() #This is the most valuable part of the script. It allows access to all the feature classes in a geodatabase, which has been especially useful since the streams were split into such small units.
    def dlt_fields(self,feature,fields):
        arcpy.DeleteField_management(feature,fields)
    def add_fields(self,feature, fields):
        for field in fields:
            arcpy.AddField_management(feature,field,"FLOAT")

    def intersect(self,feature,split_feature,out_feature):
        arcpy.Intersect_analysis([feature,split_feature],out_feature,"NO_FID")

    def dissolve (self,feature,out_feature):
        arcpy.Dissolve_management(feature,out_feature, "BHR_rounded", "Top_of_Bank MAX;Drainage_mi2 MAX;Bankfull_Width_ft MAX;Bankfull_Depth_ft MAX;BHR_rounded MAX", "MULTI_PART", "UNSPLIT_LINES")
        
    def calc(self, feature, fields):
        with arcpy.da.UpdateCursor(feature,fields) as cursor:
        #Example:
        #Calculate price of property per acre
        """
            for row in cursor:
                if (row[2]>0):
                    LandPP = row[0]/row[2]
                    ParPP = row[1]/row[2]
                    row[3] = LandPP
                    row[4] = ParPP
                    cursor.updateRow(row)
                else:
                    row[3] = 0
                    row[4] = 0
                    cursor.updateRow(row)
                
        """





#Example:
#Intersect entire geodatabase with census data


"""
gdb = wrkspace("C:\Users\graham.farley\Downloads\Data\Piedmont_Streams")
for feat in gdb.ListOfFeatures: 
    out = "a_" + feat
    out_path = os.path.join("C:\Users\graham.farley\Downloads\Data\Piedmont_Intersects.gdb",out)
    census = "R:\_GIS_Data\Site_Search_Project\Data\CollectedData.gdb\Census"
    gdb.intersect(feat,census,out_path)"""







                   

        

