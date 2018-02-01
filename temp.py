#!/usr/bin/env python3

import tkinter as tk
from tkinter import ttk


class CustomBox(ttk.Combobox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind('<Map>', self._handle_popdown_font)

    def _handle_popdown_font(self, *args):
        popdown = self.tk.eval('ttk::combobox::PopdownWindow %s' % combo_box)
        self.tk.call('%s.f.l' % popdown, 'configure', '-font', self['font'])


root = tk.Tk()
text_font = ('Courier New', '10')
main_frame = tk.Frame(root, bg='gray')
main_frame.grid()  # main frame
combo_box = CustomBox(main_frame, font=text_font)  # apply font to combobox
combo_box.grid(row=0, column=0)
combo_box["values"] = ["Dupa Romana", "Jest jak śmietana", "Oj dana dana"]
entry_box = ttk.Entry(main_frame, font=text_font)  # apply font to entry
entry_box.grid(row=0, column=1)  # apply font to combobox
root.mainloop()
