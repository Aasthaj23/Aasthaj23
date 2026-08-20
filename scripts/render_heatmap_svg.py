import json
from pathlib import Path
from datetime import date


INPUT = Path("data/contributions.json")
OUTPUT = Path("contrib-heatmap.svg")

PALETTE = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]


CELL = 12
GAP = 3

LEFT = 40
TOP = 35

LABEL_WIDTH = 30

WEEKS = 53
DAYS = 7

GRID_WIDTH = WEEKS * (CELL + GAP)
GRID_HEIGHT = DAYS * (CELL + GAP)

WIDTH = LEFT + LABEL_WIDTH + GRID_WIDTH + 20
HEIGHT = TOP + GRID_HEIGHT + 55


def load_data():
    with INPUT.open("r", encoding="utf-8") as f:
        return json.load(f)


def render(data):
    days = data["days"]

    # Map dates to contribution levels
    lookup = {
        item["date"]: item["level"]
        for item in days
    }

    # Find the latest date available
    last_date = max(
        date.fromisoformat(item["date"])
        for item in days
    )

    # Start roughly one year before the last date
    start_date = last_date

    # Move backward until we reach the beginning of a week
    start_date = start_date.replace(
        day=start_date.day
    )

    # Find Sunday before/at start date
    start_date -= (
        __import__("datetime").timedelta(
            days=(start_date.weekday() + 1) % 7
        )
    )

    rects = []

    for week in range(WEEKS):
        for day_index in range(DAYS):

            current_date = (
                start_date
                + __import__("datetime").timedelta(
                    days=week * 7 + day_index
                )
            )

            date_string = current_date.isoformat()

            level = lookup.get(date_string, 0)

            level = max(
                0,
                min(level, len(PALETTE) - 1)
            )

            x = LEFT + LABEL_WIDTH + week * (CELL + GAP)
            y = TOP + day_index * (CELL + GAP)

            rects.append(
                f'''
                <rect
                    x="{x}"
                    y="{y}"
                    width="{CELL}"
                    height="{CELL}"
                    rx="3"
                    fill="{PALETTE[level]}">
                    <title>
                        {date_string}: level {level}
                    </title>
                </rect>
                '''
            )

    stats = data.get("stats", {})

    current_streak = stats.get(
        "current_streak", 0
    )

    longest_streak = stats.get(
        "longest_streak", 0
    )

    username = data.get(
        "username", ""
    )

    svg = f'''
<svg xmlns="http://www.w3.org/2000/svg"
     width="{WIDTH}"
     height="{HEIGHT}"
     viewBox="0 0 {WIDTH} {HEIGHT}">

    <rect
        width="100%"
        height="100%"
        rx="12"
        fill="#0d1117"/>

    <text
        x="20"
        y="23"
        font-family="monospace"
        font-size="14"
        font-weight="bold"
        fill="#c9d1d9">
        @{username} — CONTRIBUTIONS
    </text>

    <g>
        {''.join(rects)}
    </g>

    <text
        x="{LEFT + LABEL_WIDTH}"
        y="{TOP + GRID_HEIGHT + 25}"
        font-family="monospace"
        font-size="11"
        fill="#8b949e">
        Less
    </text>

    <g>
        {''.join(
            '<rect '
            f'x="{LEFT + LABEL_WIDTH + 35 + i * 18}" '
            f'y="{TOP + GRID_HEIGHT + 15}" '
            'width="12" '
            'height="12" '
            'rx="3" '
            f'fill="{color}"/>'
            for i, color in enumerate(PALETTE)
       )}
    </g>

    <text
        x="{LEFT + LABEL_WIDTH + 35 + len(PALETTE) * 18 + 5}"
        y="{TOP + GRID_HEIGHT + 25}"
        font-family="monospace"
        font-size="11"
        fill="#8b949e">
        More
    </text>

    <text
        x="20"
        y="{HEIGHT - 10}"
        font-family="monospace"
        font-size="11"
        fill="#8b949e">
        Current streak: {current_streak} days
        • Longest streak: {longest_streak} days
    </text>

</svg>
'''

    OUTPUT.write_text(
        svg,
        encoding="utf-8"
    )

    print(f"Saved: {OUTPUT}")


if __name__ == "__main__":
    data = load_data()
    render(data)