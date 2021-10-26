# Basic use of open API Kartverket wms.hoyde-dom for getting elevation data in a specific area (Norway only).
#
# 1. Go to https://kartkatalog.geonorge.no
# 2. Find and add WMS service "Digital overflatemodell WMS".
# 3. Press "Vis kart", or go to for example this URL to view an area and enable the surface model in left menu:
#    https://kartkatalog.geonorge.no/kart?lat=6882011.719407242&lon=68429.52888256384&zoom=8.589318931685455
#
#
# Note:
# Example code for UiA MAS417 project. Easy-to-follow demonstration on how to use a WMS API to fetch an image and
# display it. In addition to converting the image to a numpy array for analysis, manipulation, enhancement, and so on.
#
# Written by K. M. Knausgård 2021-10-26.
#
from io import BytesIO

import numpy as np
import requests
from PIL import Image



# This is directly the API call used by Geonorge here:
# https://kartkatalog.geonorge.no/kart?lat=6882011.719407242&lon=68429.52888256384&zoom=8.589318931685455
# .. when adding the "Digital overflatemodell WMS layer".
# For use in an application, please see requests user manual: https://docs.python-requests.org/en/latest/
# See the following examples on how to handle http request parameters / payload and so on:
# https://docs.python-requests.org/en/latest/user/quickstart/#passing-parameters-in-urls
request_url = 'https://wms.geonorge.no/skwms1/wms.hoyde-dom?' \
           'SERVICE=WMS&' \
           'VERSION=1.3.0&' \
           'REQUEST=GetMap&' \
           'FORMAT=image/png&' \
           'TRANSPARENT=false&' \
           'LAYERS=DOM:None&' \
           'CRS=EPSG:25833&' \
           'STYLES=&' \
           'WIDTH=1751&' \
           'HEIGHT=1241&' \
           'BBOX=18676.05018252586,6845773.541229122,117163.78576648101,6915575.52858474'


response = requests.get(request_url, verify=True)  # SSL Cert verification explicitly enabled. (This is also default.)
print(f"HTTP response status code = {response.status_code}")

img = Image.open(BytesIO(response.content))
np_img = np.asarray(img)
# Could do something with numpy here.
img = Image.fromarray(np.uint8(np_img))
img.show()

# Could convert to STL here.


