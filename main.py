from PIL import Image
import numpy as np
import os
from tqdm import tqdm

image = Image.open("images/conversion-images/obama.jpg")
width, height = image.size

cropSize = 32
cropX, cropY = 0, 0  # top-left corner of the crop
area = (cropX, cropY, cropX + cropSize, cropY + cropSize)

directory = ("images/mosaic-parts/frog")
mosaicParts = []

print("Generating Image...")

for mosaicPart in os.listdir(directory):

	mosaicPartPath = f'{directory}/{mosaicPart}'
	mosaicPartImg = Image.open(mosaicPartPath)
	arr = np.array(mosaicPartImg)
	mosaicPartProcessed = arr.mean(axis=(0,1)).astype(int)

	mosaicParts.append([mosaicPartPath, mosaicPartProcessed])


for i in tqdm(range(0, width // 32)):
	for j in range(0, height // 32):
		cropX, cropY = i * 32, j * 32
		area = (cropX, cropY, cropX + cropSize, cropY + cropSize)

		croppedImage = image.crop(area)

		arr = np.array(croppedImage)
		avg = arr.mean(axis=(0,1)).astype(int)

		# Find the most similar mosaic part
		minDist = float('inf')
		bestMatchPath = None

		for partPath, partAvg in mosaicParts:
			dist = np.linalg.norm(avg - partAvg)
			if dist < minDist:
				minDist = dist
				bestMatchPath = partPath

		# print(f"Best match for region ({i}, {j}): {bestMatchPath}")

		image.paste(Image.open(bestMatchPath), (i*32, j*32))


finalWidth = (width // 32) * 32
finalHeight = (height // 32) * 32

# Crop and show the result
image.crop((0, 0, finalWidth, finalHeight)).show()

