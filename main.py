from InteractivePlotter import InteractivePlotter

params = {"a": 1, "b": 2, "frequency": 1}
plotter = InteractivePlotter(params, "a * np.cos(frequency * x)")

plotter.start()

             


