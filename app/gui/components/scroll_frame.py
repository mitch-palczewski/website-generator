import tkinter as tk

from app.util.controller import JsonController
colors = JsonController.get_config_data("colors")
C1 = colors["c1"]
C2 = colors["c2"]
C3 = colors["c3"]
C4 = colors["c4"]

class ScrollFrame(tk.Frame):
    def __init__(self, parent, width = 300, height = 300, **kwargs):
        super().__init__(parent, **kwargs)

        self.canvas = tk.Canvas(self, borderwidth=0, width=width, height=height, bg=C1)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.v_scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.v_scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.v_scrollbar.set)
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")

        self.inner_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.inner_frame.bind('<Enter>', self._bind_mousewheel)
        self.inner_frame.bind('<Leave>', self._unbind_mousewheel)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _bind_mousewheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")


