import os

os.popen('ffmpeg -framerate 24 -r 1 -i jpg%04d.jpg -t 600 -vf scale=1280:720 output.mp4')
