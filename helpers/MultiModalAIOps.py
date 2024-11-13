# Pixtral AI
import io
import os
import base64
import dotenv
import numpy as np
dotenv.load_dotenv()
from PIL import Image
from mistralai import Mistral


def image_to_data_url(image_array:np.ndarray, format = "PNG"):
    """
    Convert PIL image to a data URL without saving to disk.
    """
    buffer = io.BytesIO()

    image = image = Image.fromarray(image_array)
    image.save(buffer, format = format)
    buffer.seek(0)
    encoded_string = base64.b64encode(buffer.read()).decode("utf-8")
    mime_type = f"image/{format.lower()}"
    return f"data:{mime_type};base64,{encoded_string}"


def pixtral_describe_target(image_url:str):
    # Retrieve the API key from environment variables
    api_key = os.environ["MISTRAL_API_KEY"]

    # Specify model
    model = "pixtral-12b-2409"

    # Initialize the Mistral client
    client = Mistral(api_key = api_key)

    # Define the messages for the chat
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """Give a detailed description of the individual with the green bounding box on face.
                            The following are some piece of information you can include about the individual if found within the image:
                            Include information such as sex (male or female), Observed racial or ethnic background, Complexion,
                            Distinctive Features: Birthmarks, scars, tattoos, or moles; Hair: Color, length, Facial Hair: Beard, mustache, sideburns,
                            Headwear, Upper Body: Shirts, jackets, sweaters (include color, style, logos), Lower Body: Pants, skirts, shorts (include color and type),
                            Footwear: Shoes, boots, sandals (include color and type).
                            Accessories: Scarves, gloves, belts, backpacks, or handbags.
                            Outerwear: Coats, rainwear, or specific gear.

                            For example, you could give a description such as:
                            
                            Description of the Individual (Green Box):
                            Observable Sex: Male.
                            Complexion: Medium to dark complexion.
                            Hair: Short, closely cropped hair, dark in color.
                            Facial Hair: Clean-shaven.
                            Accessories: Wearing clear-framed glasses.
                            Upper Body: Olive green jacket with a zipper, possibly made of a soft fabric.
                            Lower Body and Footwear: Not clearly visible in image.
                            Distinctive Features: None clearly visible, such as tattoos, moles, or scars.
                            Outerwear: Olive green jacket acts as the main outer layer.
                            """
                },
                {
                    "type": "image_url",
                    "image_url": image_url
                }
            ]
        }
    ]

    # Get the chat response
    chat_response = client.chat.complete(
        model = model,
        messages = messages
    )
    return chat_response.choices[0].message.content


# OpenAI