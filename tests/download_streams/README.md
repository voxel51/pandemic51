# Download Streams

This script allows you to download streams from earthcam.com in real time.
It will download videos roughly 6 seconds long and save them as `.mp4` files. 

In order to get downloads for a new stream, you need to inspect element on the
videos page and go to the network tab. Look for `chunklist.m3u8` and copy the
link address to that file. 
This file contains the information of which clips to load.
The actual clips themselves are the `media_XXXX.ts` files.


