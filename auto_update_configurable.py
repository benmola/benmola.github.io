#!/usr/bin/env python3
"""
Auto Update Script (Configurable Version)
Watches for changes in cv-data.json and cv-config.json and automatically regenerates files
"""

import os
import sys
import time
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

class ConfigurableAutoUpdater:
    def __init__(self, data_file: str = "cv-data.json", config_file: str = "cv-config.json"):
        """Initialize the auto updater."""
        self.data_file = data_file
        self.config_file = config_file
        self.last_data_hash = self.get_file_hash(data_file)
        self.last_config_hash = self.get_file_hash(config_file)
        self.last_update = datetime.now()
        
    def get_file_hash(self, file_path: str) -> str:
        """Get MD5 hash of a file."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except FileNotFoundError:
            return ""
    
    def files_changed(self) -> tuple[bool, list]:
        """Check if any watched files have changed."""
        changed_files = []
        
        # Check data file
        current_data_hash = self.get_file_hash(self.data_file)
        if current_data_hash != self.last_data_hash:
            self.last_data_hash = current_data_hash
            changed_files.append(self.data_file)
        
        # Check config file
        current_config_hash = self.get_file_hash(self.config_file)
        if current_config_hash != self.last_config_hash:
            self.last_config_hash = current_config_hash
            changed_files.append(self.config_file)
        
        return len(changed_files) > 0, changed_files
    
    def run_script(self, script_name: str) -> bool:
        """Run a Python script and return success status."""
        try:
            result = subprocess.run(
                [sys.executable, script_name],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"✅ {script_name} executed successfully")
                if result.stdout:
                    # Print only important output lines
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if any(marker in line for marker in ['✅', '❌', '⚠️', '📋', '💡']):
                            print(f"   {line}")
                return True
            else:
                print(f"❌ {script_name} failed with return code {result.returncode}")
                if result.stderr:
                    print(f"   Error: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"❌ {script_name} timed out")
            return False
        except Exception as e:
            print(f"❌ Error running {script_name}: {e}")
            return False
    
    def update_files(self, changed_files: list) -> None:
        """Update HTML and LaTeX files."""
        print(f"\n📝 Files changed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   Changed: {', '.join(changed_files)}")
        print("🔄 Regenerating files...")
        
        # Generate HTML pages
        html_success = self.run_script("generate_html.py")
        
        # Generate LaTeX CV using configurable generator
        latex_success = self.run_script("generate_cv_configurable.py")
        
        # Compile PDF if LaTeX generation was successful
        if latex_success:
            print("📄 Compiling PDF...")
            pdf_success = self.compile_pdf()
            if pdf_success:
                print("✅ PDF compiled successfully")
            else:
                print("⚠️  PDF compilation failed (LaTeX may not be installed)")
        
        if html_success and latex_success:
            print("🎉 All files updated successfully!")
        else:
            print("⚠️  Some files failed to update")
        
        self.last_update = datetime.now()
    
    def compile_pdf(self) -> bool:
        """Compile LaTeX to PDF."""
        try:
            # Run pdflatex twice for proper cross-references
            for i in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', 'CV.tex'],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode != 0:
                    return False
            
            # Clean up auxiliary files
            aux_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls']
            for ext in aux_extensions:
                aux_file = f"CV{ext}"
                if os.path.exists(aux_file):
                    os.remove(aux_file)
            
            return True
            
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            return False
    
    def show_current_config(self) -> None:
        """Show current CV configuration."""
        try:
            import json
            with open(self.config_file, 'r') as f:
                config = json.load(f)
            
            print("\n📋 Current CV Configuration:")
            for section, enabled in config.get('cv_sections', {}).items():
                status = "✅ Enabled" if enabled else "❌ Disabled"
                print(f"   {section.title()}: {status}")
            
            settings = config.get('cv_settings', {})
            if any(v for v in settings.values() if v is not None):
                print("\n⚙️  CV Settings:")
                for key, value in settings.items():
                    if value is not None:
                        print(f"   {key}: {value}")
        
        except (FileNotFoundError, json.JSONDecodeError):
            print("⚠️  No configuration found - using defaults")
    
    def watch(self, interval: int = 2) -> None:
        """Watch for file changes and update accordingly."""
        print(f"👀 Watching for changes in:")
        print(f"   📄 {self.data_file}")
        print(f"   ⚙️  {self.config_file}")
        print("📍 Press Ctrl+C to stop watching\n")
        
        self.show_current_config()
        print(f"\n💡 Edit {self.config_file} to control which sections appear in your CV")
        print(f"💡 Edit {self.data_file} to update your content")
        print(f"\n👀 Monitoring started at {datetime.now().strftime('%H:%M:%S')}...")
        
        try:
            while True:
                changed, changed_files = self.files_changed()
                if changed:
                    self.update_files(changed_files)
                    print(f"\n👀 Resuming watch at {datetime.now().strftime('%H:%M:%S')}...")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopped watching for changes")
    
    def force_update(self) -> None:
        """Force update all files regardless of changes."""
        print("🔄 Force updating all files...")
        self.update_files([self.data_file, self.config_file])

def check_dependencies() -> bool:
    """Check if required dependencies are available."""
    dependencies = {
        'jinja2': 'pip install jinja2'
    }
    
    missing = []
    
    try:
        import jinja2
    except ImportError:
        missing.append('jinja2')
    
    if missing:
        print("❌ Missing dependencies:")
        for dep in missing:
            print(f"   - {dep}: {dependencies[dep]}")
        return False
    
    return True

def main():
    """Main function."""
    if not check_dependencies():
        return
    
    updater = ConfigurableAutoUpdater()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--force" or sys.argv[1] == "-f":
            updater.force_update()
            return
        elif sys.argv[1] == "--config" or sys.argv[1] == "-c":
            updater.show_current_config()
            return
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Configurable Auto Update Script")
            print("Usage:")
            print("  python auto_update_configurable.py           # Watch for changes")
            print("  python auto_update_configurable.py --force   # Force update all files")
            print("  python auto_update_configurable.py --config  # Show current config")
            print("  python auto_update_configurable.py --help    # Show this help")
            print("\nConfiguration:")
            print("  Edit cv-config.json to control which sections appear in your CV")
            print("  Edit cv-data.json to update your content")
            return
    
    # Check if data file exists
    if not os.path.exists(updater.data_file):
        print(f"❌ Data file {updater.data_file} not found!")
        print("Please create the data file first.")
        return
    
    # Create default config if it doesn't exist
    if not os.path.exists(updater.config_file):
        print(f"⚙️  Creating default configuration file: {updater.config_file}")
        # This will be created automatically by the configurable generator
        try:
            from generate_cv_configurable import ConfigurableCVGenerator
            generator = ConfigurableCVGenerator()  # This creates the config file
        except ImportError:
            print("❌ generate_cv_configurable.py not found!")
            return
    
    # Start watching
    updater.watch()

if __name__ == "__main__":
    main()
