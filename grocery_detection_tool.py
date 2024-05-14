import base64
import requests
from langchain.tools import BaseTool
import dotenv
import time
import requests
from PIL import Image
from io import BytesIO
import os

# class ImageCaptionTool(BaseTool):
#     name = "image_captioner"
#     description = "Use this tool when given the path to an image that you would like to be described. It will return a simple caption describing the image."

#     def _run(self, img_path):
#         return detect_groceries(img_path)

#     def _arun(self, query: str):
#         raise NotImplementedError("This tool does not support async")

start_time = time.time()
# OpenAI API Key
# Load environment variables from .env file
dotenv.load_dotenv()

# OpenAI API Key
api_key = os.getenv('API_KEY')

# Replace this URL with the actual URL of your ESP32 camera server
url = 'http://10.42.8.154/capture'
# Path to your image
image_path = "./images/captured_image.jpg"

# Sending a GET request to the ESP32-CAM and saving the response
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Open a file in binary write mode and save the image
    if os.path.exists(image_path):
        # Remove the file
        os.remove(image_path)
        print(f"The file {image_path} has been deleted.")
    with open(image_path, 'wb') as f:
        f.write(response.content)
    print("Image saved successfully.")
else:
    print("Failed to retrieve the image.")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4-vision-preview",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Name the groceries in the image each in 1 word."
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# print(response.choices[0].message.content)
print(response.json()["choices"][0]["message"]["content"])
end_time = time.time()
print("Total seconds: ", end_time - start_time)
