import requests
from PIL import Image
from io import BytesIO
import os 
import openai

def generate_image_stable_diffusion(prompt):
    url = "https://api.stability.ai/v1/generation/stable-diffusion-v1-5/text-to-image"
    headers = {
        "Authorization": f"Bearer {os.environ.get('STABILITY_API_KEY')}"
    }
    data = {
        "text_prompts": [{"text": prompt}],
        "cfg_scale": 7, 
        "height": 512,
        "width": 512,
        "samples": 1,
        "steps": 50, 
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        response_data = response.json()
        image_url = response_data['artifacts'][0]['base64']
        image_data = BytesIO(base64.b64decode(image_url))
        image = Image.open(image_data)
        return image
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def generate_image_dalle(prompt): 
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    response = openai.Image.create(
        prompt=prompt,
        n=1,                
        size="512x512",    
        response_format="b64" # Getting base64 encoded data
    )
    image_data = BytesIO(base64.b64decode(response['data'][0]['b64_json']))
    image = Image.open(image_data)
    return image
