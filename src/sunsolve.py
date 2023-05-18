import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import random
import scipy.stats as stats
from scipy.stats import norm
from scipy import signal
from scipy.integrate import simps as simps
import math
import operator
import pygad
import pygad.gann
from time import sleep
import sys
import typing

from plot_spectrum.plotter import plot_spectrum

class SunSolve:

    def __init__(self, data: pd.DataFrame):
            # variables generated during matching
            # assign unique indices to test and control
            
            #assert some checks for the dataframe
            self.leds = data
    
    # Generate a randomly generated spectrum
    def random_selection(self, n_leds=24, plot=False, sim_info=False):
        # Select number of LEDs to be present
        num_leds = 24

        # Generate a random solution of LED's and Brightnesses
        dna = np.random.randint(len(self.leds.index), size=num_leds*2)

        fits, fit, fit_weight, bins, bin_perc, xs, ys = main_calc(solution)

        if sim_info:
            print('\n')
            print('% Accuracy = ', [round(num, 2) for num in bin_perc])
            print('Weighted =', [round(num, 3) for num in fit_weight])
            print('Fits = ', [round(num, 2) for num in fits])
            print('Fit-weights = ', [round(num, 2) for num in fit_weight])
            print('Fitness = ', fit)
            print('\n')

        if plot:
            plot_spectrum(fits, fit, fit_weight, bins, bin_perc, xs, ys)

        return