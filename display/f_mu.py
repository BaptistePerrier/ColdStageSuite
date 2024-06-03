import numpy as np
from matplotlib import pyplot as plt

raw_f_mu = np.load("computed_objects/f_mu.npz")
fs = raw_f_mu['fs']
mus = raw_f_mu['mus']
f_mu = raw_f_mu['f_mu']

x, y = np.meshgrid(fs, mus) # Axes are reverse for pcolormesh
plt.pcolormesh(x,y,np.log(f_mu), cmap="jet")
plt.colorbar()

plt.ylabel("$\mu$")
plt.xlabel("f")
plt.title("$log$ of $f$-$\mu$ probability density function")
plt.show()
