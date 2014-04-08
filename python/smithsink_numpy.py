#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 Mitul Vekariya <vekariya93@gmail.com>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import numpy as np
from gnuradio import gr;
import matplotlib.pyplot as plt

# data points to plot circles
data = np.array([0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,1.0,1.2,1.4,1.6,1.8,2.0,3.0,4.0,5.0,10,20,50])
center_x = np.zeros(20)	
center_y = np.zeros(20)
circle_radii_x = np.zeros(20) 
circle_radii_y = np.zeros(20) 

fig = plt.figure()
ax = plt.subplot(111, polar=True)
ax.set_rmax(1)

class smithsink_numpy(gr.sync_block):
    
    def __init__(self,blkname="smithchart numpy"):
        gr.sync_block.__init__(self,blkname,[],[])    
	fig.canvas.mpl_connect('close_event', self.handle_close)   
	self.draw_graph()
    
    def handle_close(evt):
	print "closing..."
	fig.close()

    def draw_graph(self):
	for x in range (20):
		center_x[x] = 1/(data[x]+1)
		circle_radii_x[x] = center_x[x]

	# draw circle (x,0)
	for x in range (20):
		circle = plt.Circle((1 - center_x[x],0),circle_radii_x[x], transform=ax.transData._b, fill=False)
		ax.add_artist(circle)

	# calculate radius from data points using formula r = 1/im(z)
	for x in range (20):
		center_y[x] = 1/data[x]
		circle_radii_y[x] = center_y[x]
	

	# draw circle (1,y)
	for x in range (20):
		circle = plt.Circle((1,center_y[x]),circle_radii_y[x], transform=ax.transData._b, fill=False)
		ax.add_artist(circle)	
		circle = plt.Circle((1,-center_y[x]),circle_radii_y[x], transform=ax.transData._b, fill=False)
		ax.add_artist(circle)		

	ax.grid(False)
	ax.axes.get_xaxis().set_visible(False)
	ax.axes.get_yaxis().set_visible(False)

	plt.show()
				
    def work(self, input_items, output_items):
	        pass


