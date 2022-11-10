import openai
import os


class DALLE:
    def __init__(self):
        self.a = ""

    @staticmethod
    def generate_image(prompt):
        openai.api_key = os.getenv('DALLE_TOKEN')
        return openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )['data'][0]['url']
