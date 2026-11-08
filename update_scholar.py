import json
import os
from datetime import datetime, timezone
from pathlib import Path

from scholarly import scholarly

# Your Google Scholar profile ID
SCHOLAR_ID = "7f1ZqaEAAAAJ"

# File that stores the latest metrics
OUTPUT_FILE = Path("scholar_stats.json")


def update_scholar_stats():
    print("Retrieving Google Scholar profile...")

    # Retrieve your profile directly using its unique ID
    author = scholarly.search_author_id(SCHOLAR_ID)

    # Retrieve citation indices
    author = scholarly.fill(author, sections=["indices"])

    # Extract and validate the metrics
    citations = int(author["citedby"])
    h_index = int(author["hindex"])
    i10_index = int(author["i10index"])

    if min(citations, h_index, i10_index) < 0:
        raise ValueError("Google Scholar returned an invalid metric.")

    # Prepare the updated data
    stats = {
        "citations": citations,
        "h_index": h_index,
        "i10_index": i10_index,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "profile_url": (
            "https://scholar.google.com/citations"
            "?user=7f1ZqaEAAAAJ&hl=en"
        )
    }

    # Save the updated metrics
    OUTPUT_FILE.write_text(
        json.dumps(stats, indent=2) + "\n",
        encoding="utf-8"
    )

    print("Successfully updated Google Scholar metrics:")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    update_scholar_stats()
