# Object density test

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


## Run test

Compute object density by executing the test script:

```py
python compute_object_density.py
```

The script outputs `ImageLabels` to `out/labels` and annotated images with the
predictions overlaid to `out/anno`.

Plot the outputs of the above script by running the following script:

```py
python plot_object_density.py
```


## Copyright

Copyright 2017-2020, Voxel51, Inc.<br>
voxel51.com
