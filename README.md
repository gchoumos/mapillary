# Mapillary
## Useful tools for interacting with Mapillary API v4

* `get_sequences.py` script is fetching all sequence ids for a given organization id or user id in a given bounding box
* `get_images.py` script is fetching all image ids for a given set of sequences

Thus a use case scenario, is for an organization or user that wants to receive their images. They will
1. Run the `get_sequences.py` script using their `user_id` or `organization_id` and specifying their bounding box of interest
2. The result of the above execution is stored in the `outputs` folder (or however the user selects to change it) as a `seq_dataset.csv`
3. Run the `get_images.py` script, which will read the sequences from the `seq_dataset.csv` and fetch the image ids.
4. The result of the above execution will be stored as a `img_dataset.csv` in the `outputs` folder

This README file will be updated soon with comprehensive details.

Also, the repo will be updated with more functionality.

TBU

