import tkinter as tk
from PIL import ImageTk, Image

class DragDropImage:
    def __init__(self, canvas, image_path, x, y):
        self.canvas = canvas
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

    def start_drag(self, event):
        self.is_dragging = True
        self.offset_x = event.x - self.canvas.coords(self.image_id)[0]
        self.offset_y = event.y - self.canvas.coords(self.image_id)[1]

    def drag(self, event):
        if self.is_dragging:
            x = event.x - self.offset_x
            y = event.y - self.offset_y
            self.canvas.coords(self.image_id, x, y)

    def drop(self, event):
        if self.is_dragging:
            self.is_dragging = False
            x = event.x - self.offset_x
            y = event.y - self.offset_y
            self.animate_drop(x, y)

    def animate_drop(self, x, y):
        dx = x - self.canvas.coords(self.image_id)[0]
        dy = y - self.canvas.coords(self.image_id)[1]
        step = 5
        delay = 10
        for i in range(step):
            self.canvas.after(delay * i, lambda: self.move_image(dx/step, dy/step))
        self.canvas.after(delay * step, lambda: self.move_image(dx - (dx/step)*step, dy - (dy/step)*step))

    def move_image(self, dx, dy):
        self.canvas.move(self.image_id, dx, dy)

    def open_menu(self, event):
        menu = tk.Menu(self.canvas, tearoff=0)
        menu.add_command(label="Properties", command=self.properties)
        menu.add_command(label="Delete", command=self.delete)
        menu.post(event.x_root, event.y_root)

    def properties(self):
        # Code to handle the "Properties" option
        pass

    def delete(self):
        self.canvas.delete(self.image_id)

# Create the main window
root = tk.Tk()
root.title("Drag and Drop Images")
root.geometry("400x400")

# Create a canvas
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Create the image objects and place them on the canvas
image1 = DragDropImage(canvas, "bird.png", 50, 50)
image2 = DragDropImage(canvas, "bird.png", 150, 150)
image3 = DragDropImage(canvas, "bird.png", 250, 250)

# Start the Tkinter event loop
root.mainloop()
