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
block.make_block(a)
my_plot.trace(a, y = 39000, nb = 90)
