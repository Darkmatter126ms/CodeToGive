import os
from dotenv import load_dotenv
import requests


load_dotenv()

# === CONFIG ===
API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")
OUTPUT_DIR = "generated_images"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_badge(
    prompt: str, base_image_url: str = None, output_filename: str = "output.png"):
    """
    Generates an image using the SiliconFlow AI API based on the given prompt.

    Args:
        prompt (str): The text prompt describing the image.
        output_filename (str): The filename to save the generated image.
        base_image_url (str, optional): URL of a base image to guide style (image-to-image).
    """
    payload = {
        "model": "stabilityai/stable-diffusion-3-5-large",
        "prompt": prompt,
        "size": "1024x1024",
        "n": 1,
        "response_format": "url",
    }

    if base_image_url and base_image_url.strip() and base_image_url != "None":
        payload["image_url"] = base_image_url
        payload["strength"] = 0.7  # optional: adjust influence of base image

    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

    resp = requests.post(API_URL, headers=headers, json=payload)
    if resp.status_code != 200:
        raise Exception(f"Error generating image: {resp.text}")

    result = resp.json()
    image_url = result["data"][0]["url"]
    img_resp = requests.get(image_url)

    output_path = os.path.join(OUTPUT_DIR, output_filename)
    with open(output_path, "wb") as f:
        f.write(img_resp.content)

    return output_path
