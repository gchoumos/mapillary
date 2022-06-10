
import csv
import os
import wget
import time
from settings import SETTINGS

start = time.time()

# Get settings
out_dir  = SETTINGS['output_folder']
in_dir   = out_dir # Same directory

out_img_dir = SETTINGS['image_downloads_folder']
# input file is the images metadata output (from get_images_metadata.py)
in_file  = SETTINGS['img_meta_out_file']

img_download_quality = SETTINGS['img_download_quality']

# Let's read the image metadata dataset, as a list.
with open('./{0}{1}{2}'.format(in_dir,os.path.sep,in_file), 'r') as images_meta_obj:
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

# Create outputs directory if it doesn't exist (it should exist though)
if not os.path.isdir(out_dir):
    print("Output directory '{0}' doesn't exist. Creating ...".format(out_dir))
    os.mkdir(out_dir)

# Create image downloads directory inside the outputs directory if it doesn't exist
if not os.path.isdir('{0}/{1}'.format(out_dir,out_img_dir)):
    print("Image downloads directory '{0}/{1}' doesn't exist. Creating ... ".format(out_dir,out_img_dir))
    os.mkdir('{0}/{1}'.format(out_dir,out_img_dir))

# Use these to display the progress
iteration = 0
downloaded = 0
to_download = len(images_rows)
# Iterate through the images and download
for img in images_rows:
    id = img[0]
    download_url = img[1]
    iteration += 1
    # We should download the file only if it doesn't already exist!
    if not os.path.exists('{0}/{1}/{2}_{3}.jpg'.format(out_dir,out_img_dir,id,img_download_quality)):
        print("Downloading image {0} out of {1}".format(downloaded,to_download))
        wget.download(download_url,'{0}/{1}/{2}_{3}.jpg'.format(out_dir,out_img_dir,id,img_download_quality))
        downloaded += 1
    else:
        print("This image in this quality already exists! Not downloading.")

print('\n')
print("Finished")
print("--------")
print("Images in the dataset: {0}".format(len(images_rows)))
print("Images downloaded: {0}".format(downloaded))
print("Images that already existed: {0}".format(len(images_rows)-downloaded))

end = time.time()
print("Total time: {0}".format(end-start))
