###gr-smithchart
-----------------

pyQT based smith chart for GNU Radio

####Steps:

To run this code do following

1. git clone https://github.com/mitul93/gr-smithchart.git
2. cd gr-smithchart
3. mkdir build && cd build
4. cmake ../
5. make
6. make install or sudo make install
7. cd ../examples
8. ./example_smith.py or sudo chmod +x example_smith.py && ./example_smith.py

####Workdone:

- [x] created skeleton for smith chart using pyQT
- [x] created example to check the compatibility with GNU Radio

####Todo:

- [ ] implement method to draw points on graph
- [ ] implement method to draw contineous graph from given points
- [ ] incorporate stream tags or message to display result
- [ ] add major and minor grid

![ScreenShot](https://raw.githubusercontent.com/mitul93/gr-smithchart/master/smithchart_snapshot_070414.jpg)
