import csv
import json
import os
import requests
import time
import pandas as pd
import pdb
from vt2geojson.tools import vt_bytes_to_geojson
from settings import SETTINGS

start = time.time()

# Get settings
out_dir  = SETTINGS['output_folder']
in_dir   = out_dir # Same directory

in_file  = SETTINGS['img_out_file'] # input is the images output (from get_images.py)
out_file = SETTINGS['img_meta_out_file']

# Base image request url
base_req_url = SETTINGS['graph_endpoint']

# access token
token = SETTINGS['token']

# Get the image metadata that we will be acquiring
# To see all available fields, check the "Image" section of the documentation:
#   https://www.mapillary.com/developer/api-documentation/#image
# To see/update which fields we'll be fetching and storing, check settings.py
img_fields = SETTINGS['image_metadata_fields']

# Read the image ids from the image dataset
# images = pd.read_csv('./{0}{1}{2}'.format(in_dir,os.path.sep,in_file), sep=',')

# Let's read the image dataset, as a list. Not as a pandas dataframe.
with open('./{0}{1}{2}'.format(in_dir,os.path.sep,in_file), 'r') as images_obj:
    # convert the input dataset to list of lists (list of rows)
    images = list(csv.reader(images_obj))
    # pdb.set_trace()
    images_header = images[0]
    images_rows = images[1:]

# We will prepare an images metadata dataset with the following columns (for now).
# It will be a csv file.
# - Sequence id (seq_id)
# - Image id (img_id)
# - field 1 (eg. captured_at)
# - field 2 (eg. compass_angle)
# - ... etc. (check settings)
dataset_header = ['seq_id','img_id'] + [f for f in img_fields]
dataset_rows = [] # will be a list of rows (list of lists)

n_all_images = len(images_rows)
n_processed_images = 1
print('Fetching first image out of {0} total ...'.format(n_all_images))
# Iterate through the image ids and get the metadata
for r in images_rows:
    # pdb.set_trace()
    seq = r[images_header.index('seq_id')]
    img = r[images_header.index('img_id')]

    if n_processed_images % 100 == 0:
        print('Processed images: {0} out of {1} ...'.format(n_processed_images,n_all_images))
    n_processed_images += 1

    # build the request for this particular image
    img_req_url = '{0}/{1}?access_token={2}&fields={3}' \
                    .format(
                        base_req_url,
                        img,
                        token,
                        ','.join(img_fields)
                    )

    # Send the request
    r = requests.get(img_req_url)
    assert r.status_code == 200, r.content

    # if n_processed_images > 400:
    #     break

    # Get the content of the response as a json element
    img_features = json.loads(r.content)

    current_image_data = [seq,img]
    # pdb.set_trace()
    for field in img_fields:
        current_image_data.append(img_features[field])

    # append the current image data to the rows of the dataset we are creating
    dataset_rows.append(current_image_data)


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
