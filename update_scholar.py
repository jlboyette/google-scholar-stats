import json
from datetime import datetime, timezone
from pathlib import Path

from scholarly import scholarly

# Google Scholar profile ID
SCHOLAR_ID = "7f1ZqaEAAAAJ"

# Output file
OUTPUT_FILE = Path("scholar_stats.json")


def update_scholar_stats():
    print("Retrieving Google Scholar profile...")

    # Retrieve profile and citation indices
    author = scholarly.search_author_id(SCHOLAR_ID)
    author = scholarly.fill(author, sections=["indices"])

    citations = int(author["citedby"])
    h_index = int(author["hindex"])
    i10_index = int(author["i10index"])

    # Validate retrieved values
    if min(citations, h_index, i10_index) < 0:
        raise ValueError("Invalid Google Scholar metrics.")

    # Display text for the i10-index
    i10_display = "Not yet!" if i10_index == 0 else str(i10_index)

    # Prepare updated metrics
    stats = {
        "citations": citations,
        "h_index": h_index,
        "i10_index": i10_index,
        "i10_display": i10_display,
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "profile_url": (
            "https://scholar.google.com/citations"
            "?user=7f1ZqaEAAAAJ&hl=en"
        )
    }

    # Save only after successful retrieval
    OUTPUT_FILE.write_text(
        json.dumps(stats, indent=2) + "\n",
        encoding="utf-8"
    )

    print("Successfully updated metrics:")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    update_scholar_stats()
