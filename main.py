import requests
import os
import json
from tqdm import tqdm

# main 
def main(json_file, base_path):
    # Load the JSON file
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        print(f"Error: JSON file '{json_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file '{json_file}'.")
        return

    models = data.get('models', [])

    # Check if the base path is a valid directory
    if not os.path.isdir(base_path):
        print(f"Error: Invalid base path '{base_path}'.")
        return

    for model in models:
        url = model.get('url')
        save_path = os.path.join(base_path, model.get('save_path', ''), model.get('filename', ''))

        # Check if the file already exists
        if os.path.exists(save_path):
            print(f"{model.get('filename', '')} already exists, skipping download.")
            continue

        # Make the directory if it does not exist
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        description = model.get('description', '')
        print("Downloading " + description)
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 Kibibyte
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open(save_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
            if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
                print(f"ERROR, something went wrong in downloading {model.get('name', '')}")
            else:
                print(f"Downloaded {model.get('name', '')} to {save_path}")
        else:
            print(f"Failed to download {model.get('name', '')} from {url}")

    print("All downloads attempted.")

if __name__ == "__main__":
    main('picked-models.json', 'models')