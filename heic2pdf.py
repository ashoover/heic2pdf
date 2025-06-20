import os
import tkinter as tk
from tkinter import filedialog, messagebox, Listbox, StringVar, END
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF opener with Pillow
register_heif_opener()

def load_files():
    """Load all .heic files from the selected directory."""
    global heic_directory
    heic_directory = filedialog.askdirectory(title="Select Directory")
    if not heic_directory:
        return

    heic_files = [f for f in os.listdir(heic_directory) if f.lower().endswith('.heic')]
    listbox.delete(0, END)
    for file in heic_files:
        listbox.insert(END, file)

def convert_selected_files():
    """Convert the selected files to PDF or JPEG."""
    selected_files = [listbox.get(i) for i in listbox.curselection()]
    if not selected_files:
        messagebox.showwarning("Warning", "Please select at least one file.")
        return

    output_format = format_var.get()

    for filename in selected_files:
        try:
            # Open the HEIC image using Pillow
            heic_path = os.path.join(heic_directory, filename)
            with Image.open(heic_path) as image:
                if output_format == "PDF":
                    pdf_filename = filename.replace('.heic', '.pdf')
                    pdf_path = os.path.join(heic_directory, pdf_filename)
                    image.save(pdf_path, 'PDF', resolution=100.0)

                elif output_format == "JPEG":
                    jpeg_filename = filename.replace('.heic', '.jpeg')
                    jpeg_path = os.path.join(heic_directory, jpeg_filename)
                    if image.mode != 'RGB':
                        image = image.convert('RGB')
                    image.save(jpeg_path, 'JPEG')

                messagebox.showinfo("Success", f"Converted {filename} to {output_format.lower()}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert {filename}: {e}")

def create_gui():
    """Create the Tkinter GUI."""
    global listbox, format_var

    root = tk.Tk()
    root.title("HEIC Converter")

    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    load_button = tk.Button(frame, text="Load HEIC Files", command=load_files)
    load_button.grid(row=0, columnspan=3, pady=(0, 10))

    listbox = Listbox(frame, width=50, height=15, selectmode=tk.MULTIPLE)
    listbox.grid(row=1, columnspan=3, pady=(0, 10))

    format_var = StringVar()
    format_var.set("PDF")
    format_label = tk.Label(frame, text="Convert to:")
    format_label.grid(row=2, column=0, sticky="w")

    format_menu = tk.OptionMenu(frame, format_var, "PDF", "JPEG")
    format_menu.grid(row=2, column=1, padx=(5, 0))

    convert_button = tk.Button(frame, text="Convert Selected Files", command=convert_selected_files)
    convert_button.grid(row=3, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()