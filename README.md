# iNaturalist Image Downloader

iNaturalist Image Downloader is a simple GUI application that enables users to download images from a list of URLs exported from iNaturalist, specified in a CSV file. It supports progressive numbering for filenames, continues numbering from the last downloaded image, and displays mean download speed along with the estimated remaining time.

## Features

- Browse and select a CSV file containing image URLs
- Choose a directory to save the downloaded images
- Progressive numbering of filenames
- Continues numbering from the last existing image
- Displays estimated remaining download time
- Displays mean download speed
- Progress bar for visual feedback during downloads

## Requirements

- Python 3.x
- tkinter (for GUI)
- pandas (for CSV file handling)
- requests (for downloading images)

## Installation

1. Clone the repository:

   git clone https://github.com/Camponotus-vagus/iNaturalist-Image-Downloader.git

   cd iNaturalist-Image-Downloader

3. Create a virtual environment:

    python -m venv venv

4. Activate the virtual environment:

    On Windows:

    venv\Scripts\activate

    On macOS and Linux:

    source venv/bin/activate

5. Install the required packages:

    pip install -r requirements.txt

## Usage

Run the application:

python image_downloader.py

Follow the on-screen instructions to:

Browse and load a CSV file containing image URLs.
Select a directory where the images should be saved.
Click the “Download Images” button to start the download process.
The GUI will display progress, current download speed, and mean download speed throughout the process.

## CSV File Format

The CSV file should have a column named image_url containing the URLs of the images to be downloaded. For example:

image_url
https://example.com/image1.jpg
https://example.com/image2.jpg

## Screenshots

### Initial Screen
![Initial Screen](path_to_screenshot/initial_screen.png)

### Selecting CSV File
![CSV Browsing](path_to_screenshot/csv_browsing.png)

### Selecting Download Directory
![Directory Browsing](path_to_screenshot/directory_browsing.png)

### Download in Progress
![Download in Progress](path_to_screenshot/download_in_progress.png)

### Download Complete
![Download Complete](path_to_screenshot/download_complete.png)

### Sample CSV File
![Example CSV](path_to_screenshot/example_csv.png)

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any features, bug fixes, or enhancements.

## License

This project is licensed under the GNU GPLv3 License. See the LICENSE file for details.
