import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()


class StabilityImage:

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.base_url = "https://api.stability.ai/v2beta/stable-image/"
        # self.output_format = "webp"
        self.session = requests.session()

    def __str__(self) -> str:
        return "Stability Image Generator Class"

    def generateImage(
        self,
        prompt: str,
        filename: str,
        negative_prompt: str = "",
        seed: int = 0,
        aspect_ratio: str = "1:1",
        output_format: str = "webp",
    ) -> bool:
        try:
            response = self.session.post(
                self.base_url + "generate/core",
                headers={
                    "authorization": f"Bearer {self.api_key}",
                    "accept": "image/*",
                },
                files={"none": ""},
                data={
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "seed": seed,
                    "output_format": output_format,
                    "aspect_ratio": aspect_ratio,
                },
            )
            print(response.status_code)
            if response.status_code == 200:
                if self.writeFile(filename, response.content):
                    return True
                return False
            print(response.content)
            return False

        except Exception as e:
            print(e)
            return False

    def upscaleImage(
        self,
        init_file: str,
        prompt: str,
        filename: str,
        negative_prompt: str = "",
        seed: int = 0,
        creativity: int = 0.2,
        output_format: str = "webp",
    ) -> bool:
        try:
            response = self.session.post(
                self.base_url + "upscale/creative",
                headers={
                    "authorization": f"Bearer {self.api_key}",
                    "accept": "image/*",
                },
                files={"init_file": init_file},
                data={
                    "prompt": prompt,
                    "negative_prompt": negative_prompt,
                    "seed": seed,
                    "creativity": creativity,
                    "output_format": output_format,
                },
            )
            print(response.status_code)
            if response.status_code == 200:
                if self.writeFile(filename, response.content):
                    return True
                return False
            print(response.content)
            return False

        except Exception as e:
            print(e)
            return False

    def writeFile(self, filename: str, content: bytes, format: str = "webp") -> bool:
        if not filename.endswith(format):
            filename = filename + "." + format
        try:
            with open(filename, "wb") as fileHandler:
                fileHandler.write(content)
            return True
        except Exception as e:
            print(e)
            return False

    def __del__(self):
        if hasattr(self, "session"):
            self.session.close()


if __name__ == "__main__":

    api_key = os.getenv("API_KEY")
    print(api_key)
    main_object = StabilityImage(api_key=api_key)
    print(main_object)
    prompt = """Create an image of dog wearing samurai uniform in dark room in front of computer. The dog is also wearing glasses and is programming. The glasses is slightly reflecting the computer screen.Use some neon lights and add alot posters related to computer science and python programming in the wall."""
    generated_image = main_object.generateImage(prompt, "coding_dog")
    print(generated_image)
