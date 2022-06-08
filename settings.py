""" Settings and defaults"""

SETTINGS = {
    'org_id': 123456789876543,
    'output_folder': 'outputs',
    'token': 'MLY|1234567890123456|1234567890abcdef1234567890abcdef',
    'min_zoom': 1,
    'max_zoom': 14,
    'AOI_bbox': {
        # Our AOI in Cyprus
        'll_lat': 34.52,
        'll_lon': 32.19,
        'ur_lat': 35.49,
        'ur_lon': 34.18,
    }
}

try:
    from redacted import *
except ImportError:
    print("No redacted overrides found ...")
