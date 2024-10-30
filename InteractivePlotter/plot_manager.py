import matplotlib.pyplot as plt
import numpy as np
from rich.panel import Panel
from rich.console import Console
from rich import box

class PlotManager:
    def __init__(self, title, xlabel, ylabel, grid, params, custom_formula):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.grid = grid

        self.params = params if params else {"a": 1, "b": 1}
        self.custom_formula = custom_formula if custom_formula else "a * np.sin(b * x)"
        self.labels = []

        plt.ion()
        self.fig, self.ax = plt.subplots()
        self.console = Console()

    def plot(self):
        x = np.linspace(-10, 10, 100)
        try:
            y = eval(self.custom_formula, {"np": np}, {**self.params, "x": x})
        except Exception as e:
            self.console.print(f"[red]Error formula evaluation: {e}[/red]")
            return

        self.ax.clear()
        self.ax.plot(x, y)
        self.ax.set_title(self.title)
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.ax.grid(self.grid)

        for label in self.labels:
            self.ax.annotate(label["text"], (label["x"], label["y"]),
                             textcoords="offset points", xytext=(5, 5), ha='center')

        plt.draw()

    def update_params(self, new_params):
        self.params.update(new_params)
        self.plot()

    def show_settings(self):
        label_str = "\n".join([f"({label['x']}, {label['y']}) -> '{label['text']}'" for label in self.labels]) or "No labels added."

        self.console.print(Panel(
            f"[cyan]Current Settings[/cyan]\n"
            f"Parameters: {self.params}\n"
            f"Formula: y = {self.custom_formula}\n"
            f"Labels:\n{label_str}",
            title="Settings", style="bold green", box=box.ROUNDED))
