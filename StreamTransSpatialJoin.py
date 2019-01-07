import arcpy
import os
arcpy.env.overwriteOutput = True

"""This script reads from two different geodatabases, one containing stream 
delineations, and the other containing transects which have the top of bank for
that 20ft stretch of stream. This script maps the top of bank to the stream.""" 





StreamWorkspace = r"C:\Users\graham.farley\Downloads\Data\MountainStreams.gdb" #Change according to ecoregion
TransWorkspace = r"C:\Users\graham.farley\Downloads\Data\Mountain_Shortened.gdb" #"
OutWorkspace = r"C:\Users\graham.farley\Downloads\Data\MountainStreamsFinal.gdb" #"

arcpy.env.workspace = TransWorkspace

def JoinDrainage(streams,trans):
    
    targetFeatures = os.path.join(StreamWorkspace, streams)
    joinFeatures = os.path.join(TransWorkspace, trans)

    output_name = streams + "_Final"
    outfc = os.path.join(OutWorkspace,output_name)

    fieldmappings = arcpy.FieldMappings()
    
    fieldmappings.addTable(joinFeatures)
    #field mappings creates a sort of copy of the table to be joined, where you can
    #manipulate which fields are joined and by what method
    atts = ["Join_Count","TARGET_FID","LineOID"]

    for att in atts:
        x = fieldmappings.findFieldMapIndex(att)
        fieldmappings.removeFieldMap(x)

    fieldmappings.addTable(targetFeatures)


    
    drainage = fieldmappings.findFieldMapIndex("Top_of_Bank")
    fieldmap = fieldmappings.getFieldMap(drainage)


    fieldmap.mergeRule = "Min"          #If that stream intersects multiple transects, take the minimum ToB.
    fieldmappings.replaceFieldMap(drainage, fieldmap)


    arcpy.SpatialJoin_analysis(targetFeatures,joinFeatures,outfc,"#","#",fieldmappings)
    print(outfc)


trans = arcpy.ListFeatureClasses() #loop through all HUC8s in the ecoregion
for tran in trans:
    stream = tran[:-15]+"_Joined"
    print(stream)
    print tran
    JoinDrainage(stream,tran)
        
