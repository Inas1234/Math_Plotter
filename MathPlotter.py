import matplotlib.pyplot as plt
import numpy as np
import ast
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel
from rich import box

class InteractivePlotter:
    def __init__(self,  params = None, custom_formula = None, title = "Plot", xlabel = "xAxis", ylabel = "yAxis", grid = True):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.grid = grid

        self.params = params if params else {"a": 1, "b": 1}
        self.custom_formula = custom_formula if custom_formula else "a * np.sin(b * x)"
        self.labels = []


        self.console = Console()
        plt.ion()
        self.fig, self.ax = plt.subplots()

    def update_params(self, new_params):
        for key, value in new_params.items():
            self.params[key] = value
        self.plot()


    def plot(self):
        x = np.linspace(-10, 10, 100)

        try:
            y = eval(self.custom_formula, {"np": np}, {**self.params, "x":x})
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

    def set_formula(self, custom_formula):
        self.custom_formula = custom_formula
        self.console.print(f"[green]Formula set to: {self.custom_formula}[/green]")
        self.plot()

    def show_settings(self):
        """Display current settings."""
        label_str = "\n".join([f"({label['x']}, {label['y']}) -> '{label['text']}'" for label in self.labels]) or "No labels added."

        self.console.print(Panel(
            f"[cyan]Current Settings[/cyan]\n"
            f"Parameters: {self.params}\n"
            f"Formula: y = {self.custom_formula}\n"
            f"Labels:\n{label_str}",
            title="Settings", style="bold green", box=box.ROUNDED))
        

    def add_label(self, label_data):
        try:
            x = label_data.get("x")
            y = label_data.get("y")
            text = label_data.get("text", "")
            if x is not None and y is not None and text:
                self.labels.append({"x": x, "y": y, "text": text})
                self.console.print(f"[green]Label added: ({x}, {y}) -> '{text}'[/green]")
                self.plot()
            else:
                self.console.print("[red]Invalid label format! Use: label {'x': value, 'y': value, 'text': 'label text'}[/red]")
        except Exception as e:
            self.console.print(f"[red]Error adding label: {e}[/red]")

    def save(self, filename):
        try:
            state = {
                "params": self.params,
                "formula": self.custom_formula,
                "labels": self.labels,
                "title": self.title,
                "xlabel": self.xlabel,
                "ylabel": self.ylabel,
                "grid": self.grid
            }
            with open(filename, 'w') as f:
                json.dump(state, f, indent=4)
            self.console.print(f"[green]State saved to '{filename}'[/green]")
        except Exception as e:
            self.console.print(f"[red]Error saving state: {e}[/red]")
    
    def load_state(self, filename):
        try:
            with open(filename, 'r') as f:
                state = json.load(f)
            
            self.params = state.get("params", {})
            self.custom_formula = state.get("formula", "a * np.sin(b * x)")
            self.labels = state.get("labels", [])
            self.title = state.get("title", "Plot")
            self.xlabel = state.get("xlabel", "X-axis")
            self.ylabel = state.get("ylabel", "Y-axis")
            self.grid = state.get("grid", True)
            
            self.console.print(f"[green]State loaded from '{filename}'[/green]")
            self.plot()
        except Exception as e:
            self.console.print(f"[red]Error loading state: {e}[/red]")


    def parse_command(self, command):
        if command.startswith("params"):
            try:
                new_params = ast.literal_eval(command.replace("params", "").strip())
                if isinstance(new_params, dict):
                    self.update_params(new_params)
                    self.console.print("[green]Parameters updated.[/green]")
                else:
                    self.console.print("[red]Invalid parameter format! Use: params {'param': value}[/red]")
            except (ValueError, SyntaxError):
                self.console.print("[red]Invalid parameter format! Use: params {'param': value}[/red]")

        elif command.startswith("y ="):
            formula = command.replace("y =", "").strip()
            self.set_formula(formula)

        elif command.startswith("label"):
            try:
                label_data = ast.literal_eval(command.replace("label", "").strip())
                if isinstance(label_data, dict):
                    self.add_label(label_data)
                else:
                    self.console.print("[red]Invalid label format! Use: label {'x': value, 'y': value, 'text': 'label text'}[/red]")
            except (ValueError, SyntaxError):
                self.console.print("[red]Invalid label format! Use: label {'x': value, 'y': value, 'text': 'label text'}[/red]")


        elif command == "show":
            self.show_settings()

        elif command == "plot":
            self.plot()

        elif command.startswith("save"):
            filename = command.replace("save", "").strip()
            if filename:
                self.save(filename)
            else:
                self.console.print("[red]Please provide a filename to save the state![/red]")
        
        elif command.startswith("load"):
            filename = command.replace("load", "").strip()
            if filename:
                self.load_state(filename)
            else:
                self.console.print("[red]Please provide a filename to load the state from![/red]")


        elif command == "exit":
            raise KeyboardInterrupt

        else:
            self.console.print("[red]Unknown command![/red]")

    def start(self):
        self.console.print("[cyan]Enter 'params' to set parameters, 'y =' to set the formula, 'show' to display settings, 'plot' to re-plot, or 'exit' to quit.[/cyan]")
        self.plot()

        while True:
            try:
                command = self.console.input("> ")
                self.parse_command(command)
            except KeyboardInterrupt:
                self.console.print("[yellow]Exiting...[/yellow]")
                break
                
        plt.ioff()
        plt.show()
