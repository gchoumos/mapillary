# This script uses an ID (organization or user) and a bbox as input
# and it finds all the sequences of images belonging to that id.
# The result is saved in a sequences_dataset.csv

import csv
import json
import math
import os
import pdb
import requests
import time
from vt2geojson.tools import vt_bytes_to_geojson
from settings import SETTINGS

start = time.time()

# Get settings
min_zoom = SETTINGS['min_zoom']
max_zoom = SETTINGS['max_zoom']
org_id   = SETTINGS['org_id']
out_dir  = SETTINGS['output_folder']
out_file = SETTINGS['seq_out_file']
token    = SETTINGS['token']

# check if valid to remove
seen = []

# https://stackoverflow.com/questions/13757736/python-deg2num-syntax-error)
def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * n)
    return (xtile, ytile)

output = {"type":"FeatureCollection","features":[]}
# Let's set the following as set (pun intended) so that they are definitely unique
# and we reduce the possibility of unnecessary requests (as quotas are in place)
sequences = set()
organizations = set ()

# We will also prepare a sequences dataset with the following columns (for now).
# It will be a csv file.
# - Organization id (org_id)
# - Sequence id (seq_id)
dataset_header = ['org_id','seq_id']
dataset_rows = [] # will be a list of rows (list of lists)

# Create output directory if it doesn't exist
if not os.path.isdir(out_dir):
    print("Output directory '{0}' doesn't exist. Creating ...".format(out_dir))
    os.mkdir(out_dir)

# There are 2 cases of requests to mapillary depending if using original (?)
# or computed tiles. We will use the original, though I don't yet know the
# actual difference (having tested it out of curiosity, the tiles returned
# on my dummy example where the same)
mly_std = 'mly1_public'
mly_comp = 'mly1_computed_public'

def check_tile(z1,x1,y1):
    # move this to the settings maybe?
    url = "https://tiles.mapillary.com/maps/vtp/{0}/2/{1}/{2}/{3}?access_token={4}" \
            .format(mly_std,z1,x1,y1,token)
    print("Sending request:\n {}".format(url))
    if url in seen:
        return 1
    seen.append(url)

    r = requests.get(url)
    assert r.status_code == 200, r.content
    vt_content = r.content

    features = vt_bytes_to_geojson(vt_content, x1, y1, z1)

    if str(org_id) in (json.dumps(features)):
        if z1<max_zoom:
            print (z1,x1,y1)
            check_tile(z1+1,2*x1,2*y1)
            check_tile(z1+1,2*x1+1,2*y1)
            check_tile(z1+1,2*x1,2*y1+1)
            check_tile(z1+1,2*x1+1,2*y1+1)
        else:
            for f in features['features']:
                if 'organization_id' in f['properties'] and \
                    'sequence_id' in f['properties']:

                    org = f['properties']['organization_id']
                    seq = f['properties']['sequence_id']
    
                    if org == org_id and seq not in sequences:
                        # Add the sequence to the sequences set
                        # Also add a row to the output dataset of (organization,sequence) pairs
                        sequences.add(seq)
                        dataset_rows.append([org,seq])


# Define the bounding box we care for in Cyprus
ll_lat = SETTINGS['AOI_bbox']['ll_lat']
ll_lon = SETTINGS['AOI_bbox']['ll_lon']
ur_lat = SETTINGS['AOI_bbox']['ur_lat']
ur_lon = SETTINGS['AOI_bbox']['ur_lon']

 
# Starting at level z (1)
llx,lly = deg2num (ll_lat, ll_lon, z)
urx,ury = deg2num (ur_lat, ur_lon, z)
output = {"type":"FeatureCollection","features":[]}
print("Starting drill down of tiles from zoom level {0}, to zoom level {1}."
    .format(z,max_zoom))
print("Will focus and further zoom only if target id (user/organization) exists in the zoomed tile.")

for x in range(min(llx,urx),max(llx,urx)+1,1):
    for y in range(min(lly,ury),max(lly,ury)+1,1):
        check_tile(z,x,y)

with open(out_dir + os.path.sep + str(org_id) + '.geojson', 'w') as outfile:
    json.dump(output, outfile)

with open(out_dir + os.path.sep + 'sequences_' + str(org_id) + '.txt', 'w') as outseq:
    for sequence in sequences:
        outseq.write('%s\n' % sequence)

with open(out_dir + os.path.sep + 'organizations_' + str(org_id) + '.txt', 'w') as outorg:
    for organization in organizations:
        outorg.write('%s\n' % organization)

# Create also an output file that will be the "dataset" holding in each row:
# - Organization ID
# - Sequence ID
with open(out_dir + os.path.sep + out_file, 'w') as outdat:
    writer = csv.writer(outdat)
    writer.writerow(dataset_header)
    for r in dataset_rows:
        writer.writerow(r)

end = time.time()
print("Total time: {0}".format(end-start))
