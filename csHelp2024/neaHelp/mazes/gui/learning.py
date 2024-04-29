
import tkinter as tk

window = tk.Tk()
window.geometry('800x500')


scale = tk.Scale(window,  orient='horizontal')
scale.place(x=50, y=20)

window.mainloop()