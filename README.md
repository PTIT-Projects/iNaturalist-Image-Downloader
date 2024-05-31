# iNaturalist Image Downloader

iNaturalist Image Downloader is a simple, open-source, GUI application that enables users to download images from a list of URLs exported from iNaturalist, specified in a CSV file. It supports progressive numbering for filenames, continues numbering from the last downloaded image, and displays mean download speed along with the estimated remaining time.

## Features

- Browse and select a CSV file containing image URLs.
- Choose a directory to save the downloaded images.
- Progressive numbering of filenames.
- Continues numbering from the last existing image.
- Displays estimated remaining download time.
- Displays mean download speed.
- Progress bar for visual feedback during downloads.

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

1. Browse and load a CSV file containing image URLs.
2. Select a directory where the images should be saved.
3. Click the “Download Images” button to start the download process.

The GUI will display progress, current download speed, and mean download speed throughout the process.

## CSV File Format

The CSV file should have a column named `image_url` containing the URLs of the images to be downloaded. To export this list from [iNaturalist](https://www.inaturalist.org/observations/export), follow these steps:

1. Go to the [iNaturalist Observations Export](https://www.inaturalist.org/observations/export) page.
2. In Step 1, select the type of observations you want to export (e.g., "Formicidae").
3. In Step 3, de-select all columns except for `image_url`.
4. Scroll to the bottom of the page and click the "Create Export" button.
5. Wait for the export process to complete (this may take a few seconds to minutes, depending on the amount of data). Once finished, a download link for the CSV file will appear.

Download the CSV file, and it will be ready for use with the Image Downloader!

## Screenshots

### Initial Screen
<img width="846" alt="Screenshot 2024-05-31 alle 11 12 58" src="https://github.com/Camponotus-vagus/iNaturalist-Image-Downloader/assets/114755488/b69c2fb8-5b69-4173-8de4-e3c55745c9ed">

### Download in Progress
<img width="846" alt="Screenshot 2024-05-31 alle 11 22 20" src="https://github.com/Camponotus-vagus/iNaturalist-Image-Downloader/assets/114755488/cb00a566-c13c-4ecb-b487-746243b20657">

### Download Complete
<img width="730" alt="Screenshot 2024-05-31 alle 11 35 35" src="https://github.com/Camponotus-vagus/iNaturalist-Image-Downloader/assets/114755488/1b7844a0-c81a-4637-9f51-399f6b8b29e8">

### Sample CSV File
<img width="1195" alt="Screenshot 2024-05-30 alle 18 55 36" src="https://github.com/Camponotus-vagus/iNaturalist-Image-Downloader/assets/114755488/6416cecc-b4d2-4348-a4e0-aa46e50da055">

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any features, bug fixes, or enhancements.

## License

This project is licensed under the GNU GPLv3 License. See the LICENSE file for details.

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=Camponotus-vagus/iNaturalist-Image-Downloader&type=Date)](https://star-history.com/#Camponotus-vagus/iNaturalist-Image-Downloader&Date)
