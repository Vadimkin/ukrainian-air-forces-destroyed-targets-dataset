import base64
import os

import requests
import config

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {config.OPENAI_API_KEY}"
}


def recognize_all_images():
    path = config.RAW_IMAGES_PATH
    for filename in os.listdir(path):
        if not filename.endswith(".jpg"):
            print(f"Skipping {filename}...")
            continue

        process_image(filename)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def process_image(image_filename):
    path = config.RAW_IMAGES_PATH / image_filename
    base64_image = encode_image(path)

    output_filename = image_filename.replace(".jpg", ".txt")
    if os.path.exists(config.RAW_TXT_PATH / output_filename):
        print(f"Skipping {image_filename}...")
        return

    print(f"Processing {image_filename}")

    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Identify and transcribe the text visible in this picture. Ignore any visual elements or images, focusing solely on the text. Provide the transcribed text without any alterations or interpretations. Do not translate the text; transcribe it in its original language"
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
    print("Response:", response.json())

    with open(config.RAW_TXT_PATH / output_filename, "w") as f:
        f.write(response.json()["choices"][0]["message"]["content"])
