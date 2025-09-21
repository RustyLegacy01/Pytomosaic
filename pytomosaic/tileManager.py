from PIL import Image
import numpy as np
import os

VALID_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif"
}

class TileManager:

	def __init__(self, cropSize: int, sourceImagesDir: str, verbose: bool = False):
		self._sourceImagesDir: str = sourceImagesDir
		self.__verbose: bool = verbose
		self._cropSize: int = cropSize
		self.tiles = []
		self.averages = []
		self.__processTiles()

	def __processTiles(self):
		if self.__verbose: print(f"Loading tiles from {self._sourceImagesDir}")

		for mosaicPart in os.listdir(self._sourceImagesDir):
			_, extension = os.path.splitext(mosaicPart)
			if extension not in VALID_EXTENSIONS:
				if self.__verbose: print(f"WARN: File extension '{extension}' is not accepted by PytoMosaic, skipped")
				continue

			mosaicPartPath = os.path.join(self._sourceImagesDir, mosaicPart)
			mosaicPartImg = Image.open(mosaicPartPath).convert('RGB').resize((self._cropSize, self._cropSize))
			arr = np.array(mosaicPartImg)
			mosaicPartProcessed = arr.mean(axis=(0,1)).astype(int)

			self.tiles.append(mosaicPartImg)
			self.averages.append(mosaicPartProcessed)
		
		self.averages = np.array(self.averages)
	
	def findClosestTile(self, target: np.ndarray):
		# Compute distances from target_color to all tile averages
		dists = np.linalg.norm(self.averages - target, axis=1)

		# Find the index of the closest tile
		best_idx = np.argmin(dists)

		# Return the corresponding tile image
		return self.tiles[best_idx]