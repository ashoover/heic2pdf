import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF opener with Pillow
register_heif_opener()

def heic_to_pdf(heic_file):
    """Convert a HEIC file to PDF and save in the same directory."""
    try:
        # Open the HEIC image using Pillow
        image = Image.open(heic_file)

        # Convert the image to RGB mode if it's not already
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Get the directory of the HEIC file
        dir_path = os.path.dirname(heic_file)
        base_name = os.path.basename(heic_file).replace('.heic', '.pdf')
        pdf_file = os.path.join(dir_path, base_name)

        # Save as PDF
        image.save(pdf_file, 'PDF', resolution=100.0)

        return pdf_file

    except Exception as e:
        messagebox.showerror("Error", f"Failed to convert {heic_file}: {str(e)}")
        return None

def select_file():
    """Open file dialog to select a HEIC file."""
    heic_file = filedialog.askopenfilename(
        title="Select HEIC File",
        filetypes=[("HEIC files", "*.heic")]
    )
    if heic_file:
        entry_var.set(heic_file)

def on_drop(event):
    """Handle file drop event."""
    heic_file = event.data
    if heic_file.lower().endswith('.heic'):
        entry_var.set(heic_file)

def convert():
    """Convert the selected HEIC file to PDF."""
    heic_file = entry_var.get()
    if not heic_file or not os.path.isfile(heic_file):
        messagebox.showwarning("Warning", "Please select a valid HEIC file.")
        return

    pdf_file = heic_to_pdf(heic_file)
    if pdf_file:
        messagebox.showinfo("Success", f"Converted to {pdf_file}")

def create_gui():
    """Create the Tkinter GUI."""
    root = tk.Tk()
    root.title("HEIC to PDF Converter")

    # Create and place widgets
    frame = tk.Frame(root, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="Select HEIC file:")
    label.grid(row=0, column=0, sticky="w")

    global entry_var
    entry_var = tk.StringVar()
    entry = tk.Entry(frame, width=50, textvariable=entry_var)
    entry.grid(row=0, column=1)

    browse_button = tk.Button(frame, text="Browse...", command=select_file)
    browse_button.grid(row=0, column=2, padx=5)

    convert_button = tk.Button(frame, text="Convert", command=convert)
    convert_button.grid(row=1, columnspan=3, pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_gui()