import tkinter as tk
parent = tk.Tk()
parent.title("-Welcome to Python tkinter Basic exercises-")
my_label = tk.Label(parent, text="Label widget")
my_label.grid(column=0, row=0)
parent.mainloop()