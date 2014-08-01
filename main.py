import numpy as np
import matplotlib.pyplot as plt
import plot
import get

a = get.get_stream(x = 20000, y = 30000)
plot.trace(a, y = 10000, nb = 90)
print(a)
