"""String sanitization utilities."""

import re


def sanitize_filename(name: str) -> str:
    """
    Sanitize a string to be safe for use as a filename.
    
    Keeps letters, numbers, spaces, dashes, underscores, and parentheses.
    Collapses multiple whitespace characters into a single space.
    
    Args:
        name: Original string to sanitize
        
    Returns:
        Sanitized string safe for use as filename
        
    Example:
        >>> sanitize_filename("Song Title  (feat. Artist)")
        'Song Title (feat Artist)'
    """
    # Collapse multiple whitespace
    name = re.sub(r"\s+", " ", name).strip()
    
    # Remove special characters except word chars, dash, space, parens
    name = re.sub(r"[^\w\- ()]", "", name)
    
    # Normalize spaces again
    name = re.sub(r"\s", " ", name).strip()
    
    return name or "yt_download"

