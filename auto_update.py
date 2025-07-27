#!/usr/bin/env python3
"""
Auto Update Script
Watches for changes in cv-data.json and automatically regenerates HTML and LaTeX files
"""

import os
import sys
import time
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

class AutoUpdater:
    def __init__(self, data_file: str = "cv-data.json"):
        """Initialize the auto updater."""
        self.data_file = data_file
        self.last_hash = self.get_file_hash()
        self.last_update = datetime.now()
        
    def get_file_hash(self) -> str:
        """Get MD5 hash of the data file."""
        try:
            with open(self.data_file, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except FileNotFoundError:
            return ""
    
    def file_changed(self) -> bool:
        """Check if the data file has changed."""
        current_hash = self.get_file_hash()
        if current_hash != self.last_hash:
            self.last_hash = current_hash
            return True
        return False
    
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
                print(f"✓ {script_name} executed successfully")
                if result.stdout:
                    print(f"  Output: {result.stdout.strip()}")
                return True
            else:
                print(f"✗ {script_name} failed with return code {result.returncode}")
                if result.stderr:
                    print(f"  Error: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            print(f"✗ {script_name} timed out")
            return False
        except Exception as e:
            print(f"✗ Error running {script_name}: {e}")
            return False
    
    def update_files(self) -> None:
        """Update HTML and LaTeX files."""
        print(f"\n📝 Data file changed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔄 Regenerating files...")
        
        # Generate HTML pages
        html_success = self.run_script("generate_html.py")
        
        # Generate LaTeX CV
        latex_success = self.run_script("generate_cv.py")
        
        # Compile PDF if LaTeX generation was successful
        if latex_success:
            print("📄 Compiling PDF...")
            pdf_success = self.compile_pdf()
            if pdf_success:
                print("✓ PDF compiled successfully")
            else:
                print("✗ PDF compilation failed")
        
        if html_success and latex_success:
            print("🎉 All files updated successfully!")
        else:
            print("⚠️ Some files failed to update")
        
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
    
    def watch(self, interval: int = 2) -> None:
        """Watch for file changes and update accordingly."""
        print(f"👀 Watching {self.data_file} for changes...")
        print("📍 Press Ctrl+C to stop watching\n")
        
        try:
            while True:
                if self.file_changed():
                    self.update_files()
                    print(f"\n👀 Resuming watch at {datetime.now().strftime('%H:%M:%S')}...")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n🛑 Stopped watching for changes")
    
    def force_update(self) -> None:
        """Force update all files regardless of changes."""
        print("🔄 Force updating all files...")
        self.update_files()

def check_dependencies() -> bool:
    """Check if required dependencies are available."""
    dependencies = {
        'jinja2': 'pip install jinja2',
        'watchdog': 'pip install watchdog (optional, for improved file watching)'
    }
    
    missing = []
    
    try:
        import jinja2
    except ImportError:
        missing.append('jinja2')
    
    if missing:
        print("❌ Missing dependencies:")
        for dep in missing:
            print(f"  - {dep}: {dependencies[dep]}")
        return False
    
    return True

def main():
    """Main function."""
    if not check_dependencies():
        return
    
    updater = AutoUpdater()
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--force" or sys.argv[1] == "-f":
            updater.force_update()
            return
        elif sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print("Auto Update Script")
            print("Usage:")
            print("  python auto_update.py          # Watch for changes")
            print("  python auto_update.py --force  # Force update all files")
            print("  python auto_update.py --help   # Show this help")
            return
    
    # Check if data file exists
    if not os.path.exists(updater.data_file):
        print(f"❌ Data file {updater.data_file} not found!")
        print("Please create the data file first.")
        return
    
    # Start watching
    updater.watch()

if __name__ == "__main__":
    main()
