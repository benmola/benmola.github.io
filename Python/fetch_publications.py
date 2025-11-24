#!/usr/bin/env python3
"""
Google Scholar Publications Fetcher
Fetches publications from Google Scholar and updates publications.html
"""

import json
import re
from typing import List, Dict, Any
from scholarly import scholarly, ProxyGenerator

def fetch_scholar_publications(scholar_id: str) -> List[Dict[str, Any]]:
    """
    Fetch publications from Google Scholar.
    
    Args:
        scholar_id: Google Scholar author ID (e.g., 'ELEdK98AAAAJ')
    
    Returns:
        List of publication dictionaries
    """
    print(f"Fetching publications for scholar ID: {scholar_id}")
    
    # Set up a proxy to avoid rate limiting
    try:
        print("Setting up proxy to avoid rate limiting...")
        pg = ProxyGenerator()
        pg.FreeProxies()
        scholarly.use_proxy(pg)
        print("✓ Proxy configured")
    except Exception as e:
        print(f"⚠ Warning: Could not set up proxy: {e}")
        print("  Continuing without proxy...")
    
    try:
        # Search for author
        print("Searching for author...")
        search_query = scholarly.search_author_id(scholar_id)
        
        print("Filling author details...")
        author = scholarly.fill(search_query)
        
        print(f"✓ Found author: {author.get('name', 'Unknown')}")
        print(f"  Total publications: {len(author.get('publications', []))}")
        
        publications = []
        
        for i, pub in enumerate(author['publications'], 1):
            try:
                print(f"  Fetching publication {i}/{len(author['publications'])}...")
                # Fill publication details
                filled_pub = scholarly.fill(pub)
                
                # Extract relevant information
                pub_data = {
                    'title': filled_pub['bib'].get('title', ''),
                    'authors': filled_pub['bib'].get('author', ''),
                    'venue': filled_pub['bib'].get('venue', filled_pub['bib'].get('journal', '')),
                    'year': filled_pub['bib'].get('pub_year', ''),
                    'abstract': filled_pub['bib'].get('abstract', ''),
                    'url': filled_pub.get('pub_url', filled_pub.get('eprint_url', '')),
                    'citations': filled_pub.get('num_citations', 0)
                }
                
                publications.append(pub_data)
                print(f"    ✓ {pub_data['title'][:60]}...")
                
            except Exception as e:
                print(f"    ⚠ Warning: Could not fetch publication {i}: {e}")
                # Add basic info even if full details fail
                pub_data = {
                    'title': pub.get('bib', {}).get('title', 'Unknown'),
                    'authors': pub.get('bib', {}).get('author', ''),
                    'venue': pub.get('bib', {}).get('venue', ''),
                    'year': pub.get('bib', {}).get('pub_year', ''),
                    'abstract': '',
                    'url': pub.get('pub_url', ''),
                    'citations': pub.get('num_citations', 0)
                }
                publications.append(pub_data)
        
        # Sort by year (newest first)
        publications.sort(key=lambda x: int(x['year']) if x['year'] else 0, reverse=True)
        
        return publications
        
    except Exception as e:
        print(f"\n❌ Error fetching from Google Scholar: {e}")
        print("\nThis is likely due to Google Scholar rate limiting.")
        print("Please try again in a few minutes, or use the manual update method.")
        raise


def save_publications_to_json(publications: List[Dict[str, Any]], output_file: str = 'Python/publications_data.json'):
    """Save publications to JSON file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(publications, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(publications)} publications to {output_file}")


def generate_publications_html(publications: List[Dict[str, Any]]) -> str:
    """Generate HTML for publications list."""
    html_items = []
    
    for pub in publications:
        # Format authors
        authors = pub['authors'] if isinstance(pub['authors'], str) else ', '.join(pub['authors'])
        
        # Create publication card HTML
        title_html = f'<a href="{pub["url"]}" target="_blank">{pub["title"]}</a>' if pub['url'] else pub['title']
        
        html = f'''                <li class="list-group-item card mb-3 card-hover-effect">
                    <div class="card-body">
                        <h5 class="card-title">{title_html}</h5>
                        <h6 class="card-subtitle mb-2 text-muted">
                            <strong>Authors:</strong> {authors}<br>
                            Published in: {pub["venue"]}, {pub["year"]}
                        </h6>'''
        
        if pub['abstract']:
            html += f'''
                        <p class="card-text"><strong>Abstract:</strong> {pub["abstract"]}</p>'''
        
        if pub['citations'] > 0:
            html += f'''
                        <p class="card-text"><small class="text-muted">Citations: {pub["citations"]}</small></p>'''
        
        html += '''
                    </div>
                </li>'''
        
        html_items.append(html)
    
    return '\n'.join(html_items)


def update_publications_html(publications: List[Dict[str, Any]], html_file: str = 'publications.html'):
    """Update publications.html with new publications."""
    # Read current HTML
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Generate new publications HTML
    new_pubs_html = generate_publications_html(publications)
    
    # Find and replace the publications list
    # Look for the <ul class="timeline list-group list-group-flush"> section
    pattern = r'(<ul class="timeline list-group list-group-flush">)(.*?)(</ul>)'
    
    replacement = f'\\1\n{new_pubs_html}\n            \\3'
    
    updated_html = re.sub(pattern, replacement, html_content, flags=re.DOTALL)
    
    # Write updated HTML
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(updated_html)
    
    print(f"Updated {html_file} with {len(publications)} publications")


def main():
    """Main function."""
    # Your Google Scholar ID
    SCHOLAR_ID = 'ELEdK98AAAAJ'
    
    try:
        # Fetch publications
        print("Fetching publications from Google Scholar...")
        publications = fetch_scholar_publications(SCHOLAR_ID)
        
        # Save to JSON for backup
        save_publications_to_json(publications)
        
        # Update HTML
        update_publications_html(publications)
        
        print(f"\n✅ Successfully updated publications!")
        print(f"   Total publications: {len(publications)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
