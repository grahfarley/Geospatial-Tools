import arcpy
import os

arcpy.env.overwriteOutput = True

"""This script reads from two different geodatabases, one containing transect
polylines, and the other containing the shortened transects. The longer segments also contain
the top-of-bank. This script spatially joins the smaller transects with the lowest top-of-bank.""" 





TransWorkspace = r"C:\Users\graham.farley\Downloads\Data\MountainTransects.gdb"         #The workspace needs to be changed based on which ecoregion you're working in
ShortWorkspace = r"C:\Users\graham.farley\Downloads\Data\Mountain_Shortened.gdb"        #"
OutWorkspace = ShortWorkspace

arcpy.env.workspace = TransWorkspace

def JoinDrainage(Trans,Truncated):
    print(Trans)
    targetFeatures = os.path.join(ShortWorkspace, Truncated)    #The Shorten Polylines tool produces feature classes of the same name as the input
    joinFeatures = os.path.join(TransWorkspace, Trans)
    print(joinFeatures)
    output_name = Trans + "_Short"
    outfc = os.path.join(OutWorkspace,output_name)      #The output feature class will be "(HUC8 Name)_Short"

    fieldmappings = arcpy.FieldMappings()
    
    fieldmappings.addTable(joinFeatures)

    atts = ["x_start","y_start","x_end","y_end"]

    for att in atts:                                    #Gets rid of some of the extraneous fields picked up throughout the process
        x = fieldmappings.findFieldMapIndex(att)
        print(x)
        fieldmappings.removeFieldMap(x)

    fieldmappings.addTable(targetFeatures) 

    att = "Value"
    x = fieldmappings.findFieldMapIndex(att)
    fieldmappings.removeFieldMap(x)
    
    drainage = fieldmappings.findFieldMapIndex("Top_of_Bank")
    fieldmap = fieldmappings.getFieldMap(drainage)


    fieldmap.mergeRule = "Min"                          #We want the lowest top-of-bank, although there should only be one that meets the join criteria
    fieldmappings.replaceFieldMap(drainage, fieldmap)


    arcpy.SpatialJoin_analysis(targetFeatures,joinFeatures,outfc,"#","#",fieldmappings,"SHARE_A_LINE_SEGMENT_WITH") #Apply the field mapping and join only those features that share a line segment

fcs = arcpy.ListFeatureClasses()
print(fcs)
for fc in fcs:
    JoinDrainage(fc,fc)     #Again, they'll have the same names, but different locations. 

        
