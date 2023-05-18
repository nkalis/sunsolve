import pkgutil

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# function used when plotting the information
def plot_spectrum(fits, fit, fit_weight, bins, bin_perc, xs, ys):
    """_summary_

    Args:
        fits (_type_): _description_
        fit (_type_): _description_
        fit_weight (_type_): _description_
        bins (_type_): _description_
        bin_perc (_type_): _description_
        xs (_type_): _description_
        ys (_type_): _description_

    Returns:
        _type_: _description_
    """

    am0_data = pkgutil.get_data(__package__, "data/am0.xls")
    am0 = pd.read_excel(am0_data)

    plt.figure(figsize=(14, 8))
    for x in range(len(bins) - 1):
        plt.text((bins[x] + 10), 0.4, f"{np.round(100*bin_perc[x],0)}%", fontsize=9)
    for nm in bins:
        plt.plot([nm, nm], [0, 4], "--", color="black")
    plt.plot(xs, ys, color="green")
    plt.plot(am0["Wavelength (nm)"], am0["W*m-2*nm-1"])
    plt.xlim([250, 1250])
    plt.ylim([0, 4])
    plt.xlabel("Wavelength [nm]")
    plt.ylabel("Solar Irradiance [W/m^2/nm]")

    plt.show()

    return fit
