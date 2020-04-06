'''
Run this every 15 minutes to get the current image that is being displayed
(this is not a livestream)

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import io
import requests

import numpy as np
from PIL import Image

import eta.core.image as etai
import pandemic51.core.streaming as pans


# Ypsilanti (EMU Campus)
webpage = "https://www.weatherbug.com/weather-camera/?cam=PSLNM"

# Get the source from the page
urls = pans.get_img_urls(webpage)
filtered_urls = [u for u in urls if "PSLNM" in u]

for url in filtered_urls:
    # Get the large version of the image instead of the thumbnail
    url = url[:-5]+"l"+url[-4:]
    data = requests.get(url).content
    img = np.array(Image.open(io.BytesIO(data)))
    time = url.split("/")[-1].split("_")[0]
    print("Downloading url")
    etai.write(img, "out/ypsilanti/"+time+".jpg")

if len(filtered_urls) == 0:
    print("No matching images found")

