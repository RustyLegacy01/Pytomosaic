import requests
from PIL import Image
import os
from io import BytesIO
from tqdm import tqdm

def downloadImages(key: str, amount: int, query: str, downloadPath: str, verbose: bool=False):

    if amount > 200:
        raise Exception("PytoMosaic - Can not download more than 200 images, aborting download")
    
    # Replace all space with + for request formatting
    if " " in query:
        for i in range(0, len(query)-1):
            if query[i] == " ":
                query[i] == "+"

    if verbose: print("Requesting Image List...")
    r = requests.get(f"https://pixabay.com/api/?key={key}&q={query}&image_type=photo&per_page={amount}")
    data = r.json()

    count = 0

    if verbose: print("Downloading Images...")

    for i in tqdm(range(0, len(data["hits"])-1), disable=not verbose):
        imageURL = data["hits"][count]["webformatURL"] # Link to Image
        imageData = requests.get(imageURL).content # Image itself
        img = Image.open(BytesIO(imageData)).convert("RGB") # Open with PIL
        img.save(os.path.join(downloadPath, f"{query}_{count}.jpg"))

        count += 1
    
    if verbose: print(f"Finished downloading {amount} images to {downloadPath}.")
