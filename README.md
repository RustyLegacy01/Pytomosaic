# PytoMosaic

PytoMosaic is a Python library for creating photomosaics from images using a set of source images. It supports common image formats and provides a simple API with optional verbose progress output. It also allows reusing preloaded tiles for faster mosaic generation across multiple images.

---

## Features

* Create photomosaics from images
* Supports `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.tif` formats
* Optional `verbose` mode with progress bars using `tqdm`
* Reuse preloaded tiles with `TileManager` for multiple mosaics
* Easy-to-use Python API
* Compatible with Python 3.10+
* Ability to save files
* Image downloader for fast downloads

---

## Installation

Install PytoMosaic from PyPI:

```bash
pip install pytomosaic
```

Dependencies:

* `numpy`
* `Pillow`
* `tqdm`

These will be installed automatically.

---

## Usage

### Basic usage

```python
from pytomosaic import createMosaic

imgPath = "target.jpg"
sourceImages = "source_folder"
cropSize = 50  # Size of mosaic parts in px

# Generate mosaic with verbose progress
mosaic = createMosaic(imgPath, sourceImages, cropSize, verbose=True, savePath="example.jpg")
mosaic.show()
```

### Reusing preloaded tiles for multiple images

```python
from pytomosaic import createMosaic
from pytomosaic.tileManager import TileManager

# Preload tiles once
tiles = TileManager(cropSize=50, sourceImagesDir="source_folder", verbose=True)

# Generate multiple mosaics using the same tiles
mosaic1 = createMosaic("photo1.jpg", tiles)
mosaic2 = createMosaic("photo2.jpg", tiles)
```

Set `verbose=False` or leave empty to disable prints and progress bars.

### Downloading images from Pixabay

```python
from pytomosaic import downloadImages

key = "YOUR_API_KEY" # Get from Pixabay
amount = 200 # 200 Maximum due to Pixabay restriction
query = "Your Query" # What you want the pictures to be of
pathToDownloadTo = "path/to/download/to"

downloadImages(key, amount, query, pathToDownloadTo, verbose=True)
```

---

## Examples

![Example Mosaic 1](docs/747-3.jpg)

> **Note:** These files are stored in the GitHub repo for demonstration purposes. Users installing PytoMosaic via PyPI do not automatically download these images.

---

## Supported Image Extensions

```python
VALID_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif"
}
```

Files with unsupported extensions are skipped and optionally warned about in verbose mode.

---

## License

PytoMosaic is licensed under the **GNU GPL v3**. See the [LICENSE](LICENSE) file for details.
