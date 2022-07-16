#! /var/www/greenwall/python/env/bin/python

import cv2
import os
from natsort import natsorted
start = "5-2022-06-18T17:20"
end = "5-2022-06-18T17:50"
out=cv2.VideoWriter("/var/www/greenwall/cam-video/video.ogg", cv2.VideoWriter.fourcc(*'theo'), 10, (1024,768))
try:
    print("!!! Start to collect files")
    for filename in natsorted(os.listdir('/var/www/greenwall/cam-frame')):
        ext = os.path.splitext(filename)[-1].lower()
        if ext=='.jpg' and start <= filename <= end:
            print(filename)
            img=cv2.imread('/var/www/greenwall/cam-frame/' + filename)
            out.write(img)

finally:
    out.release()


