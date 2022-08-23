#This code was used as part of the Australian Government's Wildlife and Habitat Bushfire Recovery Program 
#It was used to determine mean, max etc. fire severity for different invertebrate species sites 
#Fire intensity and severity mapping (FESM) is provided by NSW DPIE(https://datasets.seed.nsw.gov.au/dataset/fire-extent-and-severity-mapping-fesm)

#Mean FESM values were used to determine the level of agreement between on on-ground assessments of fire severity and FESM 
#Working with shapefiles here but you could also do a similar process with gdb 

#Import spatial analysis module 
#If working from outside ArcGis Pro need to import arcpy module 
from arcpy.ia import *

#Set map and environment 
# If working from outside ArcGis Pro need to set the path to the project file e.g. r"C:/files/project.aprx"
aprx = arcpy.mp.ArcGISProject("CURRENT")
aprxMap = aprx.listMaps()[0]
aprxActive = aprx.activeMap  
sr = arcpy.SpatialReference(4326)
folder = "C:\FESM\\"

#FESM Input 
FESM_input = folder + "fesm.tif"
FESM = aprxMap.addDataFromPath(FESM_input)

#Set buffer distance to be 200 metres 
Buffer = 200

#Python codeblock for comparing on-ground fire severity and FESM 
codeblock = """
def FireCalc(Fire, group):
    if Fire * group > 0:
        return 1 
    if Fire == group: 
        return 1 
    else:
        return 0"""   


#Create a for loop to loop through the different intervebrate types(beetles, bugs and snails) 
for group in groups:
    #Set groups and csv path 
    groups = ['Beetles', 'Bugs', 'Snails']
    csv_path = folder + group + "_points.csv"
    
    #For each invertebrate type create point data with associated attribute table based on field data 
    arcpy.MakeXYEventLayer_management(csv_path, "Longitude", "Latitude", group, sr)
    arcpy.FeatureClassToShapefile_conversion(group, folder)
    shp_path = folder + group + ".shp"
    lyr = aprxMap.addDataFromPath(shp_path)
   
    #Create 200 metre buffer around point data 
    #Buffers represent the search area for each individual invertebrate 
    arcpy.analysis.Buffer(lyr, folder + "Outputs\\" + group + "_buffer" , str(Buffer) + " Meters")
    
    #Summarize FESM raster data using zonal statistics and search area buffers as inputs 
    ZonalStatisticsAsTable(folder + "Outputs\\" + group + "_buffer.shp", "Site", FESM, folder + "Outputs\\" + group + "_zonal_nsw.dbf")
    
    #Create a join between buffer and FESM zonal statistics table
    Layer = arcpy.management.AddJoin(folder + "Outputs\\" + group + "_buffer.shp", "Site", folder + "Outputs\\" + group + "_zonal_nsw.dbf", "Site")
    
    #Calculate field to determine level of agreement between on-ground assessment and fire severity 
    expression = "FireCalc(!Fire!," + "!" + group + "_zonal_nsw.MEAN!)"
    arcpy.management.CalculateField(Layer, "Agreement", expression, "PYTHON3", codeblock) 
    
    #Output table as a csv 
    arcpy.TableToTable_conversion(Layer, folder + "Outputs\\", group + "_" + str(Buffer) + "_FESM.csv")
