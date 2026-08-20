from pathlib import Path
import os


OUTPUT = Path("info-card.svg")

STATIC = os.getenv("STATIC") == "1"


def make_info_card():

    rows = [
        ("NOW", "Building cool things"),
        ("PREV", "Learning • Exploring • Growing"),
        ("STACK", "Python • SQL • Git • HTML/CSS"),
        ("HIGHLIGHTS", "Projects • Engineering • Problem Solving"),
    ]

    width = 620
    row_height = 45
    header_height = 70
    height = header_height + len(rows) * row_height + 30

    svg_rows = []

    for i, (key, value) in enumerate(rows):

        y = header_height + 30 + i * row_height

        if STATIC:
            animation = ""
        else:
            animation = f'''
            <animate
                attributeName="opacity"
                from="0"
                to="1"
                dur="0.5s"
                begin="{i * 0.15}s"
                fill="freeze"/>
            <animate
                attributeName="transform"
                from="translate(0,8)"
                to="translate(0,0)"
                dur="0.5s"
                begin="{i * 0.15}s"
                fill="freeze"/>
            '''

        svg_rows.append(
            f'''
            <g opacity="0">
                <text
                    x="35"
                    y="{y}"
                    font-family="monospace"
                    font-size="17"
                    font-weight="bold"
                    fill="#7aa2f7">
                    {key}
                </text>

                <text
                    x="180"
                    y="{y}"
                    font-family="monospace"
                    font-size="17"
                    fill="#d8dee9">
                    {value}
                </text>

                {animation}
            </g>
            '''
        )

    animation = "" if STATIC else '''
        <animate
            attributeName="opacity"
            from="0"
            to="1"
            dur="0.6s"
            fill="freeze"/>
    '''

    svg = f'''
<svg xmlns="http://www.w3.org/2000/svg"
     width="{width}"
     height="{height}"
     viewBox="0 0 {width} {height}">

    <rect
        x="1"
        y="1"
        width="{width - 2}"
        height="{height - 2}"
        rx="12"
        fill="#111318"
        stroke="#3b4252"
        stroke-width="2"/>

    <rect
        x="1"
        y="1"
        width="{width - 2}"
        height="{header_height}"
        rx="12"
        fill="#191c24"/>

    <circle cx="25" cy="35" r="7" fill="#ff5f56"/>
    <circle cx="48" cy="35" r="7" fill="#ffbd2e"/>
    <circle cx="71" cy="35" r="7" fill="#27c93f"/>

    <text
        x="105"
        y="42"
        font-family="monospace"
        font-size="20"
        font-weight="bold"
        fill="#e5e9f0">
        AASTHA@GITHUB
    </text>

    <g>
        {''.join(svg_rows)}
    </g>

    {animation}

</svg>
'''

    OUTPUT.write_text(svg, encoding="utf-8")

    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    make_info_card()