from rich.console import Console
from   .plot_manager import PlotManager
from  .state_manager import StateManager
from  .command_parser import CommandParser
from  .label_manager import LabelManager
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory

class InteractivePlotter:
    def __init__(self, params=None, custom_formula=None, title="Plot", xlabel="xAxis", ylabel="yAxis", grid=True):
        self.console = Console()
        self.plot_manager = PlotManager(title, xlabel, ylabel, grid, params, custom_formula)
        self.state_manager = StateManager(self.plot_manager)
        self.label_manager = LabelManager(self.plot_manager)
        self.command_parser = CommandParser(self)
        
    def start(self):
        self.console.print("[cyan]Enter 'params' to set parameters, 'y =' to set the formula, 'show' to display settings, 'plot' to re-plot, or 'exit' to quit.[/cyan]")
        self.plot_manager.plot()
        while True:
            try:
                command = self.console.input("> ")
                self.command_parser.parse(command)
            except KeyboardInterrupt:
                self.console.print("[yellow]Exiting...[/yellow]")
                break
