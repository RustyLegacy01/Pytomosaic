# PytoMosaic

PytoMosaic is a Python library for creating photomosaics from images using a set of source images. It supports common image formats and provides a simple API with optional verbose progress output.

---

## Features

* Create photomosaics from images
* Supports `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.tiff`, `.tif` formats
* Optional `verbose` mode with progress bars using `tqdm`
* Easy-to-use Python API
* Compatible with Python 3.10+

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

```python
from pytomosaic import createMosaic

imgPath = "target.jpg"
sourceImages = "source_folder"
cropSize = 50 # Size of mosaic parts in px

# Generate mosaic with verbose progress
mosaic = createMosaic(imgPath, sourceImages, cropSize, verbose=True)
mosaic.show()
```

Set `verbose=False` or leave empty to disable prints and progress bars.

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
