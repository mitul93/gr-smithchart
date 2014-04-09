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

import math
import numpy as np
from gnuradio import gr;

from PyQt4 import Qt, QtCore, QtGui
from PyQt4 import QtCore as Qc
import PyQt4.Qwt5 as Qwt

# data points necessary to draw circles
angleOfTransmissionR = np.array([912.0, 911.5, 911.0, 910.5, 910.0,
                                             909.0, 907.5, 905.5, 903.5, 901.5,
                                             899.0, 896.0, 892.5, 889.5, 885.5,
                                             882.5, 878.0, 874.0, 869.0, 863.5,
                                             858.5, 853.5, 848.0, 842.0, 835.5,
                                             829.5, 823.0, 816.0, 809.0, 802.0,
                                             794.0, 786.5, 779.0, 770.5, 762.0,
                                             754.0, 745.0, 735.5, 726.0, 716.5,
                                             707.5, 697.0, 687.0, 677.5, 666.5,
                                             655.0, 645.5, 634.0, 623.0, 612.0,
                                             600.0, 589.0, 578.0, 566.0, 554.0,
                                             542.0, 529.5, 517.0, 504.5, 492.0,
                                             479.0, 466.0, 454.0, 440.5, 427.5,
                                             414.5, 402.0, 389.0, 375.0, 362.0,
                                             349.0, 335.0, 322.0, 310.0, 297.0,
                                             284.0, 271.0, 258.0, 245.0, 232.0,
                                             223.0, 210.0, 197.0, 188.0, 177.0,
                                             166.0, 155.0, 146.5, 137.0, 130.0,
                                             122.0])	
PI = 3.141592654
dataVector = Qc.QPointF()
arcscal = 0
showInterpolatedLine = 0
textPen = QtGui.QPen(Qc.Qt.black,0.75)
thickPen = QtGui.QPen(Qc.Qt.black,0.25)
thinPen = QtGui.QPen(Qc.Qt.gray,0.25)
pointDataPen = QtGui.QPen(Qc.Qt.red,4.0,Qc.Qt.SolidLine,Qc.Qt.RoundCap)
lineDataPen = QtGui.QPen(Qc.Qt.black,0.25)
thinArcsPath = QtGui.QPainterPath()
thickArcsPath = QtGui.QPainterPath()

qp = QtGui.QPainter()

class smithsink(gr.sync_block,QtGui.QWidget):
    
    def __init__(self,blkname="smithchart"):
        gr.sync_block.__init__(self,blkname,[],[])
        Qwt.QwtPlot.__init__(self)

        self.initUI()
    
    def initUI(self):
		self.setGeometry(0,0,500,500)
		self.setWindowTitle('Smith Chart')		
		self.show()
	
    def paintEvent(self, e):
		
		qp.begin(self)
		self.drawCircles()
		qp.end()

    def drawCircles(self):
		
		min_size = min(self.width(),self.height())
		# Circular region for clipping
		r1 = QtGui.QRegion(Qc.QRect((self.width() - min_size)/2, (self.height() - min_size)/2, min_size,min_size), 		
			QtGui.QRegion.Ellipse)
	        qp.setClipRegion(r1)
		
		# calculate radius of Re(z) circles from data point
		for x in range (21):
			circle_radii_x[x] = min_size*datapoints_x[x]
			
		# # calculate radius of Re(z) circles from data point
		for x in range (20):			
			circle_radii_y[x] = min_size*datapoints_y[x]
		
		pen = QtGui.QPen(Qc.Qt.black, 5, Qc.Qt.SolidLine)
	        qp.setPen(pen)
		
		p = Qc.QPoint(self.width()/2 + min_size/2 - circle_radii_x[0]/2, self.height()/2)
		qp.drawEllipse(p,circle_radii_x[0]/2, circle_radii_x[0]/2)
		
		pen = QtGui.QPen(Qc.Qt.darkGray, 1, Qc.Qt.SolidLine)
       		qp.setPen(pen)
		
		# draw Re(z) circles
		for x in range (1,21):
			p = Qc.QPoint(self.width()/2 + min_size/2 - circle_radii_x[x]/2, self.height()/2)
			qp.drawEllipse(p,circle_radii_x[x]/2, circle_radii_x[x]/2)
		
		# draw Im(z) circles
		for x in range (20):
			p = Qc.QPoint(self.width()/2 + min_size/2, self.height()/2 - circle_radii_y[x]/2)
			qp.drawEllipse(p,circle_radii_y[x]/2,circle_radii_y[x]/2)
			p = Qc.QPoint(self.width()/2 + min_size/2, self.height()/2 + circle_radii_y[x]/2)
			qp.drawEllipse(p,circle_radii_y[x]/2,circle_radii_y[x]/2)
		
		# draw line passing through Y - axis (circle having INFINITE radius)
		qp.drawLine((self.width()-min_size)/2,min_size/2,(self.width()+min_size)/2,min_size/2)
				
    def work(self, input_items, output_items):
	        pass


