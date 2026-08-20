import json
import sys
from datetime import date, timedelta
from pathlib import Path

import requests
from bs4 import BeautifulSoup


OUTPUT = Path("data/contributions.json")


def fetch_contributions(username):
    url = f"https://github.com/users/{username}/contributions"

    print(f"Fetching contributions for @{username}...")

    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0"
        },
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    days = []

    for cell in soup.select("td.ContributionCalendar-day"):
        day = cell.get("data-date")
        level = cell.get("data-level")

        if not day or level is None:
            continue

        days.append({
            "date": day,
            "level": int(level),
        })

    if not days:
        raise RuntimeError(
            "No contribution cells were found. "
            "GitHub may have changed its HTML structure."
        )

    # Sort chronologically
    days.sort(key=lambda x: x["date"])

    # Convert to useful statistics
    counts = []

    for day in days:
        counts.append({
            "date": day["date"],
            "level": day["level"],
        })

    # Current streak
    contribution_dates = {
        item["date"]
        for item in counts
        if item["level"] > 0
    }

    today = date.today()

    # GitHub's calendar may end at yesterday/today depending
    # on when the page was generated.
    current = today

    if current.isoformat() not in contribution_dates:
        current -= timedelta(days=1)

    current_streak = 0

    while current.isoformat() in contribution_dates:
        current_streak += 1
        current -= timedelta(days=1)

    # Longest streak
    longest_streak = 0
    running = 0
    previous = None

    for item in counts:
        current_date = date.fromisoformat(item["date"])

        if item["level"] > 0:
            if (
                previous is not None
                and current_date == previous + timedelta(days=1)
            ):
                running += 1
            else:
                running = 1

            longest_streak = max(longest_streak, running)
            previous = current_date

    # Best day
    best_day = max(
        counts,
        key=lambda item: item["level"]
    )

    # Monthly totals
    monthly_totals = {}

    for item in counts:
        month = item["date"][:7]
        monthly_totals.setdefault(month, 0)

        # The level is a contribution intensity, not an exact count.
        monthly_totals[month] += item["level"]

    result = {
        "username": username,
        "days": counts,
        "stats": {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": best_day,
            "monthly_totals": monthly_totals,
        },
    }

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    OUTPUT.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8",
    )

    print(f"Saved: {OUTPUT}")
    print(f"Days found: {len(days)}")
    print(f"Current streak: {current_streak}")
    print(f"Longest streak: {longest_streak}")


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print(
            "Usage: "
            "python scripts/fetch_contributions.py YOUR_USERNAME"
        )
        sys.exit(1)

    fetch_contributions(sys.argv[1])