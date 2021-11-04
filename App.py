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

#from pyproj import Transformer

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

# lat = import_lat()
# lon = import_lon()

sq = 33                                   #This controls size of printout area, sq is side of square in kilometers
corner_const = 90*sq/22000


def get_image(lat, lon):

    BBX = [lon - corner_const * 2, lon + corner_const * 2]
    BBY = [lat - corner_const, lat + corner_const]

    # transformer = Transformer.from_crs('WGS84', 'EPSG:25833')
    # BBOX_X, BBOX_Y = transformer.transform(BBX, BBY)

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
    response = requests.get(request_url,
                            verify=True)  # SSL Cert verification explicitly enabled. (This is also default.)
    print(f"HTTP response status code = {response.status_code}")

    img = Image.open(BytesIO(response.content))
    np_img = np.asarray(img)
    # Could do something with numpy here.
    img = Image.fromarray(np.uint8(np_img))
    img.show()
    return  img

# Crete the image class based x = lat , y = lon, get_image funtion that gets image based on x and y
class MyImage:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.img = get_image(x,y)


first_image = MyImage(import_lat(), import_lon())




import numpy as np
import numpy as np
from stl import mesh
# Define the 4 vertices of the surface

from PIL import Image
import matplotlib.pyplot as plt
img = first_image.img
grey_img = img.convert('L')
grey_img.show()
print(grey_img.size)

max_size=(500,500)
max_height=10
min_height=0
#height=0 for minpix
#height=maxheight for maxpix

#resize
grey_img.thumbnail(max_size)
imageNP= np.array(grey_img)
maxPix = imageNP.max()
minPix = imageNP.min()


print(imageNP)
(ncols,nrows)=grey_img.size

verticies=np.zeros((nrows,ncols,3))

for x in range(0,ncols):
    for y in range(0,nrows):
        pixelIntensity= imageNP[y][x]
        z = (pixelIntensity * max_height) / maxPix
        #coordinates
        verticies[y][x]=(x,y,z)
faces=[]

for x in range(0, ncols-1):
  for y in range(0, nrows-1):

       #create face1
    vertice1=verticies[y][x]
    vertice2=verticies[y+1][x]
    vertice3=verticies[y+1][x+1]
    face1=np.array([vertice1,vertice2,vertice3])
       #create face 2
    vertice1 = verticies[y][x]
    vertice2 = verticies[y][x+1]
    vertice3 = verticies[y+1][x+1]

    face2 = np.array([vertice1, vertice2, vertice3])

    faces.append(face1)
    faces.append(face2)
print(f"numberof faces:{len(faces)}")

facesNP= np.array(faces)
# Create the mesh
surface = mesh.Mesh(np.zeros(facesNP.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        surface.vectors[i][j] = facesNP[i][j]
# Write the mesh to file "cube.stl"
surface.save('surface.stl')
print(surface)









# lat = 16.8                                #Example input values for debugging purposes - Remove before final release
# lon = 68.55                               #Example input values for debugging purposes - Remove before final release





