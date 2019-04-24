import requests
import base64
import json
import sys

#IMAGE_PATH = 'sample2.jpg'
IMAGE_PATH = str(sys.argv[1])
SECRET_KEY = 'sk_2487dad72fcc60a2f5d9bdf1'

with open(IMAGE_PATH, 'rb') as image_file:
    img_base64 = base64.b64encode(image_file.read())

url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=eg&secret_key=%s' % (SECRET_KEY)
r = requests.post(url, data = img_base64)
results = r.json()

plate = results['results'][0]['plate']
print(plate)

#print(json.dumps(r.json(), indent=2))