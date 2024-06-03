import numpy as np
import os

BETSurfaces = {"FS010" : 6.1, "FS010xk43" : 4.9, "FS011" : 3.6, "FS011xk43" : 14.2, "FS015" : 7.2}

for subdir, dirs, files in os.walk("FS"):
    for file in files:
        filepath = subdir + os.sep + file
        
        rawData = np.loadtxt(filepath)

        sampleName = file.split('_')[0]
        surface = BETSurfaces[sampleName]
        
        ns = - (np.log(1 - rawData[:,1])) / (surface)

        output = np.vstack((rawData[:,0], ns)).T

        outfile = "ns" + os.sep + file.split(".")[0] + "_ns.txt"
        np.savetxt(outfile, output)