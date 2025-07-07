import asyncio
from random import randint
from PIL import Image
import requests
from pathlib import Path
import os
from time import sleep
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Hugging Face token from environment variable
HUGGING_API_KEY = os.getenv("HuggingFaceAPIKey")

# Get paths
current_path = Path(__file__).resolve()
root_path = current_path.parents[1]  # ELI.AI folder
data_file_path = root_path / "Frontend" / "Files" / "ImageGeneration.data"
image_save_folder = root_path / "Data"

# Create image folder if it doesn't exist
image_save_folder.mkdir(parents=True, exist_ok=True)

# Setup API headers
headers = {
    "Authorization": f"Bearer {HUGGING_API_KEY}"
}
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"

# Function to open generated images
def open_images(prompt):
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    
    for jpg_file in files:
        image_path = image_save_folder / jpg_file
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")
            img.show()
            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

# Async request to Hugging Face
async def query(payload):
    try:
        response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type", "")
            if "image" in content_type:
                return response.content
            else:
                print("Response is not an image")
                print("Response text:", response.text[:200])  # First 200 chars
                return None
        else:
            print(f"API Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"Request error: {e}")
        return None

# Generate 4 images asynchronously
async def generate_images(prompt: str):
    print(f"Starting image generation for prompt: '{prompt}'")
    tasks = []
    
    for i in range(4):
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness=maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}"
        }
        tasks.append(asyncio.create_task(query(payload)))
    
    print("Waiting for API responses...")
    image_bytes_list = await asyncio.gather(*tasks)
    
    saved_count = 0
    for i, image_bytes in enumerate(image_bytes_list):
        if image_bytes is None:
            print(f"Failed to generate image {i + 1}")
            continue
            
        image_file = image_save_folder / f"{prompt.replace(' ', '_')}{i + 1}.jpg"
        try:
            with open(image_file, "wb") as f:
                f.write(image_bytes)
            print(f"Saved image {i + 1}: {image_file}")
            saved_count += 1
        except Exception as e:
            print(f"Error saving image {i + 1}: {e}")
    
    print(f"Successfully generated and saved {saved_count} images")
    return saved_count > 0

# Main image generation wrapper
def GenerateImage(prompt: str):
    success = asyncio.run(generate_images(prompt))
    if success:
        open_images(prompt)
    else:
        print("No images were generated successfully")

# File watcher loop
def main():
    print("Starting image generation service...")
    print(f"Watching file: {data_file_path}")
    print(f"Images will be saved to: {image_save_folder}")
    
    while True:
        try:
            # Check if the data file exists
            if not data_file_path.exists():
                print(f"Data file {data_file_path} does not exist. Creating it...")
                data_file_path.parent.mkdir(parents=True, exist_ok=True)
                with open(data_file_path, "w") as f:
                    f.write("False,False")
                sleep(1)
                continue
            
            with open(data_file_path, "r") as f:
                data = f.read().strip()
            
            if not data or "," not in data:
                print("Invalid data format in file, waiting...")
                sleep(1)
                continue
            
            parts = data.split(",", 1)  # Split on first comma only
            if len(parts) != 2:
                print("Invalid data format, expected 'prompt,status'")
                sleep(1)
                continue
                
            prompt, status = parts
            prompt = prompt.strip()
            status = status.strip()
            
            if status == "True" and prompt:
                print(f"Generating images for prompt: '{prompt}'")
                GenerateImage(prompt=prompt)
                
                # Reset the file
                with open(data_file_path, "w") as f:
                    f.write("False,False")
                print("Image generation completed, file reset")
                break
            else:
                sleep(1)
                
        except Exception as e:
            print(f"Error: {e}")
            sleep(1)

if __name__ == "__main__":
    main()
