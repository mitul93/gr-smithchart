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


