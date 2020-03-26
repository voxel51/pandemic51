#!/usr/bin/env bash

# download images
#eta gdrive download 1oMgp_SxuYKVbIYani4Zvst-dEZAnCRpW data/historical/images/abbey_road_imgs.zip
eta gdrive download 1ZQlGK03DDS0xUus9p_rRU2-X1Uwrj7XQ data/historical/images/chicago_imgs.zip
#eta gdrive download 1w9hPEXhMlSQSqLsyxTNRuRE3Opjb8-Dr data/historical/images/dublin_imgs.zip
eta gdrive download 1Olbl6GsjdGRnBaOSmXQBfAOQdM8TDnYP data/historical/images/new_jersey_imgs.zip
eta gdrive download 1OHnq7xXWK38xVPWfZPWY5n1xt-OKg1wu data/historical/images/new_orleans_imgs.zip
eta gdrive download 1x76glhutlm83lur4xir2zyGwr-vUsMY_ data/historical/images/prague_imgs.zip
eta gdrive download 1YAnidd-3Xk2yuKJRQgeAXaj0Wj6uuuZj data/historical/images/timesquare_imgs.zip

# download labels
#eta gdrive download 1ecceTHKsG0EaIv7rVN-xW6Aibbx_pMnN data/historical/labels/abbey_road_labels.zip
eta gdrive download 1NbSdtf_8T8aCzuQbDgRlK8QYy1DtxhBB data/historical/labels/chicago_labels.zip
#eta gdrive download 1KULdb9-ObktOe0BI0SgriBmuZROxA6Fo data/historical/labels/dublin_labels.zip
eta gdrive download 1baRFipnf8GYvxwncxAFMZ2xFLUzTEp38 data/historical/labels/new_jersey_labels.zip
eta gdrive download 1Pl5WRTjGVvXD1iFBLU9emgnf_2N6pqjm data/historical/labels/new_orleans_labels.zip
eta gdrive download 1_gyQeA3hF58gH1HYofTPAokuSFfPKmt4 data/historical/labels/prague_labels.zip
eta gdrive download 1fpTfUFeXtkqyEWQucD4qfmfd-uoIBeim data/historical/labels/timesquare_labels.zip

unzip 'data/historical/images/*.zip' -d data/historical/images
unzip 'data/historical/labels/*.zip' -d data/historical/labels

rm data/historical/images/*.zip
rm data/historical/labels/*.zip
