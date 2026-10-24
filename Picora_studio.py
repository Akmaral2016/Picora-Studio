import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
from PIL import Image, ImageTk, ImageOps, ImageEnhance
import shutil
LIBRARY = Path.home() / "PicoraStudio" / "images"
LIBRARY.mkdir(parents=True, exist_ok=True)
class Picora:
    def __init__(self, root):
        self.root = root
        root.title("Picora Studio ♡")
        root.geometry("800x600")
        root.configure(bg="#FFF0F7")
        self.image = None
        self.path = None
        self.photo = None
        tk.Label(root, text="♡ Picora Studio", font=("Arial", 22, "bold"),
                 bg="#FFF0F7", fg="#C94F91").pack(pady=12)
        tk.Button(root, text="Upload Image", command=self.upload,
                  bg="#E879B9", fg="white").pack(pady=5)
        self.preview = tk.Label(root, text="Choose an image ♡",
                                bg="white", width=60, height=18)
        self.preview.pack(padx=15, pady=10, fill="both", expand=True)
        bar = tk.Frame(root, bg="#FFF0F7")
        bar.pack(pady=8)
        for label, action in [
            ("Rotate", self.rotate), ("Flip", self.flip),
            ("Grayscale", self.gray), ("Sepia", self.sepia),
            ("Reset", self.reset), ("Save Copy", self.save)
        ]:
            tk.Button(bar, text=label, command=action,
                      bg="white", fg="#C94F91").pack(side="left", padx=3)
    def upload(self):
        name = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.webp *.bmp")])
        if not name:
            return
        try:
            source = Path(name)
            target = LIBRARY / source.name
            i = 2
            while target.exists():
                target = LIBRARY / f"{source.stem}_{i}{source.suffix}"
                i += 1
            shutil.copy2(source, target)
            self.path = target
            self.image = Image.open(target).convert("RGB")
            self.show()
        except Exception as error:
            messagebox.showerror("Upload failed", str(error))
    def show(self):
        if self.image is None:
            return
        image = self.image.copy()
        image.thumbnail((700, 400))
        self.photo = ImageTk.PhotoImage(image)
        self.preview.config(image=self.photo, text="")
    def rotate(self):
        if self.image:
            self.image = self.image.rotate(90, expand=True)
            self.show()
    def flip(self):
        if self.image:
            self.image = ImageOps.mirror(self.image)
            self.show()
    def gray(self):
        if self.image:
            self.image = ImageOps.grayscale(self.image).convert("RGB")
            self.show()
    def sepia(self):
        if self.image:
            self.image = ImageOps.colorize(ImageOps.grayscale(self.image),
                                           "#3B2525", "#F6D7B0").convert("RGB")
            self.show()
    def reset(self):
        if self.path and self.path.exists():
            self.image = Image.open(self.path).convert("RGB")
            self.show()
    def save(self):
        if self.image is None:
            messagebox.showinfo("Picora", "Upload an image first ♡")
            return
        name = filedialog.asksaveasfilename(defaultextension=".png",
                                             filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg")])
        if name:
            try:
                self.image.save(name)
                messagebox.showinfo("Saved", "Your image was saved ♡")
            except Exception as error:
                messagebox.showerror("Save failed", str(error))
if __name__ == "__main__":
    root = tk.Tk()
    Picora(root)
    root.mainloop()
