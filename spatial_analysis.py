#
#Import spatial analysis module 
from arcpy.ia import *

#Set map 
aprx = arcpy.mp.ArcGISProject("CURRENT")
aprxMap = aprx.listMaps()[0]
aprxActive = aprx.activeMap  
sr = arcpy.SpatialReference(4326)
folder = "C:\FESM\\"

#FESM Input 
FESM_input = folder + "fesm_20200319_albers.tif"
FESM = aprxMap.addDataFromPath(FESM_input)

Buffer = 200

codeblock = """
def FireCalc(Fire, group):
    if Fire * group > 0:
        return 1 
    if Fire == group: 
        return 1 
    else:
        return 0"""   


for group in groups:
#Add point data 
    groups = ['Beetles', 'Bugs', 'Snails']
    csv_path = folder + group + "_points.csv"
    
#csv to Shapefile 
    arcpy.MakeXYEventLayer_management(csv_path, "Longitude", "Latitude", group, sr)
    arcpy.FeatureClassToShapefile_conversion(group, folder)
    shp_path = folder + group + ".shp"
    lyr = aprxMap.addDataFromPath(shp_path)
   

#Fire calculation
    expression = "FireCalc(!Fire!," + "!" + group + "_zonal_nsw.MEAN!)"
    arcpy.analysis.Buffer(lyr, folder + "Outputs\\" + group + "_buffer" , str(Buffer) + " Meters")
    ZonalStatisticsAsTable(folder + "Outputs\\" + group + "_buffer.shp", "Site", FESM, folder + "Outputs\\" + group + "_zonal_nsw.dbf")
    Layer = arcpy.management.AddJoin(folder + "Outputs\\" + group + "_buffer.shp", "Site", folder + "Outputs\\" + group + "_zonal_nsw.dbf", "Site")
    arcpy.management.CalculateField(Layer, "Agreement", expression, "PYTHON3", codeblock) 
    arcpy.TableToTable_conversion(Layer, folder + "Outputs\\", group + "_" + str(Buffer) + "_FESM.csv")
