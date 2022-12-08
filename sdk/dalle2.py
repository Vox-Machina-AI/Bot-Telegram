import os
from dalle2 import Dalle2


class DALLE2:
    def __init__(self):
        self.dalle = Dalle2(os.getenv('DALLE2_TOKEN'))

    def generate_images(self, prompt):
        generations = self.dalle.generate(prompt)
        return list(map(lambda img: img['generation']['image_path'], generations))
