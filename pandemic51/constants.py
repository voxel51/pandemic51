'''
Package-wide constants.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
import os


# Directories
ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
MODELS_DIR = os.path.join(ROOT_DIR, "models")
AUTOML_DIR = os.path.join(ROOT_DIR, "automl")
EFFICIENTDET_DIR = os.path.join(AUTOML_DIR, "efficientdet")
