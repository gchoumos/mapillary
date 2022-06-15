
import base64
import mapbox_vector_tile


# helper function to decode geometries - taken by mapillary v4 api documentation
def decode_geometry(geometry):
    # from base64 format to a polygon
    decoded_geometry = mapbox_vector_tile.decode(
        base64.decodebytes(
            geometry.encode('utf-8')
        )
    )
    # could just return it at once - maybe a bit more readable this way
    return decoded_geometry
