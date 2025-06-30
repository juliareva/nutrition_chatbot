import os
from openai import OpenAI
from dotenv import load_dotenv
import base64


load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def get_macros_from_gpt(user_text):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a nutrition assistant. Calculate calories, protein, fat, and carbs for the food described by the user. Be concise and to the point."},
            {"role": "user", "content": user_text}
        ]
    )
    return response.choices[0].message.content


def get_macros_from_image(image_bytes):

    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    print(f"Sending image to GPT, base64 preview: {base64_image[:50]}...")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": "You are a nutrition assistant. When the user sends an image of food or a nutrition label, analyze it and estimate calories, protein, fat, and carbs. Be clear and concise."
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )

    return response.choices[0].message.content

