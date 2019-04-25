import requests
import base64
import json
import sys
import os

from extract_plate import extract_plate

INIT_IMAGE_PATH = str(sys.argv[1])
#crop plate by mo'men function
IMAGE_PATH = extract_plate(INIT_IMAGE_PATH,"template_num.JPG")
SECRET_KEY = 'sk_2487dad72fcc60a2f5d9bdf1'

with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=e                                                                                                             g&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data = img_base64)
results = r.json()

plate = results['results'][0]['plate']
#deleting image to save space
os.remove(IMAGE_PATH)

print(plate)

#print(json.dumps(r.json(), indent=2))
