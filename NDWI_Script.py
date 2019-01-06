import os
import arcpy
from arcpy.sa import Raster, Float
arcpy.env.workspace = "D:\NC_NAIP"
arcpy.CheckOutExtension('spatial')
arcpy.env.overwriteOutput = True

"""
Calculates the NDWI given the NAIP imagery on the external HDD
"""
os.chdir("D:\NC_NAIP")
files = [f for f in os.listdir("D:\NC_NAIP") if "_" in f]

print(len(files))

for f in files:
    band2 = Raster("D:\NC_NAIP\\"+f+"\Band_2")
    
    band4 = Raster("D:\NC_NAIP\\"+f+"\Band_4")
    ndvi = (arcpy.sa.Float(band2)-arcpy.sa.Float(band4))/(arcpy.sa.Float(band4)+arcpy.sa.Float(band2))
    
    new_name = f[:-4]+"NDWI.tif"
    ndvi.save(r'D:\NC_NDWI\a'+new_name)


