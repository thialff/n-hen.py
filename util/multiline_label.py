import tkinter as tk


class MultilineLabel(tk.Text):

    def __init__(self, **kw):
        super().__init__(**kw)

        self.configure(wrap=tk.WORD, bg=self.master['bg'], bd=0, cursor='arrow', state=tk.DISABLED)
        self.bindtags((str(self), str(self.master), "all"))

    def setText(self, text: str):
        self.configure(state=tk.NORMAL)
        self.insert(tk.INSERT, text)
        self.configure(state=tk.DISABLED)
