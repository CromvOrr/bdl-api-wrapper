import tkinter as tk
from tkinter import ttk
import figures as fig
import os


def switch_plot(*args):
    selected_plot = plot_selector.get()
    _img_path = f'plot_{selected_plot}.png'
    if os.path.exists(_img_path):
        _img = tk.PhotoImage(file=_img_path)
        plot_display.config(image=_img)
        plot_display.image = _img


def run(_df, years_list):
    try:
        root = tk.Tk()
        root.title('Plot Viewer')

        fig.generate_plots(_df, years_list)

        plot_selector_value = tk.StringVar()

        global plot_selector
        plot_selector = ttk.Combobox(root, textvariable=plot_selector_value, values=list(map(str, years_list)),
                                     state="readonly")
        plot_selector.set(years_list[0])
        plot_selector.grid(row=0, column=0)

        plot_selector_value.trace_add('write', switch_plot)

        img_path = f'plot_{years_list[0]}.png'
        img = tk.PhotoImage(file=img_path)

        global plot_display
        plot_display = tk.Label(root, image=img)
        plot_display.grid(row=1, columnspan=2)

        root.mainloop()
    except TypeError:
        print('ERROR 100')

    try:
        for i in years_list:
            img_path = f'plot_{i}.png'
            if os.path.exists(img_path):
                os.remove(img_path)
    except TypeError:
        print('ERROR 200')
