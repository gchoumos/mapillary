
import csv
import json
import os
import requests
import time
import pandas as pd
from vt2geojson.tools import vt_bytes_to_geojson
from settings import SETTINGS

start = time.time()

# Get settings
out_dir  = SETTINGS['output_folder']
in_dir   = out_dir # Same directory

out_file = SETTINGS['img_out_file']
in_file  = SETTINGS['seq_out_file'] # input for images for our purpose is the output of sequences

org_id   = SETTINGS['org_id']
token    = SETTINGS['token']

# Read the input csv file (sequences dataset)
sequences = pd.read_csv('./{0}{1}{2}'.format(in_dir,os.path.sep,in_file), sep=',')

# pdb.set_trace()

# We will prepare an images dataset with the following columns (for now).
# It will be a csv file.
# - Sequence id (seq_id)
# - Image id (img_id)
dataset_header = ['seq_id','img_id']
dataset_rows = [] # will be a list of rows (list of lists)

# Let's set the following as set (pun intended) so that they are definitely unique
# and we reduce the possibility of unnecessary requests (as quotas are in place)
images = set()
n_images = 0

for seq in sequences['seq_id']:
    # Get images for each sequence
    print("Requesting images of sequence with id: {0}".format(seq))
    req_url = "https://graph.mapillary.com/image_ids?access_token={0}&sequence_id={1}" \
        .format(token,seq)
    r = requests.get(req_url)
    assert r.status_code == 200, r.content

    # Get the content of the response as a json element
    features = json.loads(r.content)
    n_images += len(features['data'])
    print("Sequence with id {0} has {1} images".format(seq,len(features['data'])))

    # The below is just fancy way to append a [seq_id, img_id] for each img_id in the response
    # dataset_rows.append([seq,img['id'] for img in features['data']])
    dataset_rows += [[seq,img['id']] for img in features['data']]


# Create output directory if it doesn't exist
if not os.path.isdir(out_dir):
    print("Output directory '{0}' doesn't exist. Creating ...".format(out_dir))
    os.mkdir(out_dir)


# with open(out_dir + os.path.sep + 'sequences_' + str(org_id) + '.txt', 'w') as outseq:
#     for sequence in sequences:
#         outseq.write('%s\n' % sequence)

# Create also an output file that will be the "dataset" holding in each row:
# - Sequence ID
# - Image ID
with open(out_dir + os.path.sep + 'img_dataset.csv', 'w') as outdat:
    writer = csv.writer(outdat)
    writer.writerow(dataset_header)
    for r in dataset_rows:
        writer.writerow(r)

print("Total number of images processed: {0}".format(n_images))
end = time.time()
print("Total time: {0}".format(end-start))
