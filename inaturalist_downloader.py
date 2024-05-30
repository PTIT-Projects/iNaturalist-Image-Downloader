import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import requests
import os
import re
import threading
import time

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

    # Get the starting number for images
    existing_images = os.listdir(download_path)
    max_num = 0
    for img in existing_images:
        match = re.search(r'image_(\d+)\.jpg', img)
        if match:
            num = int(match.group(1))
            if num > max_num:
                max_num = num
    starting_num = max_num + 1

    # Show progress bar and download status
    progress_bar['maximum'] = len(urls)
    progress_label['text'] = f"Downloading 0/{len(urls)} images..."
    remaining_time_label['text'] = "Remaining time: estimating..."
    mean_speed_label['text'] = "Mean speed: 0 Mbit/s"

    def download():
        total_size = 0
        total_time = 0
        start_time = time.time()

        for i, url in enumerate(urls, start=starting_num):
            try:
                download_start_time = time.time()
                img_data = requests.get(url).content
                elapsed_time = time.time() - download_start_time

                # Update total size and time for mean speed calculation
                total_size += len(img_data)
                total_time += elapsed_time

                # Calculate mean speed in Mbit/s
                mean_speed = (total_size * 8) / (total_time * 1_000_000) if total_time > 0 else 0
                mean_speed_label['text'] = f"Mean speed: {mean_speed:.2f} Mbit/s"

                img_name = f"image_{i}.jpg"  # Save with progressive number
                with open(os.path.join(download_path, img_name), 'wb') as handler:
                    handler.write(img_data)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to download {url}: {e}")

            # Update progress
            progress_bar['value'] = i - starting_num + 1
            progress_label['text'] = f"Downloading {i - starting_num + 1}/{len(urls)} images..."

            # Estimate remaining time
            current_time = time.time()
            elapsed_total_time = current_time - start_time
            if i - starting_num + 1 > 0:
                avg_time_per_image = elapsed_total_time / (i - starting_num + 1)
                remaining_time = avg_time_per_image * (len(urls) - (i - starting_num + 1))
                remaining_time_label['text'] = f"Remaining time: {remaining_time:.2f}s"
            else:
                remaining_time_label['text'] = "Remaining time: estimating..."

        # Inform the user of completion
        messagebox.showinfo("Success", "Images have been downloaded successfully.")
        progress_bar['value'] = 0
        progress_label['text'] = ""
        remaining_time_label['text'] = ""
        mean_speed_label['text'] = ""

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

# Progress Bar and Labels
progress_label = tk.Label(root, text="")
progress_label.grid(row=3, column=0, columnspan=3, pady=10)
progress_bar = ttk.Progressbar(root, orient='horizontal', length=400, mode='determinate')
progress_bar.grid(row=4, column=0, columnspan=3, pady=10)

remaining_time_label = tk.Label(root, text="")
remaining_time_label.grid(row=5, column=0, columnspan=3, pady=10)

mean_speed_label = tk.Label(root, text="")
mean_speed_label.grid(row=6, column=0, columnspan=3, pady=10)

root.mainloop()
