from PIL import Image
import numpy as np
import os
from tqdm import tqdm
from tileManager import TileManager

VALID_EXTENSIONS = {
	".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".tif",
}

def createMosaic(imgPath: str, sourceImages: str, cropSize: int, verbose: bool=False):

	image = Image.open(imgPath)
	width, height = image.size
	cropX, cropY = 0, 0  # top-left corner of the crop
	area = (cropX, cropY, cropX + cropSize, cropY + cropSize)

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

	if verbose: print("Generating Image...")

	for i in tqdm(range(0, width // cropSize), disable=not verbose):
		for j in range(0, height // cropSize):
			cropX, cropY = i * cropSize, j * cropSize
			area = (cropX, cropY, cropX + cropSize, cropY + cropSize)

			croppedImage = image.crop(area)

			arr = np.array(croppedImage)
			avg = arr.mean(axis=(0,1)).astype(int)

			bestMatch = tileManager.findClosestTile(avg)

			image.paste(bestMatch, (i*cropSize, j*cropSize))


	finalWidth = (width // cropSize) * cropSize
	finalHeight = (height // cropSize) * cropSize

	# Crop and show the result
	return image.crop((0, 0, finalWidth, finalHeight))

