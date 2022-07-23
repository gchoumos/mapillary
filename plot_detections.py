
import csv
import os
import time
from settings import SETTINGS

import matplotlib.pyplot as plt
import cv2
import numpy as np

import ast
from PIL import Image
from PIL import ImageDraw

from shapely.geometry import Polygon
from shapely.ops import cascaded_union, unary_union
import geopandas as gpd

import pdb

start = time.time()

# Get settings
out_dir  = SETTINGS['output_folder']
in_dir   = out_dir # Same directory

out_img_dir = SETTINGS['image_downloads_folder']
out_det_dir = SETTINGS['image_detections_folder']

# Here we'll store the images cropped according to the detections geometries
out_cropped_dir = SETTINGS['image_cropped_detections_folder']
# Create that directory if it doesn't already exist
if not os.path.isdir(out_cropped_dir):
    print("Output directory '{0}' for cropped images doesn't exist. Creating ...".format(out_cropped_dir))
    os.mkdir(out_cropped_dir)

# input files are the image detections output (from get_detections.py) and
# the images metadata output (from get_images_metadata.py)
detections_file  = SETTINGS['detections_out_file']
metadata_file = SETTINGS['img_meta_out_file']

# The image quality over which the detection masks will be plotted. Let's
# do this on the original quality at first (default value). We can change
# this later on so that we can apply them on any quality, by transforming
# the detection masks accordingly.
img_download_quality = SETTINGS['img_download_quality']

# Let's read the image metadata dataset, as a list.
with open('./{0}{1}{2}'.format(in_dir,os.path.sep,metadata_file), 'r') as images_meta_obj:
    # convert the input dataset to list of lists (list of rows)
    images = list(csv.reader(images_meta_obj))
    images_header = images[0]

    # Let's get the index of the image id and download url columns
    img_id_index = images_header.index('img_id')
    img_download_url_index = images_header.index('thumb_{0}_url'.format(img_download_quality))

    # And let's now keep only these columns
    # We skip the first row (as it's the header)
    # This is a fancy way to do what we want, but not an easily readable way
    images_rows = [[x[img_id_index],x[img_download_url_index]] for x in images[1:]]


# Let's read the detections
with open('./{0}{1}{2}'.format(in_dir,os.path.sep,detections_file), 'r') as detections_obj:
    # convert input dataset to list of lists (lists of rows)
    detections = list(csv.reader(detections_obj))
    detections_header = detections[0]

    # Get the index of the columns we'll keep from the detections dataset
    det_img_id_index = detections_header.index('img_id')
    det_det_id_index = detections_header.index('detections.id')
    det_det_value_index = detections_header.index('detections.value')
    det_decoded_geometry_index = detections_header.index('decoded_geometry')
    det_height = detections_header.index('height')

    detections_rows = [
        [
            x[det_img_id_index],
            x[det_det_id_index],
            x[det_det_value_index],
            x[det_decoded_geometry_index],
            x[det_height]
        ] for x in detections[1:] # [1:] is just in order to skip the header
    ]

n = 0

# Now iterate over the images, get the detections and plot them
for img in images_rows:
    # read this image
    cur_img_path = './{0}/{1}/{2}_{3}.jpg'.format(out_dir,out_img_dir,img[0],img_download_quality)
    cur_img = cv2.imread(cur_img_path)
    rgb_img = cv2.cvtColor(cur_img, cv2.COLOR_BGR2RGB)
    # plt.imshow(rgb_img)
    # plt.show()
    image = Image.open(cur_img_path)
    poly = Image.new('RGBA',image.size)
    # poly_mask = Image.new('RGBA',image.size)

    for det in detections_rows:
        # check if the current detection is of the current image
        # det[0] and img[0] correspond both to the image id
        if det[0] == img[0]:
            # Convert a string representation of a list "[[x1,y1],[x2,y2]]"
            # to a list of this type [(x1,y1),(x2,y2)]
            geom = [(x,int(det[4])-y) for [x,y] in ast.literal_eval(det[3])]
            pdraw = ImageDraw.Draw(poly)
            # pdraw_mask = ImageDraw.Draw(poly_mask)
            pdraw.polygon(geom,fill=SETTINGS['detection_colours'][det[2]],outline=(0,0,0,255))
            # pdraw_mask.polygon(geom,fill=)


    # This was moved outside of the iteration, as we don't have to paste each time for
    # each polygon but once for all of them
    image.paste(poly,mask=poly)
    pdb.set_trace()
    fig = plt.figure(figsize=(13, 8))
    fig.add_subplot(2,1,1)
    plt.imshow(rgb_img)
    plt.title('Initial image')

    fig.add_subplot(2,1,2)
    plt.imshow(image)
    plt.title('Image detections')

    fig.tight_layout()
    plt.show()

    if n > 5:
        break
    n += 1

    # # Prepare to plot again, this time with merged polygons
    # plt.clf()
    # image = Image.open(cur_img_path)
    # poly = Image.new('RGBA',image.size)
    # #####
    # # BLOCK START -The following block can become a tool in the mapillary_helper_tools.py script
    # #####
    # # Now merge all the geometries into 1
    # cur_img_detection_geometries_poly = [Polygon(x) for x in cur_img_detection_geometries]
    # cur_detections_merged = gpd.GeoSeries(unary_union(cur_img_detection_geometries_poly))
    # # After this we will have ended up with a geopandas dataframe with multiple rows, each representing
    # # a single polygon. That is normal as, when merging mulitple polygons, we will likely end up with
    # # a multipolygon as a result. That is because it is not necessary that merging the multiple polygons
    # # will lead to a single connected surface.
    # img_final_polygons = cur_detections_merged.explode()
    # # Now iterate over those polygons
    # for p in img_final_polygons[0]:
    #     # print("polygon coords: {0}".format(list(p.exterior.coords)))
    #     # Get the coordinates in a list of type [(x1, y1), (x2, y2), ...]
    #     cur_poly = list(p.exterior.coords)
    #     # cur_poly = list(p.geometry)
    #     # pdb.set_trace()
    #     pdraw = ImageDraw.Draw(poly)
    #     pdraw.polygon(cur_poly,fill=(255,0,255,128),outline=(0,0,0,255))
    # # This was moved outside of the iteration, as we don't have to paste each time for
    # # each polygon but once for all of them
    # image.paste(poly,mask=poly)
    # plt.imshow(image)
    # plt.show()
    # #######
    # # BLOCK END
    # #######

    # pdb.set_trace()

