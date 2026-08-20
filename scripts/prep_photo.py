import sys
from pathlib import Path
from io import BytesIO

import cv2
import numpy as np
from PIL import Image
from rembg import remove


def prep_photo(input_path):
    input_path = Path(input_path)
    output_path = input_path.parent / "source-prepped.png"

    print("Removing background...")

    with open(input_path, "rb") as f:
        input_data = f.read()

    output_data = remove(input_data)

    image = Image.open(BytesIO(output_data)).convert("RGBA")

    print("Adding white background...")

    white = Image.new("RGBA", image.size, (255, 255, 255, 255))
    white.alpha_composite(image)

    print("Improving contrast...")

    gray = np.array(white.convert("L"))

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    result = Image.fromarray(enhanced)
    result.save(output_path)

    print(f"Saved: {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scripts/prep_photo.py source-photo.jpg")
        sys.exit(1)

    prep_photo(sys.argv[1])