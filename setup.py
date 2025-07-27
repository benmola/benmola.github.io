#!/usr/bin/env python3
"""
Quick Setup Script for CV Automation System
This script helps you get started quickly with the automated CV system.
"""

import os
import sys
import json
import subprocess
import shutil
from pathlib import Path

class CVSetup:
    def __init__(self):
        """Initialize the setup process."""
        self.project_dir = Path.cwd()
        self.required_files = [
            'cv-data.json',
            'generate_cv.py',
            'generate_html.py',
            'auto_update.py',
            'requirements.txt'
        ]
    
    def check_python_version(self) -> bool:
        """Check if Python version is compatible."""
        if sys.version_info < (3, 7):
            print("❌ Python 3.7 or higher is required")
            print(f"Current version: {sys.version}")
            return False
        print(f"✅ Python {sys.version.split()[0]} detected")
        return True
    
    def check_required_files(self) -> bool:
        """Check if all required files are present."""
        missing_files = []
        for file in self.required_files:
            if not (self.project_dir / file).exists():
                missing_files.append(file)
        
        if missing_files:
            print("❌ Missing required files:")
            for file in missing_files:
                print(f"   - {file}")
            return False
        
        print("✅ All required files found")
        return True
    
    def install_dependencies(self) -> bool:
        """Install Python dependencies."""
        print("📦 Installing Python dependencies...")
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                print("✅ Dependencies installed successfully")
                return True
            else:
                print("❌ Failed to install dependencies")
                print(result.stderr)
                return False
                
        except subprocess.TimeoutExpired:
            print("❌ Installation timed out")
            return False
        except Exception as e:
            print(f"❌ Error installing dependencies: {e}")
            return False
    
    def check_latex(self) -> bool:
        """Check if LaTeX is installed."""
        try:
            result = subprocess.run(
                ['pdflatex', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print("✅ LaTeX (pdflatex) found")
                return True
            else:
                print("⚠️  LaTeX (pdflatex) not found")
                self.show_latex_installation_help()
                return False
                
        except FileNotFoundError:
            print("⚠️  LaTeX (pdflatex) not found")
            self.show_latex_installation_help()
            return False
        except Exception:
            print("⚠️  Could not check LaTeX installation")
            return False
    
    def show_latex_installation_help(self):
        """Show LaTeX installation instructions."""
        print("\n📝 To enable PDF generation, install LaTeX:")
        print("   Ubuntu/Debian: sudo apt-get install texlive-latex-extra")
        print("   macOS:         brew install --cask mactex")
        print("   Windows:       Download from https://miktex.org/")
        print("   (PDF generation will be skipped without LaTeX)\n")
    
    def create_assets_directory(self) -> bool:
        """Create assets directory if it doesn't exist."""
        assets_dir = self.project_dir / 'assets'
        if not assets_dir.exists():
            assets_dir.mkdir()
            print("✅ Created assets directory")
        
        # Check if styles.css exists
        styles_css = assets_dir / 'styles.css'
        if not styles_css.exists():
            # Create a basic styles.css
            basic_css = """/* Basic styles for CV website */
.card-hover-effect {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card-hover-effect:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.section-header {
    color: #42b883;
    border-bottom: 2px solid #3498db;
    padding-bottom: 10px;
    margin-bottom: 20px;
}

.project-status {
    position: absolute;
    top: 10px;
    right: 10px;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8em;
    font-weight: bold;
}

.status-ongoing {
    background-color: #28a745;
    color: white;
}

.status-completed {
    background-color: #6c757d;
    color: white;
}
"""
            with open(styles_css, 'w') as f:
                f.write(basic_css)
            print("✅ Created basic styles.css")
        
        return True
    
    def validate_data_file(self) -> bool:
        """Validate the cv-data.json file."""
        try:
            with open('cv-data.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check for required sections
            required_sections = ['personal', 'education', 'experience', 'projects', 'skills']
            for section in required_sections:
                if section not in data:
                    print(f"❌ Missing '{section}' section in cv-data.json")
                    return False
            
            print("✅ cv-data.json structure is valid")
            return True
            
        except FileNotFoundError:
            print("❌ cv-data.json not found")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in cv-data.json: {e}")
            return False
        except Exception as e:
            print(f"❌ Error validating cv-data.json: {e}")
            return False
    
    def check_photo(self) -> bool:
        """Check if photo file exists."""
        photo_files = ['MyPhoto.png', 'MyPhoto.jpg', 'MyPhoto.jpeg']
        for photo in photo_files:
            if (self.project_dir / photo).exists():
                print(f"✅ Photo found: {photo}")
                return True
        
        print("⚠️  No photo found (MyPhoto.png, MyPhoto.jpg, or MyPhoto.jpeg)")
        print("   Add your photo to enable profile pictures")
        return False
    
    def test_generation(self) -> bool:
        """Test file generation."""
        print("🧪 Testing file generation...")
        
        # Test HTML generation
        try:
            result = subprocess.run(
                [sys.executable, 'generate_html.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✅ HTML generation test passed")
            else:
                print("❌ HTML generation test failed")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ HTML generation test failed: {e}")
            return False
        
        # Test LaTeX generation
        try:
            result = subprocess.run(
                [sys.executable, 'generate_cv.py'],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✅ LaTeX generation test passed")
            else:
                print("❌ LaTeX generation test failed")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"❌ LaTeX generation test failed: {e}")
            return False
        
        return True
    
    def run_setup(self):
        """Run the complete setup process."""
        print("🚀 CV Automation System Setup")
        print("=" * 40)
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Check required files
        if not self.check_required_files():
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            return False
        
        # Check LaTeX
        latex_available = self.check_latex()
        
        # Create directories
        if not self.create_assets_directory():
            return False
        
        # Validate data file
        if not self.validate_data_file():
            return False
        
        # Check photo
        self.check_photo()
        
        # Test generation
        if not self.test_generation():
            return False
        
        print("\n🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Update cv-data.json with your information")
        print("2. Add your photo as MyPhoto.png")
        print("3. Run: python auto_update.py")
        print("4. Edit cv-data.json and watch files update automatically!")
        
        if not latex_available:
            print("\n⚠️  Note: Install LaTeX to enable PDF generation")
        
        return True

def main():
    """Main setup function."""
    setup = CVSetup()
    
    if len(sys.argv) > 1 and (sys.argv[1] == '--help' or sys.argv[1] == '-h'):
        print("CV Automation System Setup")
        print("Usage: python setup.py")
        print("\nThis script will:")
        print("- Check Python version compatibility")
        print("- Install required dependencies")
        print("- Check for LaTeX installation")
        print("- Validate configuration files")
        print("- Test file generation")
        return
    
    success = setup.run_setup()
    
    if not success:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)
    else:
        print("\n✨ You're all set! Happy CV updating!")

if __name__ == "__main__":
    main()
