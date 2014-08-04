import numpy as np
import matplotlib.pyplot as plt
import plot
import get

a = get.get_stream(x = 0, y = 39000)
plot.trace(a, y = 39000, nb = 90)
print(a)
