import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# function used when plotting the information
def plot_spectrum(fits, fit, fit_weight, bins, bin_perc, xs, ys):
    # AM0 Solar Spectrum
    am = pd.read_excel("AM.xls")

    plt.figure(figsize=(14, 8))
    for x in range(len(bins) - 1):
        plt.text((bins[x] + 10), 0.4, f"{np.round(100*bin_perc[x],0)}%", fontsize=9)
    for nm in bins:
        plt.plot([nm, nm], [0, 4], "--", color="black")
    plt.plot(xs, ys, color="green")
    plt.plot(am["Wavelength (nm)"], am["W*m-2*nm-1"])
    plt.xlim([250, 1250])
    plt.ylim([0, 4])
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Solar Irradiance [W/m^2/nm]")

    plt.show()

    return fit
