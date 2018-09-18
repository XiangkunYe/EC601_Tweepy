import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont

#os.popen('export GOOGLE_APPLICATION_CREDENTIALS="/Users/yxk/Documents/Python/601/GoogleVisionKey.json"')

def analypic():

    picname = list(os.popen('ls'))

    for pic in picname:

        if '.jpg' in pic:

            pict = pic.strip()
            # Instantiates a client
            client = vision.ImageAnnotatorClient()

            # The name of the image file to annotate
            file_name = os.path.join(
                os.path.dirname(__file__),
                pict)

            # Loads the image into memory
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)

            # Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations

            im = Image.open(file_name)
            draw = ImageDraw.Draw(im)
            labeldes = []

            for label in labels:
                labeldes.append(label.description+'\n')

            labeldcp = ''.join(labeldes)
            myfont = ImageFont.truetype("Chalkduster.ttf", 35)
            fillcolor = 'red'

            draw.text((50, 40), labeldcp, font=myfont, fill=fillcolor)
            im.save(file_name, 'JPEG')
