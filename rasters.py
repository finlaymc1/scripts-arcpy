#These instructions are for working with Python fom a Notebook in ArcGis Pro 
#First create a ArcGis Pro Project
#Under the Insert tab add a new base map and a notebook 

#If you are working with Python from a notebook in ArcGis Pro you don't need to import the ArcPy module 
#If you want to work with Python from a seperate IDE then import the ArcPy module 
import arcpy

#Setting up your environment 
#Define the ArcGic Pro project 
aprx = arcpy.mp.ArcGISProject("CURRENT")

#Define the map 
#You can either use the active map or choose the map by index 
aprxMap = aprx.listMaps()[0]
aprxActive = aprx.activeMap  

#Define the spatial reference you want to use 
sr = arcpy.SpatialReference(4326)

#When you create your ArcGis Pro project this also automatically creates a File Geodatabase with your project name and and the extension ".GDB" 
#This File GDB is your default workspace for creating layers
#You can comfirm this by running the following 
arcpy.env.workspace 

#Alternative steps for creating your own File GDB 
arcpy.management.CreateFileGDB(out_folder_path, out_name, {out_version})

#Set the File GDB as your workspace 
#You can only have one GDB as your workspace at one time 
arcpy.env.workspace = r"<location_path>\<name>.gdb" #path to GDB

#The Scratch Workspace is intended for output data you do not want to maintain
arcpy.env.scratchWorkspace = r"<location_path>\<name>.gdb" #path to scratch GDB 

#Now that we have setup our environment let's save some layers to our File GDB
#Function for saving a table e.g. a CSV file 
arcpy.conversion.TableToTable(in_rows, out_path, out_name, {where_clause}, {field_mapping}, {config_keyword})

#Function for converting a Feature Class to Feature Class e.g. a Shapefile to Feature Class in a GDB 
arcpy.conversion.FeatureClassToFeatureClass(in_features, out_path, out_name, {where_clause}, {field_mapping}, {config_keyword})

#Storing rasters in GDB 
arcpy.conversion.RasterToGeodatabase(Input_Rasters, Output_Geodatabase, {Configuration_Keyword})

#Working with raster data
#To work with raster data we need to import the Spatial Analyst ArcPy module 
from arcpy.sa import *

#List all the rasters available in the GDB 
raster_list = arcpy.ListRasters("*")
print (raster_list)

#Let's do some raster calculations 
#Let's create median annual temperature  
outRaster = 0.5 * Raster(Mean_max_temp) + 0.5 * Raster(Mean_min_temp) 
outRaster.save("Annual_mean_temp")

#Let's create mean diurnal range 
outRaster = Raster(Mean_max_temp) - Raster(Mean_min_temp)
outRaster.save(Mean_diurnal_range")

#Let's create isothermality 
outRaster = Raster(Mean_diurnal_range)/Raster(Temp_annual_range)
outRaster.save(Isothermality.tif")

#All these calculations are utilising Map Algebra available through the Spatial Analyst module 
#For more information see: https://pro.arcgis.com/en/pro-app/latest/help/analysis/spatial-analyst/mapalgebra/what-is-map-algebra.htm

#Some geoprocessing functions useful for rasters 
#Projection 
#For the out_coor_system you can either use the sr variable we previously defined or another raster 
arcpy.management.ProjectRaster(in_raster, out_raster, out_coor_system, {resampling_type}, {cell_size}, {geographic_transform}, {Registration_Point}, {in_coor_system}, {vertical})

#Resample 
#Again with the cell_size you can either use an existing raster or specify the the width (y) and height (x) 
arcpy.management.Resample(in_raster, out_raster, {cell_size}, {resampling_type})

#Clip 
#The rectangle determines the clip extent. It takes either an envelope e.g. rectangle = "1952602.23 294196.279 1953546.23 296176.279", or a Feature Class or Feature Layer as input 
#If you want the layers to clip exactly set mantain_clipping_extent = "MAINTAIN_EXTENT"
arcpy.management.Clip(in_raster, rectangle, out_raster, {in_template_dataset}, {nodata_value}, {clipping_geometry}, {maintain_clipping_extent})
