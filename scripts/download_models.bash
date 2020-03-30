#!/usr/bin/env bash
# Script for downloading the detector model checkpoints.
#
# Copyright 2020, Voxel51, Inc.
# voxel51.com
#

#eta gdrive download 1sc3aVx2SIcxar6ah6rg7qiGoecY0m6nK models/efficientdet-d0.tar
#eta gdrive download 1xjNuRv58uh3eWy2Hc6KTNfdRNRG8-3rP models/efficientdet-d1.tar
#eta gdrive download 15ycqxKVNmi-XEMJgPPShleNxXeDRRQvL models/efficientdet-d2.tar
#eta gdrive download 1lHwppExWGE1o-vyE6E1FiadmUIyhdcCA models/efficientdet-d3.tar
eta gdrive download 1OwRBADz6fCdfQGjr57wvTwGOTtzmBld_ models/efficientdet-d4.tar
#eta gdrive download 1_DZMF_N3MRLeqi34DbPx1Vx7wHtV0rhM models/efficientdet-d5.tar
#eta gdrive download 1cFG1kA1U_CinTodRSYtGAH9esZQWsd-w models/efficientdet-d6.tar

tar -xvf models/*.tar -C models/
rm models/*.tar
