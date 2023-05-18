import pytest
import pandas as pd

from sunsolve import sunsolver

data = pd.read_excel('tests/data/leds.xlsx')
solver = sunsolver(data=data, num_leds=5)

random_solution = solver.random_selection()
print(random_solution)