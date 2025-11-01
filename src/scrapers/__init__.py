"""Web scraping modules for music metadata."""

from .tunebat import scrape_tunebat_info, is_tunebat_available

__all__ = [
    "scrape_tunebat_info",
    "is_tunebat_available",
]

