'''
Package-wide constants.

Copyright 2020, Voxel51, Inc.
voxel51.com
'''
# pragma pylint: disable=redefined-builtin
# pragma pylint: disable=unused-wildcard-import
# pragma pylint: disable=wildcard-import
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from builtins import *
# pragma pylint: enable=redefined-builtin
# pragma pylint: enable=unused-wildcard-import
# pragma pylint: enable=wildcard-import

import os


# Directories
ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
MODELS_DIR = os.path.join(ROOT_DIR, "models")
AUTOML_DIR = os.path.join(ROOT_DIR, "automl")
EFFICIENTDET_DIR = os.path.join(AUTOML_DIR, "efficientdet")
