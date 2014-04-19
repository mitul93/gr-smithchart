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

from gnuradio import gr, blocks
#from gnuradio.qtgui import qtgui
import smithchart as smith
from PyQt4 import QtGui
import sys, sip

class my_tb(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        # Make a local QtApp so we can start it from our side
        self.qapp = QtGui.QApplication(sys.argv)
	
	src_data = (1.0+0j, 0.1+0.3j, 0.3+1.5j, 0.3-1.0j, 1.4+1.4j, 0.1-0.3j)
	self.src = blocks.vector_source_c(src_data)
        self.plot = smith.smithsink()
	self.connect(self.src,self.plot)

def main():
    tb = my_tb()
    tb.start()
    tb.qapp.exec_()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
