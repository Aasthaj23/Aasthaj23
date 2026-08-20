from pathlib import Path
from PIL import Image


INPUT = Path("source-prepped.png")
OUTPUT = Path("ascii-portrait.svg")

WIDTH = 100
RAMP = " .`:-=+*cs#%@"

CHAR_WIDTH = 6
CHAR_HEIGHT = 10


def make_svg():
    image = Image.open(INPUT).convert("L")

    aspect = image.height / image.width
    height = max(1, int(WIDTH * aspect * 0.5))

    image = image.resize((WIDTH, height))

    pixels = image.load()
    lines = []

    for y in range(height):
        line = ""

        for x in range(WIDTH):
            brightness = pixels[x, y]

            index = int(
                (255 - brightness)
                / 255
                * (len(RAMP) - 1)
            )

            line += RAMP[index]

        lines.append(line)

    svg_width = WIDTH * CHAR_WIDTH
    svg_height = height * CHAR_HEIGHT

    text_lines = []

    for y, line in enumerate(lines):
        escaped = (
            line
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        text_lines.append(
            f'<text x="0" y="{(y + 1) * CHAR_HEIGHT}" '
            f'font-family="monospace" font-size="10" '
            f'fill="#b8b8b8">{escaped}</text>'
        )

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{svg_width}"
height="{svg_height}"
viewBox="0 0 {svg_width} {svg_height}">
<rect width="100%" height="100%" fill="white"/>
{"".join(text_lines)}
</svg>
'''

    OUTPUT.write_text(svg, encoding="utf-8")

    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    make_svg()