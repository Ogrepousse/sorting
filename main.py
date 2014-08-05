import numpy as np
import matplotlib.pyplot as plt
#import plot
#import get
import libpy
from libpy import get_data
from libpy.get_data import get
from libpy import plot
from libpy.plot import my_plot
from libpy import fitting
from libpy.fitting import block

a = get.get_stream(x = 0, y = 39000)
print(a)
median = block.cal_median(a)
mad = block.stand_dev(a, median)
print(mad[90])
print(median[90])
#block.check_thresh(a, median, mad, 1000)
s = block.make_block(a, y = 39000)
my_plot.trace(a, median, mad, y = 39000, nb = 90)
