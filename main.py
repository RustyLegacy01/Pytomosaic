from PIL import Image
import numpy as np
import os
from tqdm import tqdm

imgName = str(input("Name of image (with extension): "))
cropSize = int(input("Crop size: "))

image = Image.open(f"images/conversion-images/{imgName}")
partsDirectory = ("images/mosaic-parts/")
width, height = image.size

cropX, cropY = 0, 0  # top-left corner of the crop
area = (cropX, cropY, cropX + cropSize, cropY + cropSize)

print("Processing Images...")

mosaicParts = []

for mosaicPart in os.listdir(partsDirectory):
	if mosaicPart == "criteria":
		continue
	
	mosaicPartPath = f'{partsDirectory}/{mosaicPart}'
	mosaicPartImg = Image.open(mosaicPartPath).convert('RGB').resize((cropSize, cropSize))
	arr = np.array(mosaicPartImg)
	mosaicPartProcessed = arr.mean(axis=(0,1)).astype(int)

	mosaicParts.append([mosaicPartImg, mosaicPartProcessed])

mosaicAverages = np.array([part[1] for part in mosaicParts])

print("Generating Image...")

for i in tqdm(range(0, width // cropSize)):
	for j in range(0, height // cropSize):
		cropX, cropY = i * cropSize, j * cropSize
		area = (cropX, cropY, cropX + cropSize, cropY + cropSize)

		croppedImage = image.crop(area)

		arr = np.array(croppedImage)
		avg = arr.mean(axis=(0,1)).astype(int)

		# Find the most similar mosaic part
		minDist = float('inf')
		bestMatchPath = None

		# Vectorized distance calculation
		dists = np.linalg.norm(mosaicAverages - avg, axis=1)
		bestIdx = np.argmin(dists)
		bestMatch = mosaicParts[bestIdx][0]

		image.paste(bestMatch, (i*cropSize, j*cropSize))


finalWidth = (width // cropSize) * cropSize
finalHeight = (height // cropSize) * cropSize

# Crop and show the result
image.crop((0, 0, finalWidth, finalHeight)).show()

