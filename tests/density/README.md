# Person density test

## Download sample data

Download some sample images to `data/` by running the following commands:

```bash
mkdir -p data
eta gdrive download 1JgVbZHKMPjA82Vxohx0VjVo3bdVRenN0 data/timesquare_imgs.zip
unzip data/timesquare_imgs.zip -d data/
rm data/timesquare_imgs.zip
```


## Run test

Run a person density test by executing the test script:

```py
python test_person_density.py
```

The script outputs `ImageLabels` to `out/labels` and annotated images with the
predictions overlaid to `out/anno`.


## Copyright

Copyright 2017-2020, Voxel51, Inc.<br>
voxel51.com
