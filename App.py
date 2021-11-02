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
# Originally written by K. M. Knausgård 2021-10-26.
# Forked on 2021.10.29
#
from io import BytesIO
import numpy as np
import requests
from PIL import Image

from pyproj import Transformer

def import_lat():
    print('Please input desired latitude within Norway')
    lat = float(input())

    if lat > -16.1 and lat < 32.88:
        lat = lat
    else:
        print('Latitude out of bounds. Value needs to be between -16.1 and 32.88')
        import_lat()

    return lat


def import_lon():
    print('Please input desired longitude within Norway')
    lon = float(input())

    if lon > 40.18 and lon < 84.17:
        lon = lon
    else:
        print('Longitude out of bounds. Value needs to be between 40.18 and 84.17')
        import_lon()

    return lon


lat = import_lat()
lon = import_lon()

sq = 32                                    #This controls size of printout area, sq is side of square in kilometers
corner_const = 90*sq/22000

#lat = 16.8                                #Example input values for debugging purposes - Remove before final release
#lon = 68.55                               #Example input values for debugging purposes - Remove before final release

BBX = [lon - corner_const * 2, lon + corner_const * 2]
BBY = [lat - corner_const, lat + corner_const]

#transformer = Transformer.from_crs('WGS84', 'EPSG:25833')
#BBOX_X, BBOX_Y = transformer.transform(BBX, BBY)

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
           'CRS=EPSG:4326&' \
           'STYLES=&' \
           'WIDTH=1080&' \
           'HEIGHT=1080&' \
           f'BBOX={BBX[0]},{BBY[0]},{BBX[1]},{BBY[1]},'


response = requests.get(request_url, verify=True)  # SSL Cert verification explicitly enabled. (This is also default.)
print(f"HTTP response status code = {response.status_code}")

img = Image.open(BytesIO(response.content))
np_img = np.asarray(img)
# Could do something with numpy here.
img = Image.fromarray(np.uint8(np_img))
img.show()

# Could convert to STL here.


