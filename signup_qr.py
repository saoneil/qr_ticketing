import qrcode
import tkinter as tk
from tkinter import filedialog


def open_dialog():
    global url_entry, folder_path_entry

    root = tk.Tk()
    root.geometry("500x200")

    # URL input
    url_label = tk.Label(root, text="URL:")
    url_label.pack()
    url_entry = tk.Entry(root, width=60)
    url_entry.pack()

    # Folder path input
    folder_path_label = tk.Label(root, text="Folder Path:")
    folder_path_label.pack()
    folder_path_entry = tk.Entry(root, width=60)
    folder_path_entry.insert(0, "C:/Users/saone/Desktop/")
    folder_path_entry.pack()

    # Generate button
    generate_button = tk.Button(root, text="Generate QR", command=generate_qr)
    generate_button.pack(pady=(50,0))

    root.mainloop()
def generate_qr():
    url = url_entry.get()
    folder_path = folder_path_entry.get()

    folder_path += "/signup_qr.png"

    if url and folder_path:
        qr = qrcode.QRCode(
          version=1,
          error_correction=qrcode.constants.ERROR_CORRECT_L,
          box_size=10,
          border=4,
          )
        
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img.save(folder_path)

        print(f"Generating QR for URL: {url}")
        print(f"Saving QR in folder: {folder_path}")
    else:
        print("URL or folder path is missing.")


open_dialog()