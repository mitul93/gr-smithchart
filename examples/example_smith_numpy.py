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

from gnuradio import gr
#from gnuradio.qtgui import qtgui
import smithchart as smith
from PyQt4 import QtGui
import sys, sip

class my_tb(gr.top_block):
    def __init__(self):
        gr.top_block.__init__(self)

        self.qapp = QtGui.QApplication(sys.argv)
        self.plot = smith.smithsink_numpy()

def main():
    tb = my_tb()
    tb.start()
    tb.qapp.exec_()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
