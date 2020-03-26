#!/usr/bin/env bash

# download images
eta gdrive download 1oMgp_SxuYKVbIYani4Zvst-dEZAnCRpW data/historical/images/abbey_road_imgs.zip
eta gdrive download 1k7R_uMjR46oKeArIoQnTTeYiS2M15XRr data/historical/images/chicago_imgs.zip
eta gdrive download 1w9hPEXhMlSQSqLsyxTNRuRE3Opjb8-Dr data/historical/images/dublin_imgs.zip
eta gdrive download 1w5d2i20zrzUeSj-6roiXAtbtdq-Io7e9 data/historical/images/new_jersey_imgs.zip
eta gdrive download 1CL-mVi0MksdaxfGgoChgVpnDpo2V1lkp data/historical/images/new_orleans_imgs.zip
eta gdrive download 13GXgVq2YkfBzl5CceobraBWA47SOuzC7 data/historical/images/prague_imgs.zip
eta gdrive download 1cXWzmgO-55MZD5SKarFM0Ti6q06vdDpo data/historical/images/timesquare_imgs.zip

# download labels
eta gdrive download 1ecceTHKsG0EaIv7rVN-xW6Aibbx_pMnN data/historical/labels/abbey_road_labels.zip
eta gdrive download 1oevPRh2CRbxaJKlQfv-gqF9JaXVc2P_V data/historical/labels/chicago_labels.zip
eta gdrive download 1KULdb9-ObktOe0BI0SgriBmuZROxA6Fo data/historical/labels/dublin_labels.zip
eta gdrive download 1IG2LtYVX66UtmQvmH8VI4nF0AwQBOH8g data/historical/labels/new_jersey_labels.zip
eta gdrive download 109eTOnhAQmVGGz_bFWJWXKy375rpAelS data/historical/labels/new_orleans_labels.zip
eta gdrive download 17MGY_9vD3vWrJbecDAyUDUoEWDN-a9Ui data/historical/labels/prague_labels.zip
eta gdrive download 1FpWEj6xeqvwTx0eEG69U_w99WfsSSL51 data/historical/labels/timesquare_labels.zip

unzip 'data/historical/images/*.zip' -d data/historical/images
unzip 'data/historical/labels/*.zip' -d data/historical/labels

rm data/historical/images/*.zip
rm data/historical/labels/*.zip
