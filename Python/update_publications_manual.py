#!/usr/bin/env python3
"""
Update publications from manual JSON file
Use this as a fallback when Google Scholar fetcher fails
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fetch_publications import generate_publications_html, update_publications_html


def load_manual_publications(json_file: str = 'Python/publications_manual.json'):
    """Load publications from manual JSON file."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    publications = data.get('publications', [])
    print(f"Loaded {len(publications)} publications from {json_file}")
    return publications


def main():
    """Main function."""
    try:
        # Load from manual JSON
        publications = load_manual_publications()
        
        # Update HTML
        update_publications_html(publications)
        
        print(f"\n✅ Successfully updated publications from manual JSON!")
        print(f"   Total publications: {len(publications)}")
        print(f"\n💡 To add more publications, edit: Python/publications_manual.json")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
