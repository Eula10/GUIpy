import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image

class DragDropImage:
    def __init__(self, canvas, image_path, x, y, bird_id, main_window):
        self.canvas = canvas
        self.main_window = main_window
        self.bird_id = bird_id
        self.image = Image.open(image_path).resize((100, 100))
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_id = self.canvas.create_image(x, y, image=self.image_tk)
        self.canvas.tag_bind(self.image_id, "<Button-1>", self.start_drag)
        self.canvas.tag_bind(self.image_id, "<B1-Motion>", self.drag)
        self.canvas.tag_bind(self.image_id, "<ButtonRelease-1>", self.drop)
        self.canvas.tag_bind(self.image_id, "<Button-3>", self.open_menu)
        self.is_dragging = False
        self.offset_x = 0
        self.offset_y = 0
        self.text_id = self.canvas.create_text(x, y + 60, text=f"ID: {self.bird_id}")

    def start_drag(self, event):
        self.is_dragging = True
        self.offset_x = event.x
        self.offset_y = event.y

    def drag(self, event):
        if self.is_dragging:
            dx = event.x - self.offset_x
            dy = event.y - self.offset_y
            self.move_image_with_id(dx, dy)
            self.offset_x = event.x
            self.offset_y = event.y

    def drop(self, event):
        self.is_dragging = False

    def move_image_with_id(self, dx, dy):
        self.canvas.move(self.image_id, dx, dy)
        self.canvas.move(self.text_id, dx, dy)

    def open_menu(self, event):
        menu = tk.Menu(self.canvas, tearoff=0)
        menu.add_command(label="Properties", command=self.open_properties)
        menu.add_command(label="Delete", command=self.delete)
        menu.post(event.x_root, event.y_root)

    def open_properties(self):
        properties_window = tk.Toplevel()
        properties_window.title("Bird Properties")
        properties_window.geometry("300x150")

        # Create labels and entry field
        label_id = tk.Label(properties_window, text="ID:")
        entry_id = tk.Entry(properties_window)
        entry_id.insert(tk.END, self.bird_id)
        label_id.pack()
        entry_id.pack()

        def save_properties():
            new_id = entry_id.get()
            if new_id != self.bird_id:
                if new_id in [image.bird_id for image in [image1, image2, image3] if image != self]:
                    messagebox.showerror("Error", "ID already exists for another bird.")
                    return
                self.bird_id = new_id
                self.canvas.itemconfigure(self.text_id, text=f"ID: {self.bird_id}")
                properties_window.destroy()

        button_save = tk.Button(properties_window, text="Save", command=save_properties)
        button_save.pack()

    def delete(self):
        self.canvas.delete(self.image_id)
        self.canvas.delete(self.text_id)
        self.main_window.update_bird_counter(-1)

def add_bird(main_window):
    if main_window.bird_counter < 10:
        if main_window.bird_counter < 5:
            x = 50
            y = main_window.bird_counter * 150 + 50
        else:
            x = 200
            y = (main_window.bird_counter-5) * 150 + 50
        bird_id = str(main_window.bird_counter + 1)
        bird_image = DragDropImage(main_window.canvas, "bird.png", x, y, bird_id, main_window)
        main_window.update_bird_counter(1)

def reset_canvas(main_window):
    main_window.canvas.delete("all")
    main_window.bird_counter = 1
    main_window.image1 = DragDropImage(main_window.canvas, "bird.png", 50, 50, "1", main_window)

class MainWindow:
    def __init__(self):
        self.bird_counter = 1

        # Create the main window
        self.root = tk.Tk()
        self.root.title("Drag and Drop Images")
        self.root.geometry("1000x800")  # Set the initial window size to 1000x800 pixels

        # Create a canvas
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Adjust the canvas size to match the window size

        # Create the image objects and place them on the canvas
        self.image1 = DragDropImage(self.canvas, "bird.png", 50, 50, "1", self)

        # Add Birds button
        add_bird_button = tk.Button(self.root, text="Add Birds", command=lambda: add_bird(self))
        add_bird_button.place(x=900, y=10)

        # Reset Canvas button
        reset_button = tk.Button(self.root, text="Reset Canvas", command=lambda: reset_canvas(self))
        reset_button.place(x=900, y=40)

    def update_bird_counter(self, increment):
        self.bird_counter += increment

# Create an instance of the main window
main_window = MainWindow()

# Start the Tkinter event loop
main_window.root.mainloop()
