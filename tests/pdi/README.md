# Physical distancing index (PDI) tests

## Download sample data

Download some sample images to `data/` by running the following commands:

```bash
eta gdrive download-dir 1RE-JMlKLYpQbfOkbwMFRhr_xaQ7ULVl_ data/

shopt -s nullglob
for f in data/*.zip; do
    unzip $f  -d data/
    rm $f
done
```


## Compute some PDIs

Compute object counts by executing the script:

```py
python compute_object_counts.py
```

The script outputs `eta.core.images.ImageLabels` to `out/labels` and annotated
images with the predictions overlaid to `out/anno`.

Plot the outputs of the above script by running the following script:

```py
python plot_pdis.py
```


## Copyright

Copyright 2017-2020, Voxel51, Inc.<br>
voxel51.com
