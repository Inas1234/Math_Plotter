class LabelManager:
    def __init__(self, plot_manager):
        self.plot_manager = plot_manager

    def add_label(self, x, y, text):
        if x is not None and y is not None and text:
            self.plot_manager.labels.append({"x": x, "y": y, "text": text})
            self.plot_manager.plot()
        else:
            print("Invalid label format! Use: {'x': value, 'y': value, 'text': 'label text'}")
