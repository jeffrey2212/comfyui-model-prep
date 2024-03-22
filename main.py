import requests
import os
import json
from tqdm import tqdm
from huggingface_hub import hf_hub_download

# Load the JSON file
with open('picked-models.json', 'r') as file:
    data = json.load(file)

models = data['models']

# Base path where all models will be downloaded
base_path = "/path/to/your/directory"

for model in models:
    url = model['url']
    save_path = os.path.join(base_path, model['save_path'], model['filename'])

    # Check if the file already exists
    if os.path.exists(save_path):
        print(f"{model['filename']} already exists, skipping download.")
        continue

    # Make the directory if it does not exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Download the model with a progress bar
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes,
                            unit='iB', unit_scale=True)
        with open(save_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print(f"ERROR, something went wrong in downloading {
                  model['name']}")
        else:
            print(f"Downloaded {model['name']} to {save_path}")
    else:
        print(f"Failed to download {model['name']} from {url}")

print("All downloads attempted.")
