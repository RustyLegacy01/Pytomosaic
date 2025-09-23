from PIL import Image
import numpy as np
from tqdm import tqdm
from pytomosaic.tileManager import TileManager


VALID_EXTENSIONS = {
	".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".tif",
}

def createMosaic(imgPath: str, sourceImages: str | TileManager, cropSize: int = None, verbose: bool=False, savePath: str = None):

	if verbose: print("Processing Images...")

	# Skip any files that are not images
	if isinstance(sourceImages, TileManager):
		tileManager = sourceImages
		cropSize = tileManager._cropSize
	else:
		tileManager = TileManager(
			cropSize=cropSize,                 # size of each tile
			sourceImagesDir=sourceImages,    # folder with your source images
			verbose=verbose                 # show loading messages
		)

	image = Image.open(imgPath)
	width, height = image.size
	cropX, cropY = 0, 0  # top-left corner of the crop
	area = (cropX, cropY, cropX + cropSize, cropY + cropSize)

	if verbose: print("Generating Image...")

	for i in tqdm(range(0, width // cropSize), disable=not verbose):
		for j in range(0, height // cropSize):
			cropX, cropY = i * cropSize, j * cropSize
			area = (cropX, cropY, cropX + cropSize, cropY + cropSize)

			croppedImage = image.crop(area).convert("RGB")

			arr = np.array(croppedImage)
			avg = arr.mean(axis=(0,1)).astype(int)

			bestMatch = tileManager.findClosestTile(avg)

			image.paste(bestMatch, (i*cropSize, j*cropSize))

	if verbose: print("Generation Complete.")

	finalWidth = (width // cropSize) * cropSize
	finalHeight = (height // cropSize) * cropSize

	if savePath:
		if verbose: print(f"Saving image to {savePath}")
		image.save(savePath)

	# Crop and show the result
	return image.crop((0, 0, finalWidth, finalHeight))

