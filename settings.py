""" Settings and defaults"""

SETTINGS = {
    'org_id': 123456789876543,
    'output_folder': 'outputs',
    'seq_out_file': 'seq_dataset.csv',
    'img_out_file': 'img_dataset.csv',
    'img_meta_out_file': 'img_meta_dataset.csv', # images with metadata
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
        'captured_at',
        'compass_angle',
        # 'computed_compass_angle', # doesn't exist for all, so removed it
        'thumb_256_url',
        # 'thumb_1024_url',
        # 'thumb_2048_url',
        # 'thumb_original_url',
        'width', # use this as a sketchy way to derive camera make
    ],
    'graph_endpoint': 'https://graph.mapillary.com',
}

try:
    from redacted import *
except ImportError:
    print("No redacted overrides found ...")
