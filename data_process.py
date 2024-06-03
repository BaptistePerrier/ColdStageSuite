import numpy as np
from matplotlib import pyplot as plt
from scipy.interpolate import interp1d
import os

DISPLAY = True
INTERPOLATED = False

def readDataFromFolder(samples, folderPath="FS", freezingFractionInterpStep=0.001, renormalize=False):
    outDict = {}
    interpDict = {}
    for sampleName, value in samples.items():
        for experiment_i in range(value["experiments_n"]):
            experimentName = sampleName + "_" + str(experiment_i+1)
            outDict[experimentName] = {"data" : []}
            interpDict[experimentName] = {"data" : []}

            for subdir,_,files in os.walk(folderPath):
                for file in files:
                    filepath = subdir + os.sep + file

                    if experimentName in file:
                        # Reading data from file
                        currentData = np.loadtxt(filepath)

                        if renormalize:
                            currentData[:,1] = currentData[:,1] / currentData[:,1].max()

                        outDict[experimentName]["data"].append(currentData)

                        # Interpolation
                        freezingFractionAxis = np.arange(0, 1, freezingFractionInterpStep)
                        interpolator = interp1d(currentData[:,1], currentData[:,0], bounds_error=False)
                        freezingFractionInterpolation = interpolator(freezingFractionAxis)

                        run = np.vstack((freezingFractionInterpolation, freezingFractionAxis)).T

                        interpDict[experimentName]["data"].append(run)

                interpDict[experimentName]["data"] = np.array(interpDict[experimentName]["data"])

    """outDict = { "FS010_1" : [ (run1[:,0], run1[:,1]) , (run2[:,0], run2[:,1]) , ...],
                    "FS010_2" : [ (run1[:,0], run1[:,1]) , (run2[:,0], run2[:,1]) , ...],
                    "FS011_1" : ...,
                    ...
                }
    """
    if INTERPOLATED: return interpDict
    else: return outDict

def ns(run, specificSurface, concentration=1.0, dropletVolume=20e-9):
    nsValues = - (np.log(1 - run[:,1])) / (specificSurface * concentration * dropletVolume)

    return np.vstack((run[:,0], nsValues)).T

# ))))) Cold Stage data ))))) #

# Defining samples parameters
coldStageSamples = {
    "FS010" : {
        "experiments_n" : 2,
        "specificSurface" : 6.1, # m2g-1
        "specificSurfaceUncertainties" : 0.6
    }, 
    "FS010xk43" : {
        "experiments_n" : 2,
        "specificSurface" : 4.9, # m2g-1
        "specificSurfaceUncertainties" : 0.5
    }, 
    "FS011" : {
        "experiments_n" : 2,
        "specificSurface" : 3.6, # m2g-1
        "specificSurfaceUncertainties" : 0.6
    }, 
    "FS011xk43" : {
        "experiments_n" : 2,
        "specificSurface" : 14.2, # m2g-1
        "specificSurfaceUncertainties" : 1.5
    }, 
    "FS015" : {
        "experiments_n" : 2,
        "specificSurface" : 7.2, # m2g-1
        "specificSurfaceUncertainties" : 3.3
    }
}

coldStageData = readDataFromFolder(coldStageSamples, folderPath="FS", renormalize=False)

if INTERPOLATED:
# ))))) CALCULATE AVG ))))) #
# Cannot calculate AVG if data is not interpolated
    for experimentName, experiment in coldStageData.items():
        avg = np.nanmean(experiment["data"], axis=0)
        experiment["avg"] = avg

# ))))) PLOT AVG ))))) #
    fig, axs = plt.subplots(2,5)
    axs = axs.flatten()

    # fig.tight_layout()
    plt.subplots_adjust(wspace=0.215)
    fig.suptitle("[Cold Stage] Averaged frozen fraction", fontsize=25)
    for experiment_i in range(len(list(coldStageData.keys()))):
        experimentName = list(coldStageData.keys())[experiment_i]
        axs[experiment_i].set_title(experimentName)
        axs[experiment_i].set_xlabel("T (°C)")
        
        axs[experiment_i].plot(coldStageData[experimentName]["avg"][:,0], coldStageData[experimentName]["avg"][:,1])

    if DISPLAY: plt.show()

    # ))))) CALCULATE Ns )))))
    for experimentName, experiment in coldStageData.items():
        coldStageData[experimentName]["ns"] = []
        coldStageData[experimentName]["ns"] = ns(experiment["avg"], coldStageSamples[experimentName.split("_")[0]]["specificSurface"])

    # ))))) PRINT Ns )))))
    fig, axs = plt.subplots(2,5)
    axs = axs.flatten()

    # fig.tight_layout()
    plt.subplots_adjust(wspace=0.215)
    fig.suptitle("[Cold Stage] Active site density ($m^{-2}$)", fontsize=25)
    for experiment_i in range(len(list(coldStageData.keys()))):
        experimentName = list(coldStageData.keys())[experiment_i]
        axs[experiment_i].set_title(experimentName)
        axs[experiment_i].set_xlabel("T (°C)")

        axs[experiment_i].plot(coldStageData[experimentName]["ns"][:,0], coldStageData[experimentName]["ns"][:,1])
        axs[experiment_i].set_yscale('log')
        axs[experiment_i].set_ylim(1e2, 1e8)
        axs[experiment_i].set_xlim(-35,-3)

    if DISPLAY: plt.show()

else:
# If data is not interpolated, we print every run
    # ))))) PRINT RAW DATA ))))) #
    fig, axs = plt.subplots(2,5)
    axs = axs.flatten()

    # fig.tight_layout()
    plt.subplots_adjust(wspace=0.215)
    fig.suptitle("[Cold Stage] Freezing fraction of samples", fontsize=25)
    for ax_i in range(len(axs)):
        experimentName = list(coldStageData.keys())[ax_i]
        axs[ax_i].set_title(experimentName)
        axs[ax_i].set_xlabel("T (°C)")

        for run in coldStageData[experimentName]["data"]:
            axs[ax_i].scatter(run[:,0], run[:,1], marker="x")

    if DISPLAY: plt.show()

    # ))))) CALCULATE Ns )))))
    for experimentName, experiment in coldStageData.items():
        coldStageData[experimentName]["ns"] = []
        for run in coldStageData[experimentName]["data"]:
            coldStageData[experimentName]["ns"].append(ns(run, coldStageSamples[experimentName.split("_")[0]]["specificSurface"]))

    # ))))) PRINT Ns )))))
    fig, axs = plt.subplots(2,5)
    axs = axs.flatten()

    plt.subplots_adjust(wspace=0.215)
    fig.suptitle("[Cold Stage] Active site density ($m^{-2}$)", fontsize=25)
    for ax_i in range(len(axs)):
        experimentName = list(coldStageData.keys())[ax_i]
        axs[ax_i].set_title(experimentName)
        axs[ax_i].set_xlabel("T (°C)")

        for run in coldStageData[experimentName]["ns"]:
            axs[ax_i].scatter(run[:,0], run[:,1], marker="x")
            axs[ax_i].set_yscale('log')
            axs[ax_i].set_ylim(1e2, 1e8)
            axs[ax_i].set_xlim(-35,-3)

    if DISPLAY: plt.show()


# ))))) Johana's data ))))) #

JosSamples = {
    "FS010" : {
        "experiments_n" : 2,
        "specificSurface" : 6.1, # m2g-1
        "specificSurfaceUncertainties" : 0.6
    }, 
    "FS010xk43" : {
        "experiments_n" : 2,
        "specificSurface" : 4.9, # m2g-1
        "specificSurfaceUncertainties" : 0.5
    }, 
    "FS011" : {
        "experiments_n" : 2,
        "specificSurface" : 3.6, # m2g-1
        "specificSurfaceUncertainties" : 0.6
    }, 
    "FS011xk43" : {
        "experiments_n" : 2,
        "specificSurface" : 14.2, # m2g-1
        "specificSurfaceUncertainties" : 1.5
    }
}

JosData = readDataFromFolder(JosSamples, folderPath="Jos", renormalize=False)


if INTERPOLATED:
# ))))) CALCULATE AVG ))))) #
# Cannot calculate AVG if data is not interpolated
    for experimentName, experiment in JosData.items():
        avg = np.nanmean(experiment["data"], axis=0)
        experiment["avg"] = avg

# ))))) PLOT AVG ))))) #
    fig, axs = plt.subplots(2,5)
    axs = axs.flatten()

    # fig.tight_layout()
    plt.subplots_adjust(wspace=0.215)
    fig.suptitle("[INSEKT] Averaged frozen fraction", fontsize=25)
    for experiment_i in range(len(list(JosData.keys()))):
        experimentName = list(JosData.keys())[experiment_i]
        axs[experiment_i].set_title(experimentName)
        axs[experiment_i].set_xlabel("T (°C)")
        
        axs[experiment_i].plot(JosData[experimentName]["avg"][:,0], JosData[experimentName]["avg"][:,1])

    if DISPLAY: plt.show()

    # ))))) CALCULATE Ns )))))
    for experimentName, experiment in JosData.items():
        JosData[experimentName]["ns"] = []
        JosData[experimentName]["ns"] = ns(experiment["avg"], JosSamples[experimentName.split("_")[0]]["specificSurface"], dropletVolume=15e-6)

    # ))))) PRINT Ns )))))
    fig, axs = plt.subplots(2,5)
    axs = axs.flatten()

    # fig.tight_layout()
    plt.subplots_adjust(wspace=0.215)
    fig.suptitle("[INSEKT] Active site density ($m^{-2}$)", fontsize=25)
    for experiment_i in range(len(list(JosData.keys()))):
        experimentName = list(JosData.keys())[experiment_i]
        axs[experiment_i].set_title(experimentName)
        axs[experiment_i].set_xlabel("T (°C)")

        axs[experiment_i].plot(JosData[experimentName]["ns"][:,0], JosData[experimentName]["ns"][:,1])
        axs[experiment_i].set_yscale('log')
        axs[experiment_i].set_ylim(1e2, 1e8)
        axs[experiment_i].set_xlim(-35,-3)

    if DISPLAY: plt.show()

else:
# If data is not interpolated, we print every run
    # ))))) PRINT RAW DATA ))))) #
    fig, axs = plt.subplots(2,5)
    print(axs.shape)
    axs = axs.flatten()
    print(axs.shape)
    print(list(JosData.keys()))

    # fig.tight_layout()
    plt.subplots_adjust(wspace=0.215)
    fig.suptitle("[INSEKT] Freezing fraction of samples", fontsize=25)
    for experiment_i in range(len(list(JosData.keys()))):
        print(experiment_i)
        experimentName = list(JosData.keys())[experiment_i]
        axs[experiment_i].set_title(experimentName)
        axs[experiment_i].set_xlabel("T (°C)")

        for run in JosData[experimentName]["data"]:
            axs[experiment_i].scatter(run[:,0], run[:,1], marker="x")

    if DISPLAY: plt.show()

    # ))))) CALCULATE Ns )))))
    for experimentName, experiment in JosData.items():
        JosData[experimentName]["ns"] = []
        for run in JosData[experimentName]["data"]:
            JosData[experimentName]["ns"].append(ns(run, JosSamples[experimentName.split("_")[0]]["specificSurface"], dropletVolume=15e-6))

    # ))))) PRINT Ns )))))
    fig, axs = plt.subplots(2,5)
    axs = axs.flatten()

    plt.subplots_adjust(wspace=0.215)
    fig.suptitle("[INSEKT] Active site density ($m^{-2}$)", fontsize=25)
    for experiment_i in range(len(list(JosData.keys()))):
        experimentName = list(JosData.keys())[experiment_i]
        axs[experiment_i].set_title(experimentName)
        axs[experiment_i].set_xlabel("T (°C)")

        for run in JosData[experimentName]["ns"]:
            axs[experiment_i].scatter(run[:,0], run[:,1], marker="x")
            axs[experiment_i].set_yscale('log')
            axs[experiment_i].set_ylim(1e2, 1e8)
            axs[experiment_i].set_xlim(-35,-3)

    if DISPLAY: plt.show(); fig.tight_layout()


# ))))) Combining Ns ))))) #

if INTERPOLATED:
    # ))))) PRINT Ns )))))
    fig, axs = plt.subplots(2,2)
    axs = axs.flatten()

    # fig.tight_layout()
    plt.subplots_adjust(wspace=0.215)
    fig.suptitle("[Combined] Active site density ($m^{-2}$)", fontsize=25)

    samplesAxs = {}
    sample_i = 0

    for experiment_i in range(len(list(coldStageData.keys()))):
        experimentName = list(coldStageData.keys())[experiment_i]
        if experimentName in list(JosData.keys()):
            sampleName = experimentName.split("_")[0]

            if not sampleName in list(samplesAxs.keys()):
                samplesAxs[sampleName] = sample_i
                print(sampleName, sample_i)
                sample_i += 1

            axs[samplesAxs[sampleName]].set_title(sampleName)
            axs[samplesAxs[sampleName]].set_xlabel("T (°C)")

            axs[samplesAxs[sampleName]].plot(coldStageData[experimentName]["ns"][:,0], coldStageData[experimentName]["ns"][:,1], "b")
            axs[samplesAxs[sampleName]].plot(JosData[experimentName]["ns"][:,0], JosData[experimentName]["ns"][:,1], "r")
            

            axs[samplesAxs[sampleName]].set_yscale('log')
            axs[samplesAxs[sampleName]].set_ylim(1e2, 1e8)
            axs[samplesAxs[sampleName]].set_xlim(-35,-3)

    if DISPLAY: plt.show()

else:
    # ))))) PRINT Ns )))))
    fig, axs = plt.subplots(2,2)
    axs = axs.flatten()

    # fig.tight_layout()
    plt.subplots_adjust(wspace=0.215)
    fig.suptitle("[Combined] Active site density ($m^{-2}$)", fontsize=25)

    samplesAxs = {}
    sample_i = 0

    for experiment_i in range(len(list(coldStageData.keys()))):
        experimentName = list(coldStageData.keys())[experiment_i]
        if experimentName in list(JosData.keys()):
            sampleName = experimentName.split("_")[0]

            if not sampleName in list(samplesAxs.keys()):
                samplesAxs[sampleName] = sample_i
                print(sampleName, sample_i)
                sample_i += 1

            axs[samplesAxs[sampleName]].set_title(sampleName)
            axs[samplesAxs[sampleName]].set_xlabel("T (°C)")

            for run in coldStageData[experimentName]["ns"]:
                axs[samplesAxs[sampleName]].scatter(run[:,0], run[:,1], marker="x", color="b")
            for run in JosData[experimentName]["ns"]:
                axs[samplesAxs[sampleName]].scatter(run[:,0], run[:,1], marker="x", color="r")            

            axs[samplesAxs[sampleName]].set_yscale('log')
            axs[samplesAxs[sampleName]].set_ylim(1e2, 1e8)
            axs[samplesAxs[sampleName]].set_xlim(-35,-3)

    if DISPLAY: plt.show()
