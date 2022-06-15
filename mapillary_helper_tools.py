
import base64
import mapbox_vector_tile
import pdb


# Helper function to decode geometries - taken by mapillary v4 api documentation
# As stated in the documentation:
#   "To normalize this, divide each x and y coordinate by the extent (4096). To get
#    exact pixel coordinates, multiply the normalized x by the width of the image
#    containing the detection, and the normalized y coordinate by the height,
#    remembering that pixel coordinates start at the top left corner of the image
#    when visualized. Retrieve the height and width by making an API request for
#    the image key with the height and width fields."
def decode_geometry(geometry,width,height):
    # from base64 format to a polygon
    decoded_geometry = mapbox_vector_tile.decode(
        base64.decodebytes(
            geometry.encode('utf-8')
        )
    )

    # Get the extent
    extent = decoded_geometry['mpy-or']['extent']

    # Get the decoded geometry coordinates
    # The following command looks like that because the decoded geometry dictionary looks like this:
    # decoded_geometry = {
    #   'mpy-or': {
    #     'extent':   4096,
    #     'version':     2,
    #     'features': [{
    #       'geometry': {
    #         'type':        'Polygon',
    #         'coordinates': [[[3260, 18], [3273, 22], [3293, 22], [3291, 15], [3260, 18]]]
    #       },
    #       'properties': {},
    #       'id': 1,
    #       'type': 3
    #     }]
    #   }
    # }
    coordinates = decoded_geometry['mpy-or']['features'][0]['geometry']['coordinates'][0]

    # Now normalize the coordinates using the extent
    normalized_coordinates = []
    for coords in coordinates:
        normalized_coordinates.append([
            int((coords[0]/extent)*width), # multiply the normalized x by the width of the image
            int((coords[1]/extent)*height) # multiply the normalized y by the height of the image
        ])

    # pdb.set_trace()

    # could just return it at once - maybe a bit more readable this way
    return normalized_coordinates
