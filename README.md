# Mapillary API v4 Toolset
**Useful tools for interacting with Mapillary API v4**

This repository includes a set of easy-to-use Python scripts that interact with Mapillary API v4 and can do a set of basic and useful operations.

The `settings.py` file is defining a dictionary of settings, and each script is reading the ones it needs. Thus, to modify the inputs/settings for your needs (like changing the Mapillary token, the bounding box, etc.) you can modify the `settings.py` file. More information on the settings is shared later on.



## Script to get sequences: `get_sequences.py`
This script is fetching all the sequence IDs for a given organization ID (or user ID) in a given bounding box. It generates a csv file that includes the sequence ids of the organization given in the bounding box specified.

In particular, each row will include 2 items.
1. `org_id` - the organization id (or user id) that owns the sequence
2. `seq_id` - the sequence id

Example Output:
```csv
org_id,seq_id
803468386961584,zK7pW0F1mgnaLiZbDqOjRI
803468386961584,Mr1jEG5HXBJxLfUS9Wtlp2
803468386961584,f72dwjtsgO6NQWEecSr5vU
```

In order for it to run properly, you have to make sure that the following settings in `settings.py` have been properly set:
* `token` - The Mapillary client access token that is required to query the API. It defaults to a random one, so you have to change it to your own. Let me know if you need help finding it!
* `org_id` - The organization id (or user id) that will own the sequences. You should be able to find yours through your Mapillary profile. Let me know though if you need help. The default value is random, thus will probably fetch no results
* `min_zoom` - The lowest zoom level that will be considered while searching for sequences. Defaults to 1. **I don't think you should change it**
* `max_zoom` - The maximum zoom level that will be considered while searching. Deafults to 14. **I don't think you should change it**
* `output_folder` - The directory where the outputs will be stored. It is considered to exist inside the current directory. If it doesn't exist, it will be created. The default is `outputs`.
* `seq_out_file` - The name of the output file that will hold the sequence ids. It defaults to `seq_dataset.csv`
* The bounding box settings dictionary (`AOI_bbox`). The default values include Cyprus
  * `ll_lat` - Lower left latitude of our bounding box
  * `ll_lon` - Lower left longitude of our bounding box
  * `ur_lat` - Upper right latitude of our bounding box
  * `ur_lon` - Upper right longitude of our bounding box



## Script to get image IDs of sequences `get_images.py`
This script is using the output of `get_sequences.py` as its input. It goes through the sequence IDs in that file, and retrieves the image IDs that belong to each. It generates a csv file that includes the pairs of sequence IDs and image IDs.

In particular, each row will include 2 items.
1. `seq_id` - a sequence id
2. `img_id` - id of an image belonging to that sequence

Example Output:
```csv
seq_id,img_id
SWxf3IwpsCM9GKBaetvkAy,1463097064038568
SWxf3IwpsCM9GKBaetvkAy,419363189104763
SWxf3IwpsCM9GKBaetvkAy,235997291422947
```

In order for it to run properly, you have to make sure that the following settings in `settings.py` have been properly set:
* `token` - The Mapillary client access token that is required to query the API. It defaults to a random one, so you have to change it to your own. Let me know if you need help finding it!
* `output_folder` - The directory where the outputs will be stored. It is considered to exist inside the current directory. If it doesn't exist, it will be created. The default is `outputs`
* `seq_out_file` - The output file of the `get_sequences.py` script. It will be used as input. You should not change it, unless you changed it previously, to run the `get_sequences.py` script.
* `img_out_file` - The name of the output file that will hold the sequence and image id pairs. It defaults to `img_dataset.csv`



## Script to get image details (image metadata) `get_images_metadata.py`
This script is using the output of `get_images.py` as its input. It goes through the image IDs in that file, and retrieves the image metadata that are configured in the `settings.py` file to be fetched. It generates a csv dataset file that includes the following (with the current configuration):
* `seq_id` - The sequence ID
* `img_id` - The image ID
* `captured_at` - The time of image capture (in miliseconds since unix epoch)
* `compass_angle` - The compass angle of the image
* `thumb_256_url` - The download url of the image in the lowest possible quality (for storage purposes), which is a 256-pixel wide thumbnail. You can easily configure the script to get a better quality image, don't worry!
* `width` - The width (in pixels) of the original uploaded image. I am including this as for my purposes it helps me understand which camera it was captured with.

Example Output:
```csv
seq_id,img_id,captured_at,compass_angle,thumb_256_url,width
SWxf3IwpsCM9GKBaetvkAy,935274303987496,1624790409193,184.43365478516,https://scontent.fath3-3.fna.fbcdn.net/m1/v/t6/An8SGFsS9Qc6zc_oGeGBjCnvE_YRykhTtQAtDDPEAT8gRi9P_e0WKmXL6ArVzayE4qEZ--YjlNEXluClT5nKoiXnfb2AvRW02kyuzZib_7EFNgvn2YLRw7hHcdbbe6zMzYaPHT_sIUMwA8U-Lx4xLg?stp=s256x144&ccb=10-5&oh=00_AT_vXUYInVUt62p-jt4cha31oXsYlI1RqeMZWSzhsVl06Q&oe=62A68E04&_nc_sid=122ab1,2560
SWxf3IwpsCM9GKBaetvkAy,571180097599390,1624790410195,184.89834594727,https://scontent.fath3-3.fna.fbcdn.net/m1/v/t6/An9yfyxI-EoHFSYBt7f1pjVbdpFHyCKpnWzYxgLh7V4AeycSGCw3s00RpbfxuGJU-2vvGWnxGQtzN9x9tLF81e3ix806wWKmVpcnTFCDmOwMV1B0UfKMX4vimDhiu8vekk9G8FziGz3qM8C1LQjxFg?stp=s256x144&ccb=10-5&oh=00_AT8XIp6IMHZbCpN1mEvyA1vJZ2Uq9RbaSk7l4GRRdSpOuQ&oe=62A7DBBC&_nc_sid=122ab1,2560
SWxf3IwpsCM9GKBaetvkAy,323654212518788,1624790412197,184.50595092773,https://scontent.fath3-3.fna.fbcdn.net/m1/v/t6/An-BfmG9eVwf0v6zIZQG6T3Ff-2paZ0FajpslmD0Iww7sFns4x16VOB817jsYgCz4mxgLQ4lYx__sIBDwBXFZ7X6fvjemVkGkFfEGVAYSXIleN330nhUGPVdkXEp8dMKSz09QTFA4LzQNNRz7LKyoQ?stp=s256x144&ccb=10-5&oh=00_AT-eZtxkMFIxl_KhY7f2Ot0g0N0QydiMV-F3LUo0VkRgCg&oe=62A78004&_nc_sid=122ab1,2560
```

In order for it to run properly, you have to make sure that the following settings in `settings.py` have been properly set:
* `token` - The Mapillary client access token that is required to query the API. It defaults to a random one, so you have to change it to your own. Let me know if you need help finding it!
* `output_folder` - The directory where the outputs will be stored. It is considered to exist inside the current directory. If it doesn't exist, it will be created. The default is `outputs`
* `img_out_file` - The name of the output file of the `get_images.py` script. This script uses that file as input. It defaults to `img_dataset.csv`
* `img_meta_out_file` - The name of the output csv dataset file. It will hold all the metadata information for each image. It defaults to `img_meta_dataset.csv`
* `graph_endpoint` - The Mapillary API v4 graph endpoint. You don't need to change that. The default is the correct one.
* `img_request_batch_size` - The batch size that will be used to simultaneously fetch results for images in a single request. Defaults to 50. I think you should not change that.
* `image_metadata_fields` - The fields that are requested for each image. Change this if you need more/less info. By default it will fetch the columns described above and displayed in the example output.



## Script to download images `download_images.py`
This script is using the output of `get_images_metadata.py` as its input. It downloads the images included in that file and stores them in a specific directory, that defaults to `./outputs/downloaded_images/`. The images are stored with the filename following the convention `<imageID_quality.jpg>`. Thus, an image with id `12345` and quality `256`, will be stored as `12345_256.jpg`.

Note that before attempting to download, the script will check if that particular image in that particular quality already exists. If it does, it will skip it. This means that if you start downloading lots of images, and for some reason the script stops, you can then re-run it and it will automatically pick up from where it left.

In order for it to run properly, you have to make sure that the following settings in `settings.py` have been properly set:
* `output_folder` - The directory where the outputs will be stored. It is considered to exist inside the current directory. If it doesn't exist, it will be created. The default is `outputs`
* `image_downloads_folder` - The folder name inside the `outputs` folder to store the actual images (or image thumbnails). Defaults to `downloaded_images`
* `img_download_quality` - The quality of image download. It defaults to `256`. Possible values are:
  * `256` - For a thumbnail of width 256 pixels (and adjusted height) (worst quality - smallest size)
  * `1024` - For a thumbnail of width 1024 pixels (and adjusted height)
  * `2048` - For a thumbnail of width 2048 pixels (and adjusted height)
  * `original` - For the original image (best quality - largest size)




Thus a use case scenario, is for an organization or user that wants to receive their images. They will
1. Run the `get_sequences.py` script using their `user_id` or `organization_id` and specifying their bounding box of interest
2. The result of the above execution is stored in the `outputs` folder (or however the user selects to change it) as a `seq_dataset.csv`
3. Run the `get_images.py` script, which will read the sequences from the `seq_dataset.csv` and fetch the image ids.
4. The result of the above execution will be stored as a `img_dataset.csv` in the `outputs` folder

This README file will be updated soon with more details. Let me know if you need specific instructions!

Also, the repo will be updated with more functionality. Next step is to incorporate detections.

