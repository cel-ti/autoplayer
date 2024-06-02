import datetime
import logging
import os
import sys
from PIL import Image
import io
from discord_webhook import DiscordWebhook
_debug_toggle : bool = False

def debug_on():
    global _debug_toggle
    _debug_toggle = True
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)

def discord_webhook(image: Image.Image):
    webhook_url = os.getenv("DISCORD_WEBHOOK")
    if not webhook_url:
        print("No webhook URL provided.")
        return

    # Convert PIL Image to bytes
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)  # move to the start of the byte array

    webhook = DiscordWebhook(url=webhook_url)

    # Attach the image file
    webhook.add_file(file=img_byte_arr.getvalue(), filename='image.png')

    # Execute the webhook
    response = webhook.execute()
    if response.status_code == 200 or response.status_code == 204:
        print("Image sent successfully.")
    else:
        print(f"Failed to send image. Status code: {response.status_code}")


def debug_img(image : Image.Image):
    if not _debug_toggle:
        return
    
    os.makedirs("debug", exist_ok=True)
    image.save(f"debug/{datetime.datetime.now()}.png")