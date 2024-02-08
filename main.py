import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from sympy import symbols, lambdify

class Plotter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1280x960")
        self.root.configure(bg='light grey')

        self.is_plotted = False

        self.canvas_frame = tk.Frame(self.root, bg='light grey')
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.button_frame = tk.Frame(self.root, bg='light grey')
        self.button_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.figure, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.figure, self.canvas_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.canvas_frame)
        self.toolbar.update()
        self.canvas.mpl_connect('motion_notify_event', self.on_motion)

        self.function_entry = tk.Entry(self.button_frame, font=('Arial', 14), bg='white', relief=tk.SUNKEN, bd=2)
        self.function_entry.pack(pady=10, padx=10)

        self.plot_button = tk.Button(self.button_frame, text="Plot", command=self.plot_function, font=('Arial', 14), bg='light blue', relief=tk.RAISED, bd=2)
        self.plot_button.pack(pady=10, padx=10)

        self.point = None  
        self.text = None  

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def plot_function(self):
        x = symbols('x')
        function_str = self.function_entry.get()
        function = lambdify(x, function_str, 'numpy')
        self.x_vals = np.linspace(-10, 10, 400)
        self.y_vals = function(self.x_vals)
        self.ax.clear()
        self.ax.plot(self.x_vals, self.y_vals)
        self.ax.grid(True)
        self.ax.axhline(0, color='black')
        self.ax.axvline(0, color='black')
        self.canvas.draw()

    def close_window(self): 
        # self.root.destroy()
        exit()

    def on_motion(self, event):
        if self.is_plotted:
            if event.xdata is not None and event.ydata is not None:
                closest_index = np.abs(self.x_vals - event.xdata).argmin()
                closest_x = self.x_vals[closest_index]
                closest_y = self.y_vals[closest_index]
                if self.point is not None:  
                    self.point.remove()  
                self.point, = self.ax.plot([closest_x], [closest_y], 'ro')  
                if self.text is not None:  
                    self.text.remove()  
                self.text = self.ax.text(closest_x, closest_y, f'({closest_x:.2f}, {closest_y:.2f})')  
                self.canvas.draw()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    plotter = Plotter()
    plotter.run()
