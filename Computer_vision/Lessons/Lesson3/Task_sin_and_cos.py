import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(-4 * np.pi, 4 * np.pi, 10000)

sn = 4 * np.sin(x)
cs = np.cos(x * 2)
plt.plot(x, sn, "-o", label="sin")
plt.plot(x, cs, "-o", label="cos")
plt.legend()
plt.grid()
plt.show()
