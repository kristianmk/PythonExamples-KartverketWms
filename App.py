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
    print('Please input desired latitude within Norway, "north-south direction" http://bboxfinder.com/#0.000000,0.000000,0.000000,0.000000')
    # latitude ->   North-south ("vertical direction"),   latitude are the "horizontal lines" of the globe,
    # -90 south pole, 0 equator, 90 north pole.
    # 04.11Fredrik changed lat vs long implementation. and the adjusted the bounds
    # changes are made in multiple lines to changes the lat vs long implementation, the lat was implemented as long. and visa verca
def import_lat():

    lat = float(input())
    if lat > 57.00 and lat < 71.00:
            lat = lat
    else:
        print('Latitude out of bounds. Value needs to be between 57 and 71')
        import_lat()

    return lat

def import_lon():
    print('Please input desired longitude within Norway')
    lon = float(input())
    if lon > 2.0 and lon < 32.88:

        lon = lon
    else:
        print('Longitude out of bounds. Value needs to be between 2 and 32.8')
        import_lon()

    return lon
lat = import_lat()
lon = import_lon()
sq = 2                    # value for printing "Gaustatoppen"          #This controls size of printout area, sq is side of square in kilometers
corner_const = 90*sq/22000

lat = 59.853952  # value for printing "Gaustatoppen"        #Example input values for debugging purposes - Remove before final release
lon = 8.648471    # value for printing "Gaustatoppen"        #Example input values for debugging purposes - Remove before final release

BBY = [lon - corner_const * 2, lon + corner_const * 2]
BBX = [lat - corner_const, lat + corner_const]

#BBOX=min_lat,min_long,max_lat,max_long:
#transformer = Transformer.from_crs('WGS84', 'EPSG:25833')
#BBOX_X, BBOX_Y = transformer.transform(BBX, BBY)


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
