from bs4 import BeautifulSoup
from datetime import datetime
from PIL import Image
from selenium import webdriver

import io
import time
import glob
import os
import requests
import numpy as np

import eta.core.image as etai

def get_gt_imgs():
    '''Load set of hand picked images that are used to filter out
    images that are dissimilar for the camera view we are 
    interested in
    '''

    gt_path = "/home/eric/work/pandemic51/core_images/timessquare/core_images/" 
    imgs = [etai.read(img) for img in glob.glob(gt_path+"*")]
    shapes = np.array([i.shape for i in imgs])
    min_shape = shapes.min(axis=0)
    imgs = np.array([img[:min_shape[0], :min_shape[1], :min_shape[2]] for img in imgs]).astype(float)
    return imgs

gt_imgs = get_gt_imgs()

output_dir = "out/" #Relative to script location
site = 'https://www.earthcam.com/usa/newyork/timessquare/?cam=tsrobo1'

driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')

driver.get(site)

# Need about 10 iterations per day
# Ex iters = 100 to go back 10 days
iters = 200
for scrolls in range(iters):
    driver.execute_script("window.scrollBy(0, 10000)")
    time.sleep(0.01)
    driver.execute_script("window.scrollBy(0, 10000)")
    time.sleep(0.01)
    driver.execute_script("window.scrollBy(0, 10000)")
    time.sleep(0.2)
    try:
        driver.find_element_by_css_selector(".fauxLink").click()
    except:
        time.sleep(0.2)
        pass
    time.sleep(0.05)


soup = BeautifulSoup(driver.page_source, 'html.parser')
img_tags = soup.find_all('img')

urls = [img['src'] for img in img_tags]
filtered_urls = [u for u in urls if ('_thumb' in u and "timessquare" in u)]

driver.service.stop()
timezone_change = -4
one_hour = 1000 * 60 * 60

for url in filtered_urls:
    dir_name, filename = os.path.split(url)
    utc_time, img_num, _ = filename.split('_')
    utc_time = int(utc_time)
    utc_time += timezone_change * one_hour
    formatted_time = datetime.utcfromtimestamp(utc_time/1000.).strftime('%Y-%m-%d %H:%M:%S')
    hr = datetime.utcfromtimestamp(utc_time/1000.).hour
    day_int = datetime.utcfromtimestamp(utc_time/1000.).day
    day, hms = formatted_time.split(' ')

    if day_int in [23,22,21,20]:
        continue
    try:
        if len(os.listdir(os.path.join(output_dir, str(day), str(hr)))) >= 1:
            continue
    except:
        pass


    full_url = os.path.join(dir_name, '_'.join(filename.split('_')[:2])+".jpg")
    data = requests.get(full_url).content
    try:
        img = np.array(Image.open(io.BytesIO(data)))
        min_shape = np.array([gt_imgs[0].shape, img.shape]).min(axis=0)
        curr_gt_imgs = gt_imgs[:, :min_shape[0], :min_shape[1], :min_shape[2]]
        query = img[:min_shape[0], :min_shape[1], :min_shape[2]].astype(float)
        diff = np.abs(query - curr_gt_imgs).mean(axis=(1,2,3))
        if diff.min() < 40:
            etai.write(query, os.path.join(output_dir, day, str(hr), str(utc_time)+'_'+img_num+'_'+hms+".jpg"))
            etai.write(query, os.path.join(output_dir, day, "all", str(utc_time)+'_'+img_num+'_'+hms+".jpg"))
    except: 
        print("Error")
    print(url, full_url, formatted_time)
import pdb; pdb.set_trace()
