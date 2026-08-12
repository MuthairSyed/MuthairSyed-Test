import json
from pathlib import Path
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent.parent

DATA_FILE = ROOT / "data" / "github-stats.json"
SVG_FILE = ROOT / "assets" / "git-status.svg"


def load_stats():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def format_number(value):
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return "0"


def format_date(value):
    if not value or value == "N/A":
        return "N/A"

    try:
        date = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )

        return date.strftime("%d %b %Y")

    except (ValueError, TypeError):
        return str(value)


def replace_text(svg, marker, value):
    return svg.replace(
        f"<!-- {marker} -->",
        str(value)
    )


def generate():
    stats = load_stats()

    repositories = format_number(
        stats.get("repositories", 0)
    )

    followers = format_number(
        stats.get("followers", 0)
    )

    following = format_number(
        stats.get("following", 0)
    )

    stars = format_number(
        stats.get("stars", 0)
    )

    forks = format_number(
        stats.get("forks", 0)
    )

    latest_commit = format_date(
        stats.get("latest_commit")
    )

    last_activity = format_date(
        stats.get("last_activity")
    )

    updated_at = format_date(
        stats.get("updated_at")
    )

    with open(
        SVG_FILE,
        "r",
        encoding="utf-8"
    ) as file:
        svg = file.read()

    replacements = {
        "GITHUB_REPOSITORIES": repositories,
        "GITHUB_FOLLOWERS": followers,
        "GITHUB_FOLLOWING": following,
        "GITHUB_STARS": stars,
        "GITHUB_FORKS": forks,
        "GITHUB_LATEST_COMMIT": latest_commit,
        "GITHUB_LAST_ACTIVITY": last_activity,
        "GITHUB_UPDATED": updated_at,
    }

    for marker, value in replacements.items():
        svg = replace_text(
            svg,
            marker,
            value
        )

    with open(
        SVG_FILE,
        "w",
        encoding="utf-8"
    ) as file:
        file.write(svg)

    print("Git status SVG updated successfully.")
    print()
    print(f"Repositories : {repositories}")
    print(f"Followers    : {followers}")
    print(f"Following    : {following}")
    print(f"Stars        : {stars}")
    print(f"Forks        : {forks}")
    print(f"Latest commit: {latest_commit}")
    print(f"Last activity: {last_activity}")
    print(f"Updated      : {updated_at}")


if __name__ == "__main__":
    generate()
