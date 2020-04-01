'''
Run this every 15 minutes to get the current image that is being displayed
(this is not a livestream)

Copyright 2020 Voxel51, Inc.
voxel51.com
'''
import io
import requests

from bs4 import BeautifulSoup
import numpy as np
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

import eta.core.image as etai


# Ypsilanti (EMU Campus)
webpage = "https://www.weatherbug.com/weather-camera/?cam=PSLNM"

# Get the source from the page
caps = DesiredCapabilities.CHROME
caps["goog:loggingPrefs"] = {"performance": "ALL"}
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(
    desired_capabilities=caps, options=chrome_options,
    executable_path="/usr/bin/chromedriver")
driver.get(webpage)

# Parse the source HTML for images with PSLNM in the title
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.service.stop()
img_tags = soup.find_all('img')
urls = [img['src'] for img in img_tags]
filtered_urls = [u for u in urls if "PSLNM" in u]

for url in filtered_urls:
    # Get the large version of the image instead of the thumbnail
    url = url[:-5]+"l"+url[-4:]
    data = requests.get(url).content
    img = np.array(Image.open(io.BytesIO(data)))
    time = url.split("/")[-1].split("_")[0]
    print("Downloading url")
    etai.write(img, "out/ypsilanti_"+time+".jpg")

if len(filtered_urls) == 0:
    print("No matching images found")

