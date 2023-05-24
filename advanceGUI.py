import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk

class BirdInterface:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Interfaz de Pájaros")
        self.window.geometry("800x600")
        self.bird_images = []
        self.num_birds = 0
        self.num_birds_entry = None

        self.canvas = tk.Canvas(self.window, bg="white")
        self.canvas.pack(expand=True, fill=tk.BOTH)

        self.num_birds_entry = tk.Entry(self.window)
        self.num_birds_entry.pack()
        self.num_birds_entry.bind("<Return>", self.update_num_birds)

        button_frame = tk.Frame(self.window)
        button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        add_button = tk.Button(button_frame, text="+", command=self.add_bird)
        add_button.pack(side=tk.LEFT)

        remove_button = tk.Button(button_frame, text="-", command=self.remove_bird)
        remove_button.pack(side=tk.LEFT)

        remove_all_button = tk.Button(button_frame, text="Eliminar todo", command=self.remove_all_birds)
        remove_all_button.pack(side=tk.LEFT)

        self.update_bird_count()

        self.canvas.bind("<Configure>", self.on_canvas_resize)
        self.canvas.bind("<Double-Button-1>", self.open_image_properties_menu)

        self.window.mainloop()

    def add_bird(self):
        self.num_birds += 1
        self.update_bird_count()

    def remove_bird(self):
        if self.num_birds > 0:
            self.num_birds -= 1
            self.update_bird_count()

            # Eliminar la última imagen agregada del canvas y la lista de imágenes
            image_label, bird_image = self.bird_images.pop()
            image_label.destroy()

    def remove_all_birds(self):
        self.num_birds = 0
        self.update_bird_count()

    def update_bird_count(self):
        self.num_birds_entry.delete(0, tk.END)
        self.num_birds_entry.insert(0, str(self.num_birds))

        self.canvas.delete("all")

        margin = 50
        bird_size = 100
        canvas_width = self.canvas.winfo_width()
        max_birds_per_row = (canvas_width - margin) // (bird_size + margin)
        row = 0
        col = 0

        for i in range(self.num_birds):
            x = margin + col * (bird_size + margin)
            y = margin + row * (bird_size + margin)

            bird_image = Image.open("bird.png")  # Ruta de la imagen del pájaro
            bird_image = bird_image.resize((bird_size, bird_size), Image.ANTIALIAS)
            bird_image = ImageTk.PhotoImage(bird_image)

            # Crear una etiqueta para la imagen con un identificador único
            image_label = tk.Label(self.canvas, image=bird_image)
            image_label.image = bird_image  # Mantener una referencia para evitar que la imagen sea eliminada por la recolección de basura
            image_label.place(x=x, y=y)

            # Configurar el menú contextual para la imagen
            image_menu = tk.Menu(self.canvas, tearoff=False)
            image_menu.add_command(label="Propiedades", command=lambda label=image_label: self.open_properties_dialog(label))
            image_menu.add_command(label="Eliminar", command=lambda label=image_label: self.delete_image(label))

            # Asociar el menú contextual a la imagen mediante el evento <Button-3>
            image_label.bind("<Button-3>", lambda event, menu=image_menu: self.show_context_menu(event, menu))

            self.bird_images.append((image_label, bird_image))

            col += 1
            if col >= max_birds_per_row:
                col = 0
                row += 1

    def on_canvas_resize(self, event):
        self.update_bird_count()

    def update_num_birds(self, event):
        try:
            new_num_birds = int(self.num_birds_entry.get())
            if new_num_birds >= 0:
                self.num_birds = new_num_birds
                self.update_bird_count()
            else:
                messagebox.showerror("Error", "El número de pájaros debe ser mayor o igual a cero.")
        except ValueError:
            messagebox.showerror("Error", "El número de pájaros debe ser un valor numérico.")

    def show_context_menu(self, event, menu):
        menu.post(event.x_root, event.y_root)

    def open_properties_dialog(self, label):
        bird_name = simpledialog.askstring("Propiedades", "Ingrese el nombre de la imagen:")
        if bird_name:
            for image_label, _ in self.bird_images:
                if image_label != label and image_label.cget("text") == bird_name:
                    messagebox.showerror("Error", "Ya existe una imagen con ese nombre.")
                    return

            label.config(text=bird_name)

    def delete_image(self, label):
        for i, (image_label, bird_image) in enumerate(self.bird_images):
            if image_label == label:
                image_label.destroy()
                del self.bird_images[i]
                break

    def open_image_properties_menu(self, event):
        x, y = event.x, event.y
        overlapping_labels = self.canvas.find_overlapping(x, y, x, y)
        if overlapping_labels:
            label_id = overlapping_labels[-1]
            for image_label, _ in self.bird_images:
                if image_label.winfo_id() == label_id:
                    self.open_properties_dialog(image_label)
                    break

if __name__ == "__main__":
    interface = BirdInterface()
