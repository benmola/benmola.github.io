#!/usr/bin/env python3
"""
Activities Extractor
Extracts activities from your existing HTML and converts them to JSON format
"""

import json
import re
from typing import List, Dict, Any

class ActivitiesExtractor:
    def __init__(self):
        """Initialize the extractor."""
        self.activities = []
    
    def extract_from_html(self, html_file: str = "skills.html") -> List[Dict[str, Any]]:
        """Extract activities from HTML file."""
        try:
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for activities in the timeline
            activities = []
            
            # Find all <li> elements that contain dates and activities
            activity_pattern = r'<li class="list-group-item"><strong>([^<]+):</strong>\s*([^<]+)(?:</li>)?'
            matches = re.findall(activity_pattern, content, re.DOTALL)
            
            for date_str, description in matches:
                activity = self.parse_activity(date_str.strip(), description.strip())
                if activity:
                    activities.append(activity)
            
            return activities
            
        except FileNotFoundError:
            print(f"❌ File {html_file} not found")
            return []
        except Exception as e:
            print(f"❌ Error extracting from HTML: {e}")
            return []
    
    def parse_activity(self, date_str: str, description: str) -> Dict[str, Any]:
        """Parse individual activity."""
        try:
            # Clean up description
            description = re.sub(r'<[^>]+>', '', description).strip()
            
            # Determine activity type based on keywords
            activity_type = self.determine_activity_type(description)
            
            # Extract location if present
            location = self.extract_location(description)
            
            # Create activity object
            activity = {
                "date": date_str,
                "event": self.extract_event_name(description),
                "type": activity_type,
                "description": description
            }
            
            if location:
                activity["location"] = location
            
            return activity
            
        except Exception as e:
            print(f"❌ Error parsing activity: {e}")
            return None
    
    def determine_activity_type(self, description: str) -> str:
        """Determine activity type based on description."""
        desc_lower = description.lower()
        
        if any(keyword in desc_lower for keyword in ['conference', 'symposium']):
            return "conference"
        elif any(keyword in desc_lower for keyword in ['workshop', 'modelling workshop']):
            return "workshop"
        elif any(keyword in desc_lower for keyword in ['summer school']):
            return "summer_school"
        elif any(keyword in desc_lower for keyword in ['spring school']):
            return "spring_school"
        elif any(keyword in desc_lower for keyword in ['training', 'mooc']):
            return "training"
        elif any(keyword in desc_lower for keyword in ['presentation', 'presented', 'talk', 'delivered']):
            return "presentation"
        elif any(keyword in desc_lower for keyword in ['webinar', 'webinaire']):
            return "webinar"
        elif any(keyword in desc_lower for keyword in ['seminar']):
            return "seminar"
        else:
            return "conference"  # Default
    
    def extract_location(self, description: str) -> str:
        """Extract location from description."""
        # Common location patterns
        location_patterns = [
            r'at\s+([^,]+(?:,\s*[^.]+)?)',
            r'in\s+([^,]+(?:,\s*[^.]+)?)',
            r',\s+([A-Z][^,]+(?:,\s*[A-Z][^,]+)?)\.',
            r'organized by.*in\s+([^,]+)',
            r'University of\s+([^,]+)',
            r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*,\s*[A-Z][a-z]+)',  # City, Country pattern
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, description, re.IGNORECASE)
            if match:
                location = match.group(1).strip()
                # Clean up location
                location = re.sub(r'^(the\s+)?', '', location, flags=re.IGNORECASE)
                if len(location) > 50:  # Skip if too long (probably not a location)
                    continue
                return location
        
        return ""
    
    def extract_event_name(self, description: str) -> str:
        """Extract event name from description."""
        # Try to find event name in quotes or after "Attended"
        event_patterns = [
            r'"([^"]+)"',
            r'Attended.*?(\d+(?:st|nd|rd|th)?\s+[^,]+)',
            r'Participation in.*?([A-Z][^,]+)',
            r'Delivered.*?on\s+"([^"]+)"',
            r'([A-Z][A-Z\s&]+(?:\d{4})?)',  # All caps event names
        ]
        
        for pattern in event_patterns:
            match = re.search(pattern, description)
            if match:
                event_name = match.group(1).strip()
                if len(event_name) > 10 and len(event_name) < 100:
                    return event_name
        
        # Fallback: extract first part of description
        words = description.split()
        if len(words) > 3:
            return ' '.join(words[:8]) + "..."
        
        return description[:50] + "..." if len(description) > 50 else description
    
    def save_to_json(self, activities: List[Dict[str, Any]], output_file: str = "extracted_activities.json"):
        """Save activities to JSON file."""
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(activities, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Activities saved to {output_file}")
            print(f"📊 Extracted {len(activities)} activities")
            
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")
    
    def print_activities_summary(self, activities: List[Dict[str, Any]]):
        """Print a summary of extracted activities."""
        print(f"\n📅 Activities Summary ({len(activities)} total):")
        print("=" * 60)
        
        # Group by type
        by_type = {}
        for activity in activities:
            activity_type = activity.get('type', 'unknown')
            if activity_type not in by_type:
                by_type[activity_type] = []
            by_type[activity_type].append(activity)
        
        for activity_type, type_activities in by_type.items():
            icon = {
                'conference': '📊',
                'workshop': '🛠️',
                'training': '📚',
                'presentation': '🎤',
                'summer_school': '🏫',
                'spring_school': '🌱',
                'webinar': '💻',
                'symposium': '🎯',
                'seminar': '📋'
            }.get(activity_type, '📅')
            
            print(f"\n{icon} {activity_type.replace('_', ' ').title()} ({len(type_activities)} items):")
            for activity in type_activities[:3]:  # Show first 3
                print(f"   • {activity['date']}: {activity['event'][:60]}...")
            if len(type_activities) > 3:
                print(f"   ... and {len(type_activities) - 3} more")
    
    def merge_with_existing_data(self, cv_data_file: str = "cv-data.json") -> bool:
        """Merge extracted activities with existing CV data."""
        try:
            # Load existing CV data
            with open(cv_data_file, 'r', encoding='utf-8') as f:
                cv_data = json.load(f)
            
            # Extract activities from HTML
            extracted_activities = self.extract_from_html()
            
            if not extracted_activities:
                print("❌ No activities extracted")
                return False
            
            # Update activities in CV data
            cv_data['activities'] = extracted_activities
            
            # Save updated CV data
            with open(cv_data_file, 'w', encoding='utf-8') as f:
                json.dump(cv_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Updated {cv_data_file} with {len(extracted_activities)} activities")
            return True
            
        except FileNotFoundError:
            print(f"❌ CV data file {cv_data_file} not found")
            return False
        except Exception as e:
            print(f"❌ Error merging activities: {e}")
            return False

def main():
    """Main function."""
    extractor = ActivitiesExtractor()
    
    print("📅 Activities Extractor")
    print("=" * 40)
    
    # Extract activities from HTML
    activities = extractor.extract_from_html()
    
    if not activities:
        print("❌ No activities found or extracted")
        print("💡 Make sure your skills.html contains activities in <li> elements")
        return
    
    # Print summary
    extractor.print_activities_summary(activities)
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Save to separate JSON file (extracted_activities.json)")
    print("2. Merge with existing cv-data.json")
    print("3. Both")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        extractor.save_to_json(activities)
    
    if choice in ['2', '3']:
        success = extractor.merge_with_existing_data()
        if success:
            print("\n🎉 Activities successfully merged!")
            print("💡 Now you can enable activities in cv-config.json:")
            print("   \"activities\": true")
            print("💡 Then run: python auto_update_configurable.py")

if __name__ == "__main__":
    main()
