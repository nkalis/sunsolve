import pkgutil

import numpy as np
import pandas as pd
import pygad
from prettytable import PrettyTable
from tqdm import tqdm

from sunsolve.fitness_function import fitness_function_factory, main_calc
from sunsolve.plotter import plot_spectrum


class SunSolver:
    def __init__(self, data: pd.DataFrame, num_leds=24):
        """_summary_

        Args:
            data (pd.DataFrame): _description_
            num_leds (int, optional): _description_. Defaults to 24.
        """
        self.leds = data
        self.num_leds = num_leds

        # load am0
        am0_data = pkgutil.get_data(__package__, "data/am0.xls")
        self.am0 = pd.read_excel(am0_data)

    # Generate a randomly generated spectrum
    def random_selection(self, n_leds=24, plot=True, sim_info=True):
        """_summary_

        Args:
            n_leds (int, optional): _description_. Defaults to 24.
            plot (bool, optional): _description_. Defaults to True.
            sim_info (bool, optional): _description_. Defaults to True.

        Returns:
            _type_: _description_
        """
        # Generate a random solution of LED's and Brightnesses
        solution = np.random.randint(len(self.leds.index), size=self.num_leds * 2)

        fits, fit, fit_weight, bins, bin_perc, xs, ys = main_calc(
            solution, led_df=self.leds, am=self.am0
        )

        if sim_info:
            print("\n")
            print("% Accuracy = ", [round(num, 2) for num in bin_perc])
            print("Weighted =", [round(num, 3) for num in fit_weight])
            print("Fits = ", [round(num, 2) for num in fits])
            print("Fit-weights = ", [round(num, 2) for num in fit_weight])
            print("Fitness = ", fit)
            print("\n")

        if plot:
            plot_spectrum(fits, fit, fit_weight, bins, bin_perc, xs, ys)

        return solution

    def solve(
        self,
        num_generations=100,
    ):
        """_summary_

        Args:
            num_generations (int, optional): _description_. Defaults to 100.
        """
        with tqdm(total=num_generations) as pbar:
            ga_instance = pygad.GA(
                num_generations=num_generations,
                sol_per_pop=20,
                num_genes=self.num_leds * 2,
                num_parents_mating=4,
                fitness_func=fitness_function_factory(am=self.am0, led_df=self.leds),
                random_mutation_min_val=0,
                random_mutation_max_val=len(self.leds.index),
                mutation_by_replacement=True,
                mutation_percent_genes=15,
                mutation_type="random",
                parent_selection_type="rank",
                keep_parents=2,
                crossover_type="single_point",
                init_range_low=(len(self.leds.index) / 2) - (len(self.leds.index) / 4),
                init_range_high=(len(self.leds.index) / 2) + (len(self.leds.index) / 8),
                gene_type=int,
                on_generation=lambda _: pbar.update(1),
            )
            ga_instance.run()
            self.ga_solution = ga_instance
            (
                self.solution,
                self.solution_fitness,
                self.solution_idx,
            ) = self.ga_solution.best_solution()

            self.solve_ran = True

    def fitness_plot(self):
        """_summary_"""
        if self.solve_ran:
            self.ga_solution.plot_fitness()

    def plot_solution(self):
        """_summary_"""
        if self.solve_ran:
            fits, fit, fit_weight, bins, bin_perc, xs, ys = main_calc(
                self.solution, led_df=self.leds, am=self.am0
            )
            plot_spectrum(fits, fit, fit_weight, bins, bin_perc, xs, ys)

    def return_solution(self):
        """_summary_"""
        t = PrettyTable(["LED", "Name", "Wavelength", "Brightness"])

        brightness = self.solution[: len(self.solution) // 2]
        brightness = brightness / (len(self.leds.index))
        dna = self.solution[len(self.solution) // 2 :]

        for leds in range(len(dna)):
            led = dna[leds]
            bright = brightness[leds]

            t.add_row(
                [
                    led,
                    self.leds["Name"][led],
                    self.leds["Peak wavelength (nm)"][led],
                    round(bright, 2),
                ]
            )

        t.sortby = "Wavelength"
        print(t)
