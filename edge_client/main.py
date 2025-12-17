from mss import mss
from PIL import Image

def take_screenshot(filename="screenshot.png"):
    """
    Takes a screenshot of the entire screen and saves it to a file.
    """
    with mss() as sct:
        # Get raw pixels from the entire screen
        sct_img = sct.grab(sct.monitors[0])

        # Create an Image from raw pixels
        img = Image.frombytes("RGB", sct_img.size, sct_img.rgb)

        # Save to the picture file
        img.save(filename)
        print(f"Screenshot saved as {filename}")

if __name__ == "__main__":
    take_screenshot()
