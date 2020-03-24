'''
Downloads EfficientDet models from Google Drive to `models/`.

Copyright 2020 Voxel51, Inc.
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

import eta.core.storage as etas
import eta.core.utils as etau


def download_model(fid, outpath):
    client = etas.GoogleDriveStorageClient()
    client.download(fid, outpath)
    etau.extract_archive(outpath)
    etau.delete_file(outpath)


download_model("1sc3aVx2SIcxar6ah6rg7qiGoecY0m6nK", "models/efficientdet-d0.tar")
download_model("1xjNuRv58uh3eWy2Hc6KTNfdRNRG8-3rP", "models/efficientdet-d1.tar")
download_model("15ycqxKVNmi-XEMJgPPShleNxXeDRRQvL", "models/efficientdet-d2.tar")
download_model("1lHwppExWGE1o-vyE6E1FiadmUIyhdcCA", "models/efficientdet-d3.tar")
download_model("1OwRBADz6fCdfQGjr57wvTwGOTtzmBld_", "models/efficientdet-d4.tar")
download_model("1_DZMF_N3MRLeqi34DbPx1Vx7wHtV0rhM", "models/efficientdet-d5.tar")
download_model("1cFG1kA1U_CinTodRSYtGAH9esZQWsd-w", "models/efficientdet-d6.tar")
