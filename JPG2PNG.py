from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def convert_jpg_to_png(input_path, output_path):
    image = Image.open(input_path)
    rgb_image = image.convert('RGB')
    rgb_image.save(output_path, 'PNG')
    messagebox.showinfo("Conversion Complete", f"Image converted and saved as {output_path}")

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("JPEG Image", "*.jpg"), ("All Files", "*.*")])
    if filename:
        selected_file_label.config(text=filename)

def convert_image():
    input_image_path = selected_file_label.cget("text")
    if os.path.exists(input_image_path):
        output_image_path = os.path.splitext(input_image_path)[0] + ".png"
        convert_jpg_to_png(input_image_path, output_image_path)
    else:
        messagebox.showerror("File Not Found", "The selected file does not exist.")

# Create the main window
window = tk.Tk()
window.title("JPEG to PNG Converter")

# Create a label for the selected file
selected_file_label = tk.Label(window, text="Select a JPEG image...")
selected_file_label.pack(pady=10)

# Create a button to browse for the file
browse_button = tk.Button(window, text="Browse", command=browse_file)
browse_button.pack()

# Create a button to start the conversion
convert_button = tk.Button(window, text="Convert", command=convert_image)
convert_button.pack(pady=10)

# Run the main event loop
window.mainloop()
