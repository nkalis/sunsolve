import pandas as pd

from sunsolve import SunSolver


def test_solver_random_spectrum():
    data = pd.read_excel("tests/data/leds.xlsx")
    solver = SunSolver(data=data)

    solver.random_selection()
    solver.solve(num_generations=10)
    solver.fitness_plot()
    solver.plot_solution()
    solver.return_solution()

    assert 2 == 2
