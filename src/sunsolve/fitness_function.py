import numpy as np
import scipy
import scipy.stats as stats
from scipy.integrate import simps as simps


# fit_sum calculates the sum of fitness values between all the specified bins
def fit_sum(fits_per_bin):
    """This is a function that uses a normalized normal disctribution to add a weighted score to how close the LED simulation is to each
    bin of the solar spectrum. The normal distribution is fitted around a mean of 1, which when using a standard deviation of 0.35, would
    give a maximum score of 1 per bin (ie: a bin with 50% or 150% of the power of the solar spectrum has a score of 0.36). Therefore if
    there are 10 bins, the maximum score is 10 (perfect fit), and the lowest score is 0.

    Args:
        fits_per_bin (_type_): _description_

    Returns:
        fit_sum (_type_): _description_
        fit_weight (_type_): _description_
    """
    fit_weight = []
    for fit in fits_per_bin:
        fit_weight.append(stats.norm.pdf(fit, 1, 0.35) / stats.norm.pdf(1, 1, 0.35))

    fit_sum = sum(fit_weight)

    return fit_sum, fit_weight


# main_calc is the main simulation/fitness calculator. Used for both calculating and potting the results
def main_calc(solution, led_df, am):
    """This is the main formuka

    Args:
        solution (_type_): _description_

    Returns:
        _type_: _description_
    """
    # Take the first half of the chromosome and uses it for brightness. Value is then normalised w.r.t number of values possible.
    brightness = solution[: len(solution) // 2]
    brightness = brightness / (len(led_df.index))
    # Take the second half of the chromosome and use it for the identification of the LED in the LED database
    solution = solution[len(solution) // 2 :]
    # Total power (area under curve)
    tot_pow = 0
    # ys = spectral irradiance [W^2/m^2/nm]
    ys = np.zeros(1500)
    xs = np.linspace(0, 1500, 1500)

    # Iterate through LEDs in solution. Simulate their wavelength and power output using a gaussian distribution and distance from the 'measuring device'.
    for x in range(len(solution)):
        # Select single solution and corresponding brightness of LED
        led = solution[x]
        bright = brightness[x]
        # Retrieve properties of the LED from the database
        power = led_df["Output Power (mw)"][led] * bright
        theta = led_df["Viewing Angle (deg)"][led]
        wavelength = led_df["Peak wavelength (nm)"][led]
        fwhm = led_df["FWHM (nm)"][led]
        # Physical constraints
        d = 0.30  # Distance from measurement device [m]
        r = np.tan(np.deg2rad(theta / 2)) * d  # radius of beam swadth [m^2]
        a = np.pi * r**2  # Area of beam swadth [m^2]
        power_den = (power / 1000) / a  # power density [W/m^2]
        # Sum the total power of all LEDs
        tot_pow = tot_pow + power_den
        # Simulate wavelength distribution ±4 standard deviations from peak-power wavelength
        std_dev = fwhm / 2.3548
        x_min = wavelength - (std_dev * 4)
        x_max = wavelength + (std_dev * 4)
        x, step = np.linspace(x_min, x_max, 20, retstep=True)
        y = scipy.stats.norm.pdf(x, wavelength, std_dev)
        y = y * power_den
        ys = ys + np.interp(xs, x, y, left=0, right=0)

    # Calculate exact number of LED panels would be required
    num_panels = np.ceil(1036.7156 / np.trapz(ys, xs))
    # Scale output of one panel to total number of panels
    ys = ys * num_panels
    # Evalation bins
    bins = list(range(350, 1250, 100))
    fits = []
    for x in range(len(bins) - 1):
        # Calculate actual solar power between two wavelengths from the bins
        # Get index of closest values
        idx1 = am["Wavelength (nm)"].sub(bins[x]).abs().idxmin()
        idx2 = am["Wavelength (nm)"].sub(bins[x + 1]).abs().idxmin()
        sol = simps(am["W*m-2*nm-1"][idx1:idx2], am["Wavelength (nm)"][idx1:idx2])
        # Calculate simulated solar power between two wavelengths from the bins
        idx3 = (np.abs(xs - bins[x])).argmin()
        idx4 = (np.abs(xs - bins[x + 1])).argmin()
        sim = simps(ys[idx3:idx4])
        # Find the % power difference between the two
        fits.append(sim / sol)

    bin_perc = fits
    fit, fit_weight = fit_sum(fits)

    return fits, fit, fit_weight, bins, bin_perc, xs, ys
