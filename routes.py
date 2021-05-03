# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 09:23:44 2021

@author: omedeiro

https://towardsdatascience.com/easy-steps-to-plot-geographic-data-on-a-map-python-11217859a2db

"""

import gpxpy
import gpxpy.gpx
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable


import os
import os

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
    

ruh_m = plt.imread('map_final.png')

fig, ax = plt.subplots(figsize = (32.819/2,23.347/2))

''' This code is used to plot elevation along x and y axes
# divider = make_axes_locatable(ax)
# ax_elx = divider.append_axes("top", 1.2, pad=0.1, sharex=ax)
# ax_ely = divider.append_axes("right", 1.2, pad=0.1, sharey=ax)
# ax_elx.xaxis.set_tick_params(labelbottom=False)
# ax_ely.yaxis.set_tick_params(labelleft=False)
'''

# bbox = (-71.13098, -70.99504, 42.32365,42.38442)
bbox = (-71.1387, -71.0079, 42.3196, 42.3883) #from photo

ax.set_xlim(bbox[0], bbox[1])
ax.set_ylim(bbox[2],bbox[3])
ax.imshow(ruh_m, zorder=0, extent = bbox, aspect= 'equal', alpha=0.5)

path = r'G:\My Drive\personal\health\data\20210428\apple_health_export\workout-routes'
for file in os.listdir(path):
    if file.endswith(".gpx"):
        print(os.path.join(path, file))
                
        gpx_file = open(os.path.join(path, file), 'r')
        
        gpx = gpxpy.parse(gpx_file)
        
        coords = np.array([0,0,0])
        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    # print('Point at ({0},{1}) -> {2}'.format(point.longitude, point.latitude, point.elevation))
                    line = np.array([point.longitude, point.latitude, point.elevation])
                    coords = np.vstack([coords, line])
        
        coords = np.delete(coords, 0, 0)
        ax.plot(coords[:,0], coords[:,1], 'b-', zorder=1, alpha = 0.3)
        
        '''
        ax_elx.plot(coords[:,0], coords[:,2], 'bo')
        ax_ely.plot(coords[:,2], coords[:,1], 'bo')
        '''
        
        
