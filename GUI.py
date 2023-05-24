import tkinter as tk

class ImageObject:
    def __init__(self, canvas, image, x, y):
        self.canvas = canvas
        self.image = image
        self.x = x
        self.y = y
        self.canvas_id = canvas.create_image(x, y, image=self.image)
        self.canvas.tag_bind(self.canvas_id, "<Button1-Motion>", self.move)

    def move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        self.canvas.move(self.canvas_id, dx, dy)
        self.x = event.x
        self.y = event.y

def center_images(event):
    canvas_width = event.width
    canvas_height = event.height

    # Calculate center coordinates
    center_x = canvas_width // 2
    center_y = canvas_height // 2

    # Move images to center
    canvas.coords(image_object.canvas_id, center_x, center_y)
    canvas.coords(image_object2.canvas_id, center_x, center_y)
    canvas.coords(image_object3.canvas_id, center_x, center_y)

root = tk.Tk()
root.title("Image Movement")

canvas = tk.Canvas(root)
canvas.pack(fill=tk.BOTH, expand=True)  # Fill the window and expand to fit

# Load different images
image1 = tk.PhotoImage(file="bird.png")
image2 = tk.PhotoImage(file="bird.png")
image3 = tk.PhotoImage(file="bird.png")

# Create image objects
image_object = ImageObject(canvas, image1, 100, 100)
image_object2 = ImageObject(canvas, image2, 200, 200)
image_object3 = ImageObject(canvas, image3, 300, 300)

# Bind window resize event to center_images function
root.bind("<Configure>", center_images)

root.mainloop()
