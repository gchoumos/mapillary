import csv
import json
import os
import requests
import time
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
# Fetching 50 image ids simultaneously is well within the get request length limit
# (around 1250 chars). However, I should probably convert this to a POST request
img_batch_size = SETTINGS['img_request_batch_size']

# access token
token = SETTINGS['token']

# Get the image metadata that we will be acquiring
# To see all available fields, check the "Image" section of the documentation:
#   https://www.mapillary.com/developer/api-documentation/#image
# To see/update which fields we'll be fetching and storing, check settings.py
img_fields = SETTINGS['image_metadata_fields']

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
dataset_header = ['seq_id','img_id'] + [f for f in img_fields[2:]]
dataset_rows = [] # will be a list of rows (list of lists)

n_all_images = len(images_rows)
n_processed_images = 0
print('Fetching first {0} images out of {1} total ...'.format(img_batch_size, n_all_images))

# Iterate through the image ids, batch by batch, and get the metadata
while n_processed_images < len(images_rows):
    if n_processed_images > 0:
        print("Fetching next batch ... Progress: {0} out of {1} images" \
                .format(n_processed_images, n_all_images))
    # Get all the image ids of the batch in a list
    img_ids = [
        # Should be the 2nd element, but let's make sure by checking the header for 'img_id'
        x[images_header.index('img_id')]
        for x in images_rows[n_processed_images:n_processed_images+img_batch_size]
    ]

    # build the request for this particular image batch
    img_req_url = '{0}?ids={1}&fields={2}&access_token={3}' \
                    .format(
                        base_req_url,
                        ','.join(img_ids),
                        ','.join(img_fields),
                        token
                    )

    # Send the request
    r = requests.get(img_req_url)
    assert r.status_code == 200, r.content

    # Get the content of the response as a json element
    img_features = json.loads(r.content)

    # Iterate through the image ids and get the details from the json response
    for img_id in img_ids:
        cur_img_metadata = []
        # Get the dictionary for this image
        cur_img = img_features[img_id]
        # Append the information we need
        # For the moment (10/06/2022) they are the following
        # ..................................................
        # - 'sequence'      (for the sequence id)
        # - 'id'            (for the image id)
        # - 'captured_at'   (in unix ms)
        # - 'compass_angle'
        # - 'thumb_256_url'
        # - 'width'
        for field in img_fields:
            cur_img_metadata.append(cur_img[field])

        # append the current image data to the rows of the dataset we are creating
        dataset_rows.append(cur_img_metadata)

    # Update number of processed images for the next iteration
    n_processed_images += len(img_ids)

    # TBR
    # if n_processed_images > 40:
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
end = time.time()
print("Total time: {0}".format(end-start))
