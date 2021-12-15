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

from stl import mesh
import cv2
from matplotlib import tri


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


nordfjord ='WIDTH=1751&' \
           'HEIGHT=1241&' \
           'BBOX=18676.05018252586,6845773.541229122,117163.78576648101,6915575.52858474'

indre_nordfjord = 'WIDTH=1562&' \
                  'HEIGHT=971&' \
                  'BBOX=47218.82866421278,6870181.07028388,91147.39604917506,6897488.777665954'

response = requests.get(request_url + indre_nordfjord, verify=True)  # SSL Cert verification explicitly enabled. (This is also default.)
print(f"HTTP response status code = {response.status_code}")

img = Image.open(BytesIO(response.content))
np_img = np.asarray(img)
# Could do something with numpy here.
img = Image.fromarray(np.uint8(np_img))
img.show()


# Convert to STL:
segmented_img = cv2.cvtColor(np_img, cv2.COLOR_BGR2GRAY)
scale = 2
newshape = (int(segmented_img.shape[1] * scale), int(segmented_img.shape[0] * scale))
print(f"New shape: {newshape}")
segmented_img = cv2.resize(segmented_img, newshape, interpolation=cv2.INTER_AREA)
downsample = 1
digital_surface_model = segmented_img[::downsample, ::downsample]
th, tw = digital_surface_model.shape

bg_image = np.full((th+220, tw+36), 0, dtype=np.uint8)
bh, bw = bg_image.shape

y_offset = round((bh-th) / 2)
x_offset = round((bw-tw) / 2)

bg_image[y_offset:y_offset+th, x_offset:x_offset+tw] = digital_surface_model
digital_surface_model = bg_image

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 2.2
height = 10 # Intensity is height
thickness = 4
place = 'Nordfjord'
(text_width, text_height) = cv2.getTextSize(place, font, font_scale, thickness)[0]

origin = (round(0.5 * bw - 0.5*text_width), round(bh - (0.5*(bw-tw)) - 0.35*text_height))
digital_surface_model = cv2.putText(digital_surface_model, place, origin, font,
                    font_scale, height, thickness, cv2.LINE_AA)

diameter = 30
center = (round(0.5 * bw), round(0.28 * (bh-th)))
radius = int(0.5*diameter)
height = 200
thickness = -1 # Filled


scalefactor = 2.4

digital_surface_model = digital_surface_model / max(digital_surface_model.flatten())
digital_surface_model = digital_surface_model * 10
digital_surface_model = cv2.circle(digital_surface_model, center, radius, height, thickness) # hole


digital_surface_model = np.flip(digital_surface_model, 1)


digital_surface_model[:, (0, -1)] = 200
digital_surface_model[(0, -1), :] = 200

z = digital_surface_model.flatten();
base_height = 3
z = z + base_height
z[z == (200+base_height)] = 0
print(digital_surface_model.shape)
nx = digital_surface_model.shape[0]
ny = digital_surface_model.shape[1]

xv, yv = np.meshgrid(np.arange(ny) * 50.0 * scalefactor / nx, np.arange(nx) * 50.0 * scalefactor / nx)
x = xv.ravel()
y = yv.ravel()
print(x.shape)
print(y.shape)
print(z.shape)

if 0:
    x = x[z != 0]
    y = y[z != 0]
    z = z[z != 0]

faces = tri.Triangulation(x, y).get_masked_triangles()

print(f"Sizes {x.shape} {y.shape} {z.shape}")
vertices = np.array([x.T, y.T, z.T]).T
print(f"Size {vertices.shape}")

selected = np.any(vertices[faces.ravel(), 2].reshape(faces.shape), axis=1)
print(f"Selected {selected.shape}")
fview = faces[selected, :]

print(f"View {faces.shape} {fview.shape}")
faces = fview


if (False):
    # Creating figure
    fig = plt.figure(figsize=(16, 9))
    ax = plt.axes(projection='3d')

    # Creating color map
    jet_cmap = plt.get_cmap(plt.cm.jet)

    # Creating plot
    trisurf = ax.plot_trisurf(x, y, z,
                              cmap=jet_cmap,
                              linewidth=0.25,
                              antialiased=True,
                              edgecolor='grey')
    fig.colorbar(trisurf, ax=ax, shrink=0.5, aspect=5)
    ax.set_title('Tri-Surface plot')

    # Adding labels
    ax.set_xlabel('X [-]', fontweight='bold')
    ax.set_ylabel('Y [-]', fontweight='bold')
    ax.set_zlabel('Z [mm]', fontweight='bold')
    ax.set_zlim3d(0, 10)

    # show plot
    plt.show()


# Create the mesh
cube = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
for i, f in enumerate(faces):
    for j in range(3):
        cube.vectors[i][j] = vertices[f[j], :]

# Write the mesh to file "cube.stl"
cube.save('terrain.stl')
