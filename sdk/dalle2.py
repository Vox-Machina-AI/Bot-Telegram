
import os
from dalle2 import Dalle2

class DALLE2:
    def __init__(self):
        self.dalle = Dalle2(os.getenv('DALLE2_TOKEN'))

    def generate_image(self, prompt):
        generations = self.dalle.generate(prompt)
        return generations[0]['generation']['image_path']
