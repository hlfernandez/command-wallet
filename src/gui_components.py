import tkinter as tk

class LabelInput(tk.Frame):

    def __init__(self, parent, label, inp_cls, inp_args, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.label = tk.Label(self, text=label, anchor='w')
        self.input = inp_cls(self, **inp_args)

        self.columnconfigure(0, weight=1)
        self.label.grid(sticky=tk.E + tk.W)
        self.input.grid(sticky=tk.E + tk.W)