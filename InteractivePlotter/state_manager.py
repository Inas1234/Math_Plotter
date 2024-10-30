import json

class StateManager:
    def __init__(self, plot_manager):
        self.plot_manager = plot_manager

    def save(self, filename):
        state = {
            "params": self.plot_manager.params,
            "formula": self.plot_manager.custom_formula,
            "labels": self.plot_manager.labels,
            "title": self.plot_manager.title,
            "xlabel": self.plot_manager.xlabel,
            "ylabel": self.plot_manager.ylabel,
            "grid": self.plot_manager.grid
        }
        with open(filename, 'w') as f:
            json.dump(state, f, indent=4)
        print(f"State saved to '{filename}'")

    def load(self, filename):
        with open(filename, 'r') as f:
            state = json.load(f)
        self.plot_manager.params = state.get("params", {})
        self.plot_manager.custom_formula = state.get("formula", "a * np.sin(b * x)")
        self.plot_manager.labels = state.get("labels", [])
        self.plot_manager.title = state.get("title", "Plot")
        self.plot_manager.xlabel = state.get("xlabel", "X-axis")
        self.plot_manager.ylabel = state.get("ylabel", "Y-axis")
        self.plot_manager.grid = state.get("grid", True)
        print(f"State loaded from '{filename}'")
        self.plot_manager.plot()
