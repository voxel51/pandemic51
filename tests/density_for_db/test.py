'''
Test that computes detections for all entries in the database that do not have
a `labels_path` column populated. The column is populated with the path to the
labels on disk.

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import pandemic51.core.density as pande


pande.compute_density_for_unprocessed_images()
