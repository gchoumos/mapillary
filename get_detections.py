
import csv
import json
import os
import requests
import time
import pandas as pd
from vt2geojson.tools import vt_bytes_to_geojson
from settings import SETTINGS

# tools within this repo
from mapillary_helper_tools import decode_geometry

start = time.time()

# Get settings
out_dir  = SETTINGS['output_folder']
in_dir   = out_dir # Same directory

in_file  = SETTINGS['img_meta_out_file'] # input is the images metadata output (from get_images_metadata.py)
out_file = SETTINGS['detections_out_file']

# Base image request url
base_req_url = SETTINGS['graph_endpoint']
# Fetching image detections simultaneously for 20 images (atm)
img_detections_batch_size = SETTINGS['img_detections_batch_size']

# access token
token = SETTINGS['token']

# Get the image detections that we will be keeping. It would be nice to actually filter the detections that
# we will receive through the response, as we are likely only interested in "nature--vegetation", but I
# can't find any such server-side filtering available at the moment. At least nothing is mentioned in the
# documentation. Thus, I need to fetch them all, and filter them on the client side afterwards.
# Check, though, if any kind of detection limit is in place, as it has been mentioned in the forum that
# some people could only get 100 detections per image.
#   UPDATE: It looks that more than 100 can be returned. Check this img id: 728019821979741
# Unfortunately, no list of all available detections exists. Thus, we cannot be sure that we indeed keep
# everything we need
detections_to_keep = SETTINGS['detections_to_keep']

# To see/update which fields we'll be fetching and storing, check settings.py
img_det_fields = SETTINGS['image_detections_fields']

# Let's read the image metadata dataset
with open('./{0}{1}{2}'.format(in_dir,os.path.sep,in_file), 'r') as images_obj:
    # convert the input dataset to list of lists (list of rows)
    images = list(csv.reader(images_obj))
    # pdb.set_trace()
    images_header = images[0]
    images_rows = images[1:]

# We will prepare an image-detections dataset with the following columns (for now).
# It will be a csv file.
# - Sequence id (seq_id)
# - Image id (img_id)
# - field 1 (eg. captured_at)
# - field 2 (eg. compass_angle)
# - ... etc. (check settings)
# - add the decoded geometry in the end
#   (we get the geometry of a detection from the API, that is encoded as a base64
#    string, and we decode it to get image-specific coordinates)
dataset_header = ['img_id'] + [f for f in img_det_fields[1:]]
dataset_rows = [] # will be a list of rows (list of lists)

n_all_images = len(images_rows)
n_processed_images = 0
n_processed_detections = 0
n_included_detections = 0
print('Fetching detections of first {0} images out of {1} total ...'.format(img_detections_batch_size, n_all_images))


# Iterate through the image ids, batch by batch, and get the detections
while n_processed_images < len(images_rows):
    if n_processed_images > 0:
        print("Fetching detections of next batch ... Progress: {0} out of {1} images" \
                .format(n_processed_images, n_all_images))
    # Get all the image ids of the batch in a list
    img_ids = [
        # Should be the 1st element, but let's make sure by checking the header for 'img_id'
        x[images_header.index('img_id')]
        for x in images_rows[n_processed_images:n_processed_images+img_detections_batch_size]
    ]

    # build the request for this particular image batch
    img_det_req_url = '{0}?ids={1}&fields={2}&access_token={3}' \
                        .format(
                           base_req_url,
                            ','.join(img_ids),
                            ','.join(img_det_fields[1:]),
                            token
                        )

    # Send the request
    r = requests.get(img_det_req_url)
    assert r.status_code == 200, r.content

    # Get the content of the response as a json element
    img_features = json.loads(r.content)

    current_image_batch_data = []
    # Iterate through the image ids and get the details from the json response
    for img_id in img_ids:

        # Get the dictionary for this image
        cur_img = img_features[img_id]

        # Iterate through the image detections
        for detection in cur_img['detections']['data']:

            cur_detection = []

            # Skip this if not a detection we want to keep
            if detection['value'] not in detections_to_keep:
                continue

            # Append the information we need
            # For the moment (10/06/2022) they are the following
            # ..................................................
            # - 'id'            (for the image id)
            # - 
            # - 'width'
            # - 'height'
            cur_detection.append(cur_img['id'])
            cur_detection.append(cur_img['width'])
            cur_detection.append(cur_img['height'])
            cur_detection.append(detection['id'])
            cur_detection.append(detection['value'])
            cur_detection.append(detection['geometry'])

            # Decode the geometry to get the detection coordinates within the image
            # Send the width and the height of the original image, as they are needed
            # for the detection coordinate normalization
            cur_detection.append(decode_geometry(detection['geometry'],cur_img['width'],cur_img['height']))

            # Another counter/information for the included detections (the ones we wanted to keep)
            n_included_detections += 1


            # append the current image data to the rows of the dataset we are creating
            # only if not empty !
            dataset_rows.append(cur_detection)

        # Update number of processed detections before the next iteration
        n_processed_detections += len(cur_img['detections']['data'])

    # Update number of processed images before the next iteration
    n_processed_images += len(img_ids)

    # TBR
    # if n_processed_detections > 400:
    #     break


# Create output directory if it doesn't exist
if not os.path.isdir(out_dir):
    print("Output directory '{0}' doesn't exist. Creating ...".format(out_dir))
    os.mkdir(out_dir)

# Create the output dataset with all the image fields
with open(out_dir + os.path.sep + out_file, 'w') as outdat:
    writer = csv.writer(outdat)
    writer.writerow(dataset_header)
    for r in dataset_rows:
        writer.writerow(r)

print("Total images processed: {0}".format(n_processed_images))
print("Total detections processed: {0}".format(n_processed_detections))
print("Detections kept {0}".format(n_included_detections))
end = time.time()
print("Total time: {0}".format(end-start))
