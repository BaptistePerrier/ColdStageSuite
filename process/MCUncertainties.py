import numpy as np
from matplotlib import pyplot as plt
from scipy import integrate
from scipy.stats import norm
from scipy import interpolate

NS_RESOLUTION = 400 # resolution of ns distribution

NS_PDF_INTEGRATION_PRECISION = 1e-13 # Required precision for computing ns_pdfs via integration

F_RESOLUTION = 200 # f resolution for computing ns distributions

# Using FS010 here
SPECIFICSURFACE = 6.1 # m2g-1
SPECIFICSURFACE_UNCERTAINTY = 0.6

CONCENTRATION = 1 # gL-1
CONCENTRATION_UNCERTAINTY = 0.1 # ARBITRARY FOR NOW, MUST USE REAL VALUES

VOLUME = 20e-9 # Using ColdStage experiments, MUST CHANGE FOR INSEKT EXPERIMENTS
VOLUME_UNCERTAINTY = 1e-10 # ARBITRARY FOR NOW, MUST USE REAL VALUES

A_VALUE = (SPECIFICSURFACE * VOLUME * CONCENTRATION)

DISTRIBS_FROM_FILE = False
DISPLAY = False

# )) Read data from FS010_1_1 for demo )) #
expe_frozenFraction = np.loadtxt("FS/FS010_1_1.txt")
nsValues = - (np.log(1 - expe_frozenFraction[:,1])) / (SPECIFICSURFACE * CONCENTRATION * VOLUME)

nss =  np.vstack((expe_frozenFraction[:,0], nsValues)).T

# )) Reading f-µ distribution )) #

raw_f_mu = np.load("computed_objects/f_mu.npz")
fs = raw_f_mu['fs']
mus = raw_f_mu['mus']
f_mu = raw_f_mu['f_mu']
    
# )) Constructing A distribution )) #

print("# Constructing A distribution")
A_UNCERTAINTY = A_VALUE * np.sqrt((SPECIFICSURFACE_UNCERTAINTY/SPECIFICSURFACE)**2 + (VOLUME_UNCERTAINTY/VOLUME)**2 + (CONCENTRATION_UNCERTAINTY/CONCENTRATION)**2) # Propagating uncertainty
A_pdf = norm(loc=A_VALUE, scale=A_UNCERTAINTY).pdf # Or scale=A_UNCERTAINTY / 2 ???

# )) Constructing ns distribution )) #

print("# Interpolating f-µ distribution")

FS,MUS = np.meshgrid(fs,mus)
MUS = MUS.flatten()
FS = FS.flatten()
coords = list(zip(MUS,FS))
f_mu_interpolator = interpolate.LinearNDInterpolator(coords, f_mu.flatten(), fill_value=0)

# Check if interpolation went ok
#x = np.linspace(mus.min(), mus.max(), 5000)
#y = np.linspace(0, 1, 500)
#X,Y = np.meshgrid(x,y)
#interp_f_mu = f_mu_interpolator(X,Y)
#plt.pcolormesh(Y,X,np.log(interp_f_mu), cmap="jet") # pcolormesh axes are reversed
#plt.show()

print("# Constructing ns distribution")

def integrand(A, ns, f, f_mu_interpolator, A_pdf):
    return abs(A) * f_mu_interpolator(ns * A, f) * A_pdf(A)

nss = np.logspace(2,8,NS_RESOLUTION)
fs = np.linspace(0,1, F_RESOLUTION)

ns_pdfs = []
ns_pdfs_errors = []
i=0
for f in fs:
    i += 1
    print("   -> Distribution {} / {}".format(i, F_RESOLUTION))
    # Plot the µ distribution
    #mu_pdf = f_mu_interpolator(mus, f)
    # Check normalization
    #print(np.trapz(mu_pdf, mus))

    ns_pdf = []
    ns_pdf_error = []
    for ns in nss:
        ns_pdf_i, ns_pdf_error_i = integrate.quad(integrand, 0, 1e-6, (ns, f, f_mu_interpolator, A_pdf), epsabs=NS_PDF_INTEGRATION_PRECISION)
        ns_pdf.append(ns_pdf_i)
        ns_pdf_error.append(ns_pdf_error_i)

    ns_pdfs.append(ns_pdf)
    ns_pdfs_errors.append(ns_pdf_error)

    #Checking normalization
    #print(np.trapz(ns_pdf, x=nss))

ns_pdfs = np.array(ns_pdfs)

# Saving the integration results
print("# Saving the integration results")
np.savez("computed_objects/ns", fs=fs, nss=nss, ns_pdfs=ns_pdfs, ns_pdfs_errors=ns_pdfs_errors)