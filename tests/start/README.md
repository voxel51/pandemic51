# Tests

This test is a set of scripts that run simple tasks. Each depends on the
output of the previous, so run the scripts in this order:

1) `download_stream.py`
2) `convert_videos_to_images.py`
3) `test_tflite_inference.py`

Before running the detector be sure to download the model via:

```bash
bash download_model.bash
```


## Copyright

Copyright 2017-2020, Voxel51, Inc.<br>
voxel51.com
