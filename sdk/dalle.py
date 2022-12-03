import openai
import os

class DALLE:
    def __init__(self):
        openai.api_key = os.getenv('DALLE_TOKEN')
        self.dalle = openai.Image

    def generate_images(self, prompt):
        images = self.dalle.create(prompt=prompt, n=4, size="1024x1024")['data']
        return list(map(lambda img: img['url'], images))
