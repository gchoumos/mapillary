""" Settings and defaults"""

SETTINGS = {
    'org_id': 123456789876543,
    'output_folder': 'outputs',
    'image_downloads_folder': 'downloaded_images',
    'seq_out_file': 'seq_dataset.csv',
    'img_out_file': 'img_dataset.csv',
    'img_meta_out_file': 'img_meta_dataset_save.csv', # images with metadata
    'detections_out_file': 'img_detections_dataset.csv', # detections of images
    'token': 'MLY|1234567890123456|1234567890abcdef1234567890abcdef',
    'min_zoom': 1,
    'max_zoom': 14,
    'AOI_bbox': {
        # Define the lower left (ll) / upper right (ur) latitude and longitude
        # The current values are defining a bounding box for Cyprus
        'll_lat': 34.52,
        'll_lon': 32.19,
        'ur_lat': 35.49,
        'ur_lon': 34.18,
    },
    'image_metadata_fields': [
        'sequence',
        'id',
        'captured_at',
        'compass_angle',
        # 'computed_compass_angle', # doesn't exist for all, so removed it
        'thumb_256_url',
        # 'thumb_1024_url',
        # 'thumb_2048_url',
        # 'thumb_original_url',
        'width', # use this as a sketchy way to derive camera make
    ],
    'image_detections_fields': [
        'id',
        'width', # use this as a sketchy way to derive camera make
        'detections.id',
        'detections.value',
        'detections.geometry',
    ],
    'detections_to_keep': [
        'nature--terrain',
        'nature--vegetation',
        'nature--water'
    ],
    'graph_endpoint': 'https://graph.mapillary.com',
    # How many images to request for simultaneously
    # If requesting with GET, then better not increase this value to more than 50
    'img_request_batch_size': 50,
    # How many images to request detections for simultaneously
    'img_detections_batch_size': 20,
    # Potential quality values: 256, 1024, 2048, original
    # Note that in order for a value to work (e.g. 256), it must be present in the
    # images metadata csv. If it's not available, then the scripts should be run
    # with the appropriate settings first.
    'img_download_quality': '256',
}


# If you want to have redacted settings (e.g., have your application token
# automatically applied without it being visible publicly), you can create
# locally a "redacted.py" file, which is already git-ignored. In that file
# (which is attempted to be sourced right below), you can override the
# SETTINGS values. The following 2 lines are examples:
# """redacted.py"""
# SETTINGS['org_id'] = 987654321
# SETTINGS['token']  = 'MLY|0123456789012345|01234567890abcdef01234567890abc'
try:
    from redacted import *
except ImportError:
    print("No redacted overrides found ...")
