import numpy as np
from matplotlib import pyplot as plt

# Using FS010 here
dataFile = "data/FS/FS010_1_1.txt"
SPECIFICSURFACE = 6.1 # m2g-1
CONCENTRATION = 1 # gL-1
VOLUME = 20e-9 # Using ColdStage experiments, MUST CHANGE FOR INSEKT EXPERIMENTS

A_VALUE = (SPECIFICSURFACE * VOLUME * CONCENTRATION)

# )) Read data from FS010_1_1 for demo )) #
expe_frozenFraction = np.loadtxt(dataFile)
nsValues = - (np.log(1 - expe_frozenFraction[:,1])) / (A_VALUE)

# )) Read uncertainties data from file )) #
raw_uncertainties = np.load("computed_objects/uncertainties.npz", allow_pickle=True)
nss = raw_uncertainties['nss']
fs = raw_uncertainties['fs']
lower_uncertainties = raw_uncertainties['lower_uncertainties']
upper_uncertainties = raw_uncertainties['upper_uncertainties']

def find_nearest(value):
    global fs
    array = - (np.log(1 - fs)) / (A_VALUE)
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (idx == len(array) or float(abs(value - array[idx-1])) < float(abs(value - array[idx]))):
        return idx-1
    else:
        return idx
    
def find_nearest_bak(value):
    global fs
    array = - (np.log(1 - fs)) / (A_VALUE)
    idx = (np.abs(array - value)).argmin()
    return idx

# )) Use closest ns value for uncertainties estimation (thus we don't need linear interpolation)
app = np.vectorize(find_nearest)
associated_ns_i = app(nsValues)
print(lower_uncertainties.shape, nsValues.shape)
fs_ns = - np.log(1 - fs) / A_VALUE

nsValues = fs_ns[associated_ns_i]

expe_lower_uncertainties = abs(nsValues - lower_uncertainties[associated_ns_i])
expe_upper_uncertainties = abs(upper_uncertainties[associated_ns_i] - nsValues)



# )) Plot the final ns graph with uncertainties ))

Ts = expe_frozenFraction[:,0]
expe_fs = expe_frozenFraction[:,1]
expe_ns = -(np.log(1 - expe_fs)) / A_VALUE
#plt.plot(Ts, lower_uncertainties[associated_ns_i], c="r")
#plt.plot(Ts, upper_uncertainties[associated_ns_i], c="g")
plt.errorbar(Ts, nsValues, [expe_lower_uncertainties, expe_upper_uncertainties], linestyle="")
plt.scatter(Ts, nsValues, marker="s", c="k", s=10, zorder=10)
plt.yscale("log")
plt.ylim((1e1, 1e9))
plt.title(dataFile)
plt.show()