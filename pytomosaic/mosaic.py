from PIL import Image
import numpy as np
import os
from tqdm import tqdm

VALID_EXTENSIONS = {
	".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
    ".tiff",
    ".tif",
}

def createMosaic(imgPath, sourceImages, cropSize, verbose=False):

	image = Image.open(imgPath)
	width, height = image.size
	cropX, cropY = 0, 0  # top-left corner of the crop
	area = (cropX, cropY, cropX + cropSize, cropY + cropSize)

	if verbose: print("Processing Images...")

	mosaicParts = []

	# Skip any files that are not images
	for mosaicPart in os.listdir(sourceImages):
		_, extension = os.path.splitext(mosaicPart)
		if extension not in VALID_EXTENSIONS:
			if verbose: print(f"WARN: File extension '{extension}' is not accepted by PytoMosaic, skipped")
			continue
		
		mosaicPartPath = f'{sourceImages}/{mosaicPart}'
		mosaicPartImg = Image.open(mosaicPartPath).convert('RGB').resize((cropSize, cropSize))
		arr = np.array(mosaicPartImg)
		mosaicPartProcessed = arr.mean(axis=(0,1)).astype(int)

		mosaicParts.append([mosaicPartImg, mosaicPartProcessed])

	mosaicAverages = np.array([part[1] for part in mosaicParts])

	if verbose: print("Generating Image...")

	for i in tqdm(range(0, width // cropSize), disable=not verbose):
		for j in range(0, height // cropSize):
			cropX, cropY = i * cropSize, j * cropSize
			area = (cropX, cropY, cropX + cropSize, cropY + cropSize)

			croppedImage = image.crop(area)

			arr = np.array(croppedImage)
			avg = arr.mean(axis=(0,1)).astype(int)

			# Vectorized distance calculation
			dists = np.linalg.norm(mosaicAverages - avg, axis=1)
			bestIdx = np.argmin(dists)
			bestMatch = mosaicParts[bestIdx][0]

			image.paste(bestMatch, (i*cropSize, j*cropSize))


	finalWidth = (width // cropSize) * cropSize
	finalHeight = (height // cropSize) * cropSize

	# Crop and show the result
	return image.crop((0, 0, finalWidth, finalHeight))

