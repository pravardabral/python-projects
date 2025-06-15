# basic gradient calculator, choose a start color, end color and number of partitions, and it gives you n number of colors between your chosen colors

import tkinter as tk
from tkinter import colorchooser, messagebox

def hex_to_rgb(hex_code):
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def interpolate(start_rgb, end_rgb, n):
    gradient = []
    for i in range(n):
        interp = tuple(
            int(start_rgb[j] + (float(i)/(n-1)) * (end_rgb[j] - start_rgb[j]))
            for j in range(3)
        )
        gradient.append(rgb_to_hex(interp))
    return gradient

def choose_start_color():
    color = colorchooser.askcolor(title="Choose start color")
    if color[1]:
        start_color_var.set(color[1])

def choose_end_color():
    color = colorchooser.askcolor(title="Choose end color")
    if color[1]:
        end_color_var.set(color[1])

def generate_gradient():
    try:
        start_hex = start_color_var.get()
        end_hex = end_color_var.get()
        n = int(n_entry.get())
        if not (start_hex and end_hex and n > 1):
            raise ValueError
        start_rgb = hex_to_rgb(start_hex)
        end_rgb = hex_to_rgb(end_hex)
        colors = interpolate(start_rgb, end_rgb, n)
        output_text.delete(1.0, tk.END)
        for color in colors:
            output_text.insert(tk.END, color + '\n')
    except Exception:
        messagebox.showerror("Error", "Please enter valid colors and an integer n > 1.")

root = tk.Tk()
root.title("Gradient Hex Color Generator")

start_color_var = tk.StringVar()
end_color_var = tk.StringVar()

tk.Label(root, text="Start Color:").grid(row=0, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=start_color_var, width=10).grid(row=0, column=1)
tk.Button(root, text="Pick", command=choose_start_color).grid(row=0, column=2)

tk.Label(root, text="End Color:").grid(row=1, column=0, padx=5, pady=5)
tk.Entry(root, textvariable=end_color_var, width=10).grid(row=1, column=1)
tk.Button(root, text="Pick", command=choose_end_color).grid(row=1, column=2)

tk.Label(root, text="Number of Colors (n):").grid(row=2, column=0, padx=5, pady=5)
n_entry = tk.Entry(root, width=10)
n_entry.grid(row=2, column=1, columnspan=2)

tk.Button(root, text="Generate Gradient", command=generate_gradient).grid(row=3, column=0, columnspan=3, pady=10)

output_text = tk.Text(root, width=20, height=10)
output_text.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
