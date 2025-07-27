#!/usr/bin/env python3
"""
Publications Extractor
Extracts publications from your existing HTML and converts them to JSON format
"""

import json
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any

class PublicationsExtractor:
    def __init__(self):
        """Initialize the extractor."""
        self.publications = []
    
    def extract_from_html(self, html_file: str = "publications.html") -> List[Dict[str, Any]]:
        """Extract publications from HTML file."""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            publication_items = soup.find_all('li', class_='list-group-item card mb-3 card-hover-effect')
            
            publications = []
            
            for item in publication_items:
                pub_data = self.parse_publication_item(item)
                if pub_data:
                    publications.append(pub_data)
            
            return publications
            
        except FileNotFoundError:
            print(f"❌ File {html_file} not found")
            return []
        except Exception as e:
            print(f"❌ Error extracting from HTML: {e}")
            return []
    
    def parse_publication_item(self, item) -> Dict[str, Any]:
        """Parse individual publication item from HTML."""
        try:
            card_body = item.find('div', class_='card-body')
            if not card_body:
                return None
            
            # Extract title and DOI
            title_element = card_body.find('h5', class_='card-title')
            if not title_element:
                return None
            
            title_link = title_element.find('a')
            if title_link:
                title = title_link.get_text().strip()
                doi = title_link.get('href', '')
            else:
                title = title_element.get_text().strip()
                doi = ""
            
            # Extract venue and year
            subtitle = card_body.find('h6', class_='card-subtitle')
            if not subtitle:
                return None
            
            subtitle_text = subtitle.get_text().strip()
            
            # Parse "Published in: VENUE, YEAR"
            venue_year_match = re.search(r'Published in:\s*(.+),\s*(\d{4})', subtitle_text)
            if venue_year_match:
                venue = venue_year_match.group(1).strip()
                year = venue_year_match.group(2).strip()
            else:
                # Fallback parsing
                parts = subtitle_text.replace('Published in:', '').strip().split(',')
                if len(parts) >= 2:
                    venue = ','.join(parts[:-1]).strip()
                    year = parts[-1].strip()
                else:
                    venue = subtitle_text.replace('Published in:', '').strip()
                    year = "Unknown"
            
            # Extract abstract
            abstract_paragraph = card_body.find('p', class_='card-text')
            abstract = ""
            if abstract_paragraph:
                abstract_text = abstract_paragraph.get_text().strip()
                if abstract_text.startswith('Abstract:'):
                    abstract = abstract_text.replace('Abstract:', '').strip()
            
            # Determine publication type
            pub_type = self.determine_publication_type(venue, title)
            
            # Create publication object
            publication = {
                "title": title,
                "authors": ["Benaissa Dekhici"],  # You can modify this as needed
                "venue": venue,
                "year": year,
                "type": pub_type
            }
            
            if doi:
                publication["doi"] = doi
            
            if abstract:
                publication["abstract"] = abstract
            
            return publication
            
        except Exception as e:
            print(f"❌ Error parsing publication item: {e}")
            return None
    
    def determine_publication_type(self, venue: str, title: str) -> str:
        """Determine publication type based on venue."""
        venue_lower = venue.lower()
        title_lower = title.lower()
        
        if 'thesis' in title_lower or 'dissertation' in title_lower:
            return "thesis"
        elif any(keyword in venue_lower for keyword in ['conference', 'symposium', 'workshop', 'proceedings']):
            return "conference"
        elif any(keyword in venue_lower for keyword in ['journal', 'transactions', 'letters']):
            return "journal"
        elif 'university' in venue_lower:
            return "thesis"
        else:
            return "conference"  # Default to conference
    
    def save_to_json(self, publications: List[Dict[str, Any]], output_file: str = "extracted_publications.json"):
        """Save publications to JSON file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(publications, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Publications saved to {output_file}")
            print(f"📊 Extracted {len(publications)} publications")
            
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")
    
    def print_publications_summary(self, publications: List[Dict[str, Any]]):
        """Print a summary of extracted publications."""
        print(f"\n📚 Publications Summary ({len(publications)} total):")
        print("=" * 60)
        
        for i, pub in enumerate(publications, 1):
            print(f"{i}. {pub['title']}")
            print(f"   📅 {pub['year']} | 📖 {pub['type'].title()}")
            print(f"   🏛️  {pub['venue']}")
            if 'doi' in pub:
                print(f"   🔗 {pub['doi']}")
            print()
    
    def merge_with_existing_data(self, cv_data_file: str = "cv-data.json") -> bool:
        """Merge extracted publications with existing CV data."""
        try:
            # Load existing CV data
            with open(cv_data_file, 'r', encoding='utf-8') as f:
                cv_data = json.load(f)
            
            # Extract publications from HTML
            extracted_pubs = self.extract_from_html()
            
            if not extracted_pubs:
                print("❌ No publications extracted")
                return False
            
            # Update publications in CV data
            cv_data['publications'] = extracted_pubs
            
            # Save updated CV data
            with open(cv_data_file, 'w', encoding='utf-8') as f:
                json.dump(cv_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Updated {cv_data_file} with {len(extracted_pubs)} publications")
            return True
            
        except FileNotFoundError:
            print(f"❌ CV data file {cv_data_file} not found")
            return False
        except Exception as e:
            print(f"❌ Error merging publications: {e}")
            return False

def main():
    """Main function."""
    extractor = PublicationsExtractor()
    
    print("📚 Publications Extractor")
    print("=" * 40)
    
    # Extract publications from HTML
    publications = extractor.extract_from_html()
    
    if not publications:
        print("❌ No publications found or extracted")
        return
    
    # Print summary
    extractor.print_publications_summary(publications)
    
    # Ask user what to do
    print("What would you like to do?")
    print("1. Save to separate JSON file (extracted_publications.json)")
    print("2. Merge with existing cv-data.json")
    print("3. Both")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        extractor.save_to_json(publications)
    
    if choice in ['2', '3']:
        success = extractor.merge_with_existing_data()
        if success:
            print("\n🎉 Publications successfully merged!")
            print("💡 Now you can run: python auto_update.py")
            print("   Your CV and website will be automatically updated!")

if __name__ == "__main__":
    main()
