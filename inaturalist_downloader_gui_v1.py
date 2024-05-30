import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import requests
import os
import threading

# Function to browse for CSV file
def browse_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filename:
        csv_file_path.set(filename)

# Function to browse for download directory
def browse_directory():
    directory = filedialog.askdirectory()
    if directory:
        download_dir.set(directory)

# Function to download images from CSV
def download_images():
    csv_path = csv_file_path.get()
    download_path = download_dir.get()

    if not csv_path or not download_path:
        messagebox.showerror("Error", "Please load a CSV file and select a download directory.")
        return

    # Read the CSV file
    try:
        data = pd.read_csv(csv_path)
        urls = data['image_url']  # Adjust the column name based on your CSV
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read the CSV file: {e}")
        return

    # If no urls are found
    if urls.empty:
        messagebox.showerror("Error", "No URLs found in the CSV file.")
        return

    # Create download directory if it doesn't exist
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # Show progress bar and download status
    progress_bar['maximum'] = len(urls)
    progress_label['text'] = f"Downloading 0/{len(urls)} images..."

    def download():
        for i, url in enumerate(urls):
            try:
                img_data = requests.get(url).content
                img_name = f"image_{i + 1}.jpg"  # Save with progressive number
                with open(os.path.join(download_path, img_name), 'wb') as handler:
                    handler.write(img_data)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download {url}: {e}")

            # Update progress
            progress_bar['value'] = i + 1
            progress_label['text'] = f"Downloading {i + 1}/{len(urls)} images..."

        # Inform the user of completion
        messagebox.showinfo("Success", "Images have been downloaded successfully.")
        progress_bar['value'] = 0
        progress_label['text'] = ""

    # Run the download function in a separate thread
    threading.Thread(target=download).start()

# Create the main window
root = tk.Tk()
root.title("Image Downloader")

csv_file_path = tk.StringVar()
download_dir = tk.StringVar()

# CSV File selection
tk.Label(root, text="CSV File:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=csv_file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_csv).grid(row=0, column=2, padx=10, pady=10)

# Download Directory selection
tk.Label(root, text="Download Directory:").grid(row=1, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=download_dir, width=50).grid(row=1, column=1, padx=10, pady=10)
tk.Button(root, text="Browse", command=browse_directory).grid(row=1, column=2, padx=10, pady=10)

# Download Button
tk.Button(root, text="Download Images", command=download_images).grid(row=2, column=0, columnspan=3, pady=20)

# Progress Bar and Label
progress_label = tk.Label(root, text="")
progress_label.grid(row=3, column=0, columnspan=3, pady=10)
progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.grid(row=4, column=0, columnspan=3, pady=10)

root.mainloop()
