#import numpy as np
#import pickle
#from osgeo import gdal
#from gdalconst import GA_ReadOnly
#import os
#
#from dgcodecoop import lut_interpolator
# 
# 
#if __name__ == "__main__":
#
##    from pympler import tracker
#
#    interpolator = lut_interpolator.BarycentricLUTInterpolator()
#    
#    # import lut information
#    lut_file = "/mnt/panasas/pyoung/localmatch/ex4/luts/luts.p"
#    lut_tables, lut_coords, lut_map = pickle.load(open(lut_file, "rb"))
#    
#    # load coords into the interpolator in the same order as will be used below
#    for table_idx in range(0, len(lut_tables)):
#        coord_indices = np.nonzero(lut_map == table_idx)  # create filter that identifies all coords that use curr lut
#        interpolator.add_coords(lut_coords[coord_indices])  # add all coords that use curr lut
#
#    # open dataset
#    infile = "/mnt/panasas/pyoung/localmatch/ex4/in3/053266107010_01_P001_pansharpen.tif"
#    ds_in = gdal.Open(infile, GA_ReadOnly)
#    proj = ds_in.GetProjection()
#    geo_transform = ds_in.GetGeoTransform()
#
#    # create output dataset
#    print("Creating output dataset")
#    outfile = "/mnt/panasas/sstirlin/haha.tif"
#    driver = gdal.GetDriverByName("GTiff")
#    ds_out = driver.Create(outfile, ds_in.RasterXSize, ds_in.RasterYSize, 3, gdal.GDT_Byte)
#    ds_out.SetProjection(proj)
#    ds_out.SetGeoTransform(geo_transform)
#
##    memory_tracker = tracker.SummaryTracker()
#    
#    # read BGR data in, apply interpolator, and convert to 8-bit RGB
#    for band_num in range(1,4):
#
#        # read band in
#        print("Reading band %d in" % (4-band_num))
#        band_in = ds_in.GetRasterBand(4-band_num)
#        data_in = band_in.ReadAsArray()  # read into numpy
#
#        # add the luts for this band
#        interpolator.clear_luts()
#        for table_idx, lut_table in enumerate(lut_tables): # loop over luts
#            
#            # grab a raw pointer to the correct lut table
#            luts = lut_table[1]  #  the multi-band luts are stored in the second of a pair for some reason 
#            lut = luts[:, band_num-1]
#            coord_indices = np.nonzero(lut_map == table_idx)  # get all coord indices that use this lut
#            for coord in lut_coords[coord_indices]:
#                interpolator.add_luts([lut])
#
#        # allocate enough space
#        data_out = np.empty(shape=(0,0))
#
#        # apply the interpolator
#        print("Applying interpolator")
#        data_out = interpolator.apply_to_image(data_in, data_out, geo_transform)
#            
#        # write it out
#        print("Swapping bgr->rgb and writing band %d" % (band_num))
#        band_out = ds_out.GetRasterBand(band_num)
#        band_out.WriteArray(data_out)
#            
# #   memory_tracker.print_diff()
#    
#    # flush output file
#    ds_out = None
