import ast

class CommandParser:
    def __init__(self, interactive_plotter):
        self.interactive_plotter = interactive_plotter

    def parse(self, command):
        if command.startswith("y ="):
            formula = command.replace("y =", "").strip()
            self.interactive_plotter.plot_manager.custom_formula = formula
            self.interactive_plotter.plot_manager.plot()

        elif command.startswith("params"):
            try:
                new_params = ast.literal_eval(command.replace("params", "").strip())
                if isinstance(new_params, dict):
                    self.interactive_plotter.plot_manager.update_params(new_params)
                else:
                    print("Invalid parameter format! Use: params {'param': value}")
            except (ValueError, SyntaxError):
                print("Invalid parameter format! Use: params {'param': value}")

        elif "=" in command and not command.startswith("y ="):
            try:
                key, value = command.split("=")
                key = key.strip()
                value = float(value.strip())
                if key in self.interactive_plotter.plot_manager.params:
                    self.interactive_plotter.plot_manager.params[key] = value
                    self.interactive_plotter.plot_manager.plot()
                else:
                    print(f"Parameter '{key}' not found.")
            except ValueError:
                print("Invalid parameter format! Use: param {'param': value}")

        elif command == "show":
            self.interactive_plotter.plot_manager.show_settings()

        elif command == "plot":
            self.interactive_plotter.plot_manager.plot()

        elif command.startswith("save"):
            filename = command.replace("save", "").strip()
            self.interactive_plotter.state_manager.save(filename)

        elif command.startswith("load"):
            filename = command.replace("load", "").strip()
            self.interactive_plotter.state_manager.load(filename)

        elif command == "exit":
            raise KeyboardInterrupt

        else:
            print("Unknown command!")

