'''
Created on 14/11/2014

@author: Kevin
'''
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)

t = np.arange(0.0, 5.0, 0.01)
s = np.cos(2*np.pi*t)
line, = ax.plot(t, s, lw=2)

ax.annotate('', xy=(2, 1), xytext=(2, 1.5),
            arrowprops=dict(facecolor='green', shrink=0.05),
            )
ax.annotate('', xy=(2.5, -1), xytext=(2.5, -1.5),
            arrowprops=dict(facecolor='red', shrink=0.05),
            )

ax.set_ylim(-2, 2)
plt.show()
