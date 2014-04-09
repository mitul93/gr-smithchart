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
	self.setGeometry(0,0,self.width(),self.height())
	self.setWindowTitle('Smith Chart')		
	self.show()
	
    def paintEvent(self, e):
		
	qp.begin(self)
	qp.setRenderHint(QtGui.QPainter.Antialiasing)
	qp.setBackground(QtGui.QBrush(QtGui.QColor(255, 255, 255)))
	qp.fillRect(0, 0, self.width(), self.height(), QtGui.QBrush(QtGui.QColor(255, 255, 255)))
	side = min(self.width(), self.height())
	qp.setViewport((self.width()-side)/2, (self.height()-side)/2, side, side)
	qp.setWindow(-512, -512, 1024, 1024)

	if (arcscal == 0):
		self.calculateInsideArcs()
		arcsCalculated = 1

	self.drawCircles()
	qp.end()

    def drawConstantZArc(self, pen, z, angle, span):

	topLeftX = 0

	topLeftX = ((z*z)-1.0)/((z+1.0)*(z+1.0))
	topLeftX = topLeftX*224.0

	rectangle = Qc.QRectF(2.0*topLeftX,-224.0+topLeftX,
	                          448.0-2.0*topLeftX,448.0-2.0*topLeftX)

	rectangle = rectangle.normalized()

	if(pen == thinPen):
	
		thinArcsPath.arcMoveTo(rectangle, angle)
		thinArcsPath.arcTo(rectangle, angle, span)
	
	else:
	
		thickArcsPath.arcMoveTo(rectangle, angle)
		thickArcsPath.arcTo(rectangle, angle, span)
	

	if(pen == thinPen):
	
		thinArcsPath.arcMoveTo(rectangle, -angle)
		thinArcsPath.arcTo(rectangle, -angle, -span)
	
	else:
	
		thickArcsPath.arcMoveTo(rectangle, -angle)
		thickArcsPath.arcTo(rectangle, -angle, -span)
	
    def drawConstantRoArc(self, pen, ro, startAngle, span):
	
	topLeftX = (1.0-(1.0/ro))*448.0
	topLeftY = 896.0*(1.0/ro)
	rectangle = Qc.QRectF(topLeftX,-topLeftY,topLeftY, topLeftY)
	rectangle = rectangle.normalized()
	
	if(pen == thinPen):
	
		thinArcsPath.arcMoveTo(rectangle, startAngle)
		thinArcsPath.arcTo(rectangle, startAngle, span)
	
	else:
	
		thickArcsPath.arcMoveTo(rectangle, startAngle)
		thickArcsPath.arcTo(rectangle, startAngle, span)
	
	rectangle.setRect(topLeftX, 0.0, topLeftY, topLeftY)
	rectangle = rectangle.normalized()

	if(pen == thinPen):
	
		thinArcsPath.arcMoveTo(rectangle, -startAngle)
		thinArcsPath.arcTo(rectangle, -startAngle, -span)

	else:
		thickArcsPath.arcMoveTo(rectangle, -startAngle)
		thickArcsPath.arcTo(rectangle, -startAngle, -span)

    def calculateInsideArcs(self):
	
	# Z = 0.01
	self.drawConstantZArc(thinPen, 0.01, 157.5, 22.5)
	# Z = 0.02
	self.drawConstantZArc(thinPen, 0.02, 128.0, 52.0)
	# Z = 0.03
	self.drawConstantZArc(thinPen, 0.03, 158.0, 22.0)
	# Z = 0.04
	self.drawConstantZArc(thinPen, 0.04, 128.5, 51.5)
	# Z = 0.05
	self.drawConstantZArc(thickPen, 0.05, 158.5, 21.5)
	self.drawConstantZArc(thinPen, 0.05, 93.0, 36.0)
	# Z = 0.06
	self.drawConstantZArc(thinPen, 0.06, 129.5, 50.5)
	# Z = 0.07
	self.drawConstantZArc(thinPen, 0.07, 159.0, 21.0)
	# Z = 0.08
	self.drawConstantZArc(thinPen, 0.08, 130.5, 49.5)
	# Z = 0.09
	self.drawConstantZArc(thinPen, 0.09, 159.5, 20.5)
	# Z = 0.1
	self.drawConstantZArc(thickPen, 0.1, 95.5, 84.5)
	self.drawConstantZArc(thinPen, 0.1, 57.5, 38.0)

	# Z = 0.11
	self.drawConstantZArc(thinPen, 0.11, 159.5, 20.5)
	# Z = 0.12
	self.drawConstantZArc(thinPen, 0.12, 132.0, 48.0)
	# Z = 0.13
	self.drawConstantZArc(thinPen, 0.13, 160.0, 20.0)
	# Z = 0.14
	self.drawConstantZArc(thinPen, 0.14, 132.5, 47.5)
	# Z = 0.15
	self.drawConstantZArc(thickPen, 0.15, 160.25, 19.75)
	self.drawConstantZArc(thinPen, 0.15, 98.0, 35.0)
	# Z = 0.16
	self.drawConstantZArc(thinPen, 0.16, 133.5, 46.5)
	# Z = 0.17
	self.drawConstantZArc(thinPen, 0.17, 160.5, 19.5)
	# Z = 0.18
	self.drawConstantZArc(thinPen, 0.18, 134.0, 46.0)
	# Z = 0.19
	self.drawConstantZArc(thinPen, 0.19, 161.0, 19.0)
	# Z = 0.2
	self.drawConstantZArc(thickPen, 0.2, 62.0, 118.0)
	self.drawConstantZArc(thinPen, 0.2, 27.0, 35.0)

	# Z = 0.22
	self.drawConstantZArc(thinPen, 0.22, 135.5, 44.5)
	# Z = 0.24
	self.drawConstantZArc(thinPen, 0.24, 136.0, 44.0)
	# Z = 0.25
	self.drawConstantZArc(thinPen, 0.25, 103.0, 33.5)
	# Z = 0.26
	self.drawConstantZArc(thinPen, 0.26, 136.75, 43.25)
	# Z = 0.28
	self.drawConstantZArc(thinPen, 0.28, 137.5, 42.5)
	# Z = 0.3
	self.drawConstantZArc(thickPen, 0.3, 105.0, 75.0)
	self.drawConstantZArc(thinPen, 0.3, 66.0, 39.0)
	# Z = 0.32
	self.drawConstantZArc(thinPen, 0.32, 138.75, 41.25)
	# Z = 0.34
	self.drawConstantZArc(thinPen, 0.34, 139.25, 40.75)
	# Z = 0.35
	self.drawConstantZArc(thinPen, 0.35, 107.0, 32.5)
	# Z = 0.36
	self.drawConstantZArc(thinPen, 0.36, 140.0, 40.0)
	# Z = 0.38
	self.drawConstantZArc(thinPen, 0.38, 140.5, 39.5)
	# Z = 0.4
	self.drawConstantZArc(thickPen, 0.4, 70.0, 110.0)
	self.drawConstantZArc(thinPen, 0.4, 31.0, 39.0)
	# Z = 0.42
	self.drawConstantZArc(thinPen, 0.42, 141.5, 38.5)
	# Z = 0.44
	self.drawConstantZArc(thinPen, 0.44, 142.0, 38.0)
	# Z = 0.45
	self.drawConstantZArc(thinPen, 0.45, 111.0, 31.5)
	# Z = 0.46
	self.drawConstantZArc(thinPen, 0.46, 142.5, 37.5)
	# Z = 0.48
	self.drawConstantZArc(thinPen, 0.48, 143.0, 37.0)
	# Z = 0.5
	self.drawConstantZArc(thickPen, 0.5, 113.0, 67.0)
	self.drawConstantZArc(thinPen, 0.5, 74.0, 39.0)

	# Z = 0.55
	self.drawConstantZArc(thinPen, 0.55, 115.0, 65.0)
	# Z = 0.6
	self.drawConstantZArc(thickPen, 0.6, 77.5, 102.5)
	self.drawConstantZArc(thinPen, 0.6, 35.5, 42.0)
	# Z = 0.65
	self.drawConstantZArc(thinPen, 0.65, 118.0, 62.0)
	# Z = 0.7
	self.drawConstantZArc(thickPen, 0.7, 119.5, 60.5)
	self.drawConstantZArc(thinPen, 0.7, 81.0, 38.5)
	# Z = 0.75
	self.drawConstantZArc(thinPen, 0.75, 121.0, 59.0)
	# Z = 0.8
	self.drawConstantZArc(thickPen, 0.8, 84.0, 96.0)
	self.drawConstantZArc(thinPen, 0.8, 39.5, 44.5)
	# Z = 0.85
	self.drawConstantZArc(thinPen, 0.85, 123.5, 56.5)
	# Z = 0.9
	self.drawConstantZArc(thickPen, 0.9, 125.0, 55.0)
	self.drawConstantZArc(thinPen, 0.9, 87.0, 38.0)
	# Z = 0.95
	self.drawConstantZArc(thinPen, 0.95, 126.0, 54.0)
	# Z = 1
	self.drawConstantZArc(thickPen, 1.0, 44.0, 136.0)
	self.drawConstantZArc(thinPen, 1.0, 22.5, 22.0)

	# Z = 1.1
	self.drawConstantZArc(thinPen, 1.1, 93.0, 87.0)
	# Z = 1.2
	self.drawConstantZArc(thickPen, 1.2, 95.5, 84.5)
	self.drawConstantZArc(thinPen, 1.2, 47.5, 50.0)
	# Z = 1.3
	self.drawConstantZArc(thinPen, 1.3, 98.0, 82.0)
	# Z = 1.4
	self.drawConstantZArc(thickPen, 1.4, 100.0, 80.0)
	self.drawConstantZArc(thinPen, 1.4, 51.0, 50.0)
	# Z = 1.5
	self.drawConstantZArc(thinPen, 1.5, 103.0, 77.0)
	# Z = 1.6
	self.drawConstantZArc(thickPen, 1.6, 105.0, 75.0)
	self.drawConstantZArc(thinPen, 1.6, 55.0, 50.0)
	# Z = 1.7
	self.drawConstantZArc(thinPen, 1.7, 107.0, 73.0)
	# Z = 1.8
	self.drawConstantZArc(thickPen, 1.8, 109.0, 71.0)
	self.drawConstantZArc(thinPen, 1.8, 58.5, 50.0)
	# Z = 1.9
	self.drawConstantZArc(thinPen, 1.9, 110.5, 69.5)
	# Z = 2
	self.drawConstantZArc(thickPen, 2.0, 62.0, 118.0)
	self.drawConstantZArc(thinPen, 2.0, 17.0, 46.0)

	# Z = 2.2
	self.drawConstantZArc(thinPen, 2.2, 65.0, 115.0)
	# Z = 2.4
	self.drawConstantZArc(thinPen, 2.4, 68.0, 112.0)
	# Z = 2.6
	self.drawConstantZArc(thinPen, 2.6, 72.0, 108.0)
	# Z = 2.8
	self.drawConstantZArc(thinPen, 2.8, 75.0, 105.0)
	# Z = 3
	self.drawConstantZArc(thickPen, 3.0, 78.0, 102.0)
	self.drawConstantZArc(thinPen, 3.0, 44.0, 34.0)
	# Z = 3.2
	self.drawConstantZArc(thinPen, 3.2, 79.5, 100.5)
	# Z = 3.4
	self.drawConstantZArc(thinPen, 3.4, 82.0, 98.0)
	# Z = 3.6
	self.drawConstantZArc(thinPen, 3.6, 85.0, 95.0)
	# Z = 3.8
	self.drawConstantZArc(thinPen, 3.8, 88.0, 92.0)
	# Z = 4
	self.drawConstantZArc(thickPen, 4.0, 90.0, 90.0)
	self.drawConstantZArc(thinPen, 4.0, 54.0, 36.0)
	# Z = 4.2
	self.drawConstantZArc(thinPen, 4.2, 93.0, 87.0)
	# Z = 4.4
	self.drawConstantZArc(thinPen, 4.4, 96.0, 84.0)
	# Z = 4.6
	self.drawConstantZArc(thinPen, 4.6, 98.0, 82.0)
	# Z = 4.8
	self.drawConstantZArc(thinPen, 4.8, 99.0, 81.0)
	# Z = 5
	self.drawConstantZArc(thickPen, 5.0, 62.0, 118.0)

	# Z = 6
	self.drawConstantZArc(thinPen, 6.0, 70.0, 110.0)
	# Z = 7
	self.drawConstantZArc(thinPen, 7.0, 79.0, 101.0)
	# Z = 8
	self.drawConstantZArc(thinPen, 8.0, 84.0, 96.0)
	# Z = 9
	self.drawConstantZArc(thinPen, 9.0, 89.0, 91.0)
	# Z = 10
	self.drawConstantZArc(thickPen, 10.0, 20.0, 160.0)

	# Z = 12
	self.drawConstantZArc(thinPen, 12.0, 20.0, 160.0)
	# Z = 14
	self.drawConstantZArc(thinPen, 14.0, 20.0, 160.0)
	# Z = 16
	self.drawConstantZArc(thinPen, 16.0, 20.0, 160.0)
	# Z = 18
	self.drawConstantZArc(thinPen, 18.0, 20.0, 160.0)
	# Z = 20
	self.drawConstantZArc(thickPen, 20.0, 20.0, 160.0)

	# Z = 30
	self.drawConstantZArc(thinPen, 30.0, 20.0, 160.0)
	# Z = 40
	self.drawConstantZArc(thinPen, 40.0, 20.0, 160.0)
	# Z = 50
	self.drawConstantZArc(thickPen, 50.0, 0.0, 180.0)

	# Ro = 0.01
	self.drawConstantRoArc(thinPen, 0.01, 268.855, 0.19)
	# Ro = 0.02
	self.drawConstantRoArc(thinPen, 0.02, 267.71, 0.76)
	# Ro = 0.03
	self.drawConstantRoArc(thinPen, 0.03, 266.57, 0.57)
	# Ro = 0.04
	self.drawConstantRoArc(thinPen, 0.04, 265.41, 1.526)
	# Ro = 0.05
	self.drawConstantRoArc(thickPen, 0.05, 264.28, 0.95)
	self.drawConstantRoArc(thinPen, 0.05, 266.15, 0.98)

	# Ro = 0.06
	self.drawConstantRoArc(thinPen, 0.06, 263.14, 2.28)
	# Ro = 0.07
	self.drawConstantRoArc(thinPen, 0.07, 262.0, 1.3)
	# Ro = 0.08
	self.drawConstantRoArc(thinPen, 0.08, 260.85, 3.05)
	# Ro = 0.09
	self.drawConstantRoArc(thinPen, 0.09, 259.7, 1.7)
	# Ro = 0.1
	self.drawConstantRoArc(thickPen, 0.1, 258.6, 5.65)
	self.drawConstantRoArc(thinPen, 0.1, 264.25, 1.95)

	# Ro = 0.11
	self.drawConstantRoArc(thinPen, 0.11, 257.45, 2.05)
	# Ro = 0.12
	self.drawConstantRoArc(thinPen, 0.12, 256.3, 4.55)
	# Ro = 0.13
	self.drawConstantRoArc(thinPen, 0.13, 255.18, 2.4)
	# Ro = 0.14
	self.drawConstantRoArc(thinPen, 0.14, 254.05, 5.3)
	# Ro = 0.15
	self.drawConstantRoArc(thickPen, 0.15, 252.95, 2.8)
	self.drawConstantRoArc(thinPen, 0.15, 258.6, 2.8)

	# Ro = 0.16
	self.drawConstantRoArc(thinPen, 0.16, 251.8, 6.0)
	# Ro = 0.17
	self.drawConstantRoArc(thinPen, 0.17, 250.75, 3.1)
	# Ro = 0.18
	self.drawConstantRoArc(thinPen, 0.18, 249.6, 6.7)
	# Ro = 0.19
	self.drawConstantRoArc(thinPen, 0.19, 248.45, 3.5)


	# Ro = 0.2
	self.drawConstantRoArc(thickPen, 0.2, 247.4, 14.95)
	self.drawConstantRoArc(thinPen, 0.2, 262.35, 3.8)
	# Ro = 0.22
	self.drawConstantRoArc(thinPen, 0.22, 245.2, 8.1)
	# Ro = 0.24
	self.drawConstantRoArc(thinPen, 0.24, 243.0, 8.8)
	# Ro = 0.25
	self.drawConstantRoArc(thinPen, 0.25, 251.1, 4.7)
	# Ro = 0.26
	self.drawConstantRoArc(thinPen, 0.26, 240.85, 9.5)
	# Ro = 0.28
	self.drawConstantRoArc(thinPen, 0.28, 238.75, 10.15)

	# Ro = 0.3
	self.drawConstantRoArc(thickPen, 0.3, 236.6, 16.3)
	self.drawConstantRoArc(thinPen, 0.3, 252.9, 5.75)
	# Ro = 0.32
	self.drawConstantRoArc(thinPen, 0.32, 234.5, 11.4)
	# Ro = 0.34
	self.drawConstantRoArc(thinPen, 0.34, 232.5, 12.0)
	# Ro = 0.35
	self.drawConstantRoArc(thinPen, 0.35, 243.75, 6.4)
	# Ro = 0.36
	self.drawConstantRoArc(thinPen, 0.36, 230.4, 12.6)
	# Ro = 0.38
	self.drawConstantRoArc(thinPen, 0.38, 228.35, 13.2)

	# Ro = 0.4
	self.drawConstantRoArc(thickPen, 0.4, 226.4, 28.4)
	self.drawConstantRoArc(thinPen, 0.4, 254.8, 7.5)
	# Ro = 0.42
	self.drawConstantRoArc(thinPen, 0.42, 224.4, 14.4)
	# Ro = 0.44
	self.drawConstantRoArc(thinPen, 0.44, 222.5, 14.8)
	# Ro = 0.45
	self.drawConstantRoArc(thinPen, 0.45, 236.6, 8.1)
	# Ro = 0.46
	self.drawConstantRoArc(thinPen, 0.46, 220.6, 15.35)
	# Ro = 0.48
	self.drawConstantRoArc(thinPen, 0.48, 218.75, 15.75)

	# Ro = 0.5
	self.drawConstantRoArc(thickPen, 0.5, 216.9, 25.0)
	self.drawConstantRoArc(thinPen, 0.5, 241.9, 9.0)
	# Ro = 0.55
	self.drawConstantRoArc(thinPen, 0.55, 212.35, 27.0)
	# Ro = 0.6
	self.drawConstantRoArc(thickPen, 0.6, 208.1, 39.25)
	self.drawConstantRoArc(thinPen, 0.6, 247.35, 11.25)
	# Ro = 0.65
	self.drawConstantRoArc(thinPen, 0.65, 204.0, 30.0)
	# Ro = 0.7
	self.drawConstantRoArc(thickPen, 0.7, 200.0, 31.4)
	self.drawConstantRoArc(thinPen, 0.7, 231.4, 12.4)
	# Ro = 0.75
	self.drawConstantRoArc(thinPen, 0.75, 196.25, 32.75)
	# Ro = 0.8
	self.drawConstantRoArc(thickPen, 0.8, 192.75, 47.4)
	self.drawConstantRoArc(thinPen, 0.8, 240.0, 14.75)
	# Ro = 0.85
	self.drawConstantRoArc(thinPen, 0.85, 189.0, 35.0)
	# Ro = 0.9
	self.drawConstantRoArc(thickPen, 0.9, 186.0, 35.5)
	self.drawConstantRoArc(thinPen, 0.9, 221.5, 15.0)
	# Ro = 0.95
	self.drawConstantRoArc(thinPen, 0.95, 183.0, 36.0)


	# Ro = 1.0
	self.drawConstantRoArc(thickPen, 1.0, 180.0, 71.0)
	self.drawConstantRoArc(thinPen, 1.0, 251.0, 8.75)
	# Ro = 1.1
	self.drawConstantRoArc(thinPen, 1.1, 174.5, 55.25)
	# Ro = 1.2
	self.drawConstantRoArc(thickPen, 1.2, 169.5, 57.0)
	self.drawConstantRoArc(thinPen, 1.2, 226.5, 21.0)
	# Ro = 1.3
	self.drawConstantRoArc(thinPen, 1.3, 165.0, 58.0)
	# Ro = 1.4
	self.drawConstantRoArc(thickPen, 1.4, 161.0, 59.0)
	self.drawConstantRoArc(thinPen, 1.4, 220.0, 24.0)
	# Ro = 1.5
	self.drawConstantRoArc(thinPen, 1.5, 157.0, 60.0)
	# Ro = 1.6
	self.drawConstantRoArc(thickPen, 1.6, 154.0, 60.0)
	self.drawConstantRoArc(thinPen, 1.6, 214.0, 26.0)
	# Ro = 1.7
	self.drawConstantRoArc(thinPen, 1.7, 151.0, 60.0)
	# Ro = 1.8
	self.drawConstantRoArc(thickPen, 1.8, 148.0, 60.0)
	self.drawConstantRoArc(thinPen, 1.8, 208.0, 28.5)
	# Ro = 1.9
	self.drawConstantRoArc(thinPen, 1.9, 145.5, 59.5)

	# Ro = 2
	self.drawConstantRoArc(thickPen, 2.0, 143.0, 90.0)
	self.drawConstantRoArc(thinPen, 2.0, 233.0, 26.0)
	# Ro = 2.2
	self.drawConstantRoArc(thinPen, 2.2, 139.0, 91.0)
	# Ro = 2.4
	self.drawConstantRoArc(thinPen, 2.4, 135.0, 91.0)
	# Ro = 2.6
	self.drawConstantRoArc(thinPen, 2.6, 132.0, 91.0)
	# Ro = 2.8
	self.drawConstantRoArc(thinPen, 2.8, 129.0, 91.0)

	# Ro = 3
	self.drawConstantRoArc(thickPen, 3.0, 127.0, 90.0)
	self.drawConstantRoArc(thinPen, 3.0, 217.0, 23.0)
	# Ro = 3.2
	self.drawConstantRoArc(thinPen, 3.2, 125.0, 89.0)
	# Ro = 3.4
	self.drawConstantRoArc(thinPen, 3.4, 122.5, 88.0)
	# Ro = 3.6
	self.drawConstantRoArc(thinPen, 3.6, 120.5, 88.0)
	# Ro = 3.8
	self.drawConstantRoArc(thinPen, 3.8, 119.0, 87.0)

	# Ro = 4
	self.drawConstantRoArc(thickPen, 4.0, 118.0, 85.0)
	self.drawConstantRoArc(thinPen, 4.0, 203.0, 46.0)
	# Ro = 4.2
	self.drawConstantRoArc(thinPen, 4.2, 116.5, 83.5)
	# Ro = 4.4
	self.drawConstantRoArc(thinPen, 4.4, 115.0, 83.0)
	# Ro = 4.6
	self.drawConstantRoArc(thinPen, 4.6, 113.5, 82.5)
	# Ro = 4.8
	self.drawConstantRoArc(thinPen, 4.8, 113.0, 81.0)

	# Ro = 5
	self.drawConstantRoArc(thickPen, 5.0, 112.5, 109.0)
	# Ro = 6
	self.drawConstantRoArc(thinPen, 6.0, 110.5, 129.0)
	# Ro = 7
	self.drawConstantRoArc(thinPen, 7.0, 109.0, 97.5)
	# Ro = 8
	self.drawConstantRoArc(thinPen, 8.0, 108.0, 120.5)
	# Ro = 9
	self.drawConstantRoArc(thinPen, 9.0, 106.0, 89.0)

	# Ro = 10
	self.drawConstantRoArc(thickPen, 10.0, 104.0, 114.0)
	# Ro = 12
	self.drawConstantRoArc(thinPen, 12.0, 102.0, 111.0)
	# Ro = 14
	self.drawConstantRoArc(thinPen, 14.0, 100.0, 106.0)
	# Ro = 16
	self.drawConstantRoArc(thinPen, 16.0, 98.0, 100.0)
	# Ro = 18
	self.drawConstantRoArc(thinPen, 18.0, 96.0, 94.0)

	# Ro = 20
	self.drawConstantRoArc(thickPen, 20.0, 94.0, 88.0)
	# Ro = 50
	self.drawConstantRoArc(thickPen, 50.0, 92.0, 178.0)


    def drawCircles(self):
		
	qp.setPen(thickPen)
	rectangle = Qc.QRectF(-512, -512, 1024, 1024)
	qp.drawArc(rectangle, 0, 5760)
	rectangle.adjust(16, 16, -16, -16)
	qp.setPen(thinPen)
	qp.drawArc(rectangle, 0, 5760)
	
	# Inner thick circle, wavelengths toward load
	rectangle.adjust(16, 16, -16, -16)
	qp.setPen(thickPen)
	qp.drawArc(rectangle, 0, 5760)

	# Inner thin circle, angle of reflection coefficient in degrees
	rectangle.adjust(16, 16, -16, -16)
	qp.setPen(thinPen)
	qp.drawArc(rectangle, 0, 5760)

	# Inner thick circle, angle of transmission coefficient in degrees
	rectangle.adjust(16, 16, -16, -16)
	qp.setPen(thickPen)
	qp.drawArc(rectangle, 0, 5760)

	for i in range (250):
		qp.save()
		qp.rotate(-i*1.44)

		if (i % 5 == 0):
			qp.setPen(thickPen)
			qp.drawLine(493, 0, 499, 0)
		else:
			qp.setPen(thinPen)
			qp.drawLine(493, 0, 499, 0)
		qp.restore()

	for i in range (90,-90,-1):
		qp.save()
		qp.rotate(-i*2.0)

		if (i % 5 == 0):
			qp.setPen(thickPen)
			qp.drawLine(464, 0, 468, 0)
		else:
			qp.setPen(thinPen)
			qp.drawLine(464, 0, 468, 0)
		
		qp.restore()

	qp.setFont(QtGui.QFont("monospace", 8, QtGui.QFont.Light))
	qp.setPen(textPen)

	for i in range (50):
		qp.save()
		qp.rotate(-90)
		qp.rotate((-i*7.2))
		if (i == 0):
			qp.drawText(-14,-595,100,100,
			                  Qc.Qt.AlignLeft | Qc.Qt.AlignBottom,
			                  Qc.QString.number(0.0,'f',2))
		else:
			qp.drawText(-14,-595,100,100,
			                  Qc.Qt.AlignLeft | Qc.Qt.AlignBottom,
			                  Qc.QString.number(0.5-(i*0.01),'f',2))

		qp.drawText(-14,-578,100,100,
		                  Qc.Qt.AlignLeft | Qc.Qt.AlignBottom,
		                  Qc.QString.number(i*0.01,'f',2))
		qp.restore()

	for i in range (18,-18,-1):
		qp.save()
		qp.rotate(90)
		qp.rotate((-i*10.0))

		if (i >= 0):
			qp.drawText((int)((-4.0/9.0)*i-4),-565,100,100,
			                  Qc.Qt.AlignLeft | Qc.Qt.AlignBottom,
			                  Qc.QString.number(i*10))
		else:
			qp.drawText((int)((4.0/9.0)*i-10),-565,100,100,
			                  Qc.Qt.AlignLeft | Qc.Qt.AlignBottom,
			                  Qc.QString.number(i*10))
		qp.restore()

	first = Qc.QPointF()
	second = Qc.QPointF()
	qp.setPen(thinPen)

	for i in range (91):
		second.rx = angleOfTransmissionR[i]*math.cos(i*PI/180.0)
		second.rx -= 448.0
		second.ry = -angleOfTransmissionR[i]*math.sin(i*PI/180.0)
		R = math.sqrt((second.rx*second.rx + 448.0) + second.ry*second.ry)
		first.rx = second.rx - (second.rx * 7.0 / R)
		first.ry = second.ry - (second.ry * 7.0 / R)
		qp.drawLine(first, second)
		first.ry *= -1
		second.ry *= -1
		qp.drawLine(first, second)

	qp.setPen(thickPen)
	qp.drawLine(448, 0, -448, 0)
	qp.save()
	qp.setPen(textPen)
	qp.rotate(-90)
	qp.drawText(Qc.QPointF(0.0,-438.0), Qc.QString.number(0.0,'f',1))
	qp.restore()
	qp.strokePath(thickArcsPath, thickPen)
	qp.strokePath(thinArcsPath, thinPen)

				
    def work(self, input_items, output_items):
	        pass


