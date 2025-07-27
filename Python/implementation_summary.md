# CV-Website Synchronization System Implementation

## 🎯 What I've Created

I've built a comprehensive automated system that synchronizes your CV.tex file with your website content using a **single source of truth** approach. Here's what the system includes:

## 📦 Complete File Set

### 1. **cv-data.json** - Single Source of Truth
- Contains all your personal information, experience, education, projects, publications, activities, and skills
- JSON format for easy editing and parsing
- Structured to feed both HTML and LaTeX generators

### 2. **generate_cv.py** - LaTeX CV Generator
- Reads cv-data.json and generates CV.tex automatically
- Handles LaTeX escaping and formatting
- Supports PDF compilation
- Maintains the same structure as your original CV

### 3. **generate_html.py** - HTML Pages Generator  
- Creates all your HTML pages from cv-data.json
- Uses Jinja2 templating for flexible customization
- Generates: home.html, education.html, experience.html, projects.html, publications.html, skills.html (with activities)
- Maintains your existing styling and design

### 4. **auto_update.py** - Automatic File Watcher
- Monitors cv-data.json for changes
- Automatically regenerates HTML and LaTeX when data changes
- Compiles PDF automatically
- Provides real-time updates

### 5. **setup.py** - Quick Setup Script
- Automates the initial setup process
- Checks dependencies and system requirements
- Validates configuration
- Tests file generation

### 6. **requirements.txt** - Dependencies
- Lists all required Python packages
- Ensures consistent environment setup

### 7. **README.md** - Comprehensive Documentation
- Step-by-step setup instructions
- Usage examples and workflows
- Troubleshooting guide
- Advanced features and customization

## 🔄 How It Works

```
cv-data.json (Single Source)
     │
     ├── generate_html.py → HTML Pages (website)
     │
     └── generate_cv.py → CV.tex → CV.pdf
```

### The Workflow:
1. **Edit cv-data.json** with your updated information
2. **Auto-detection** - The system detects changes automatically
3. **HTML Generation** - Updates all website pages
4. **LaTeX Generation** - Updates CV.tex with the same information
5. **PDF Compilation** - Automatically compiles CV.pdf
6. **File Cleanup** - Removes temporary LaTeX files

## 🚀 Getting Started

### Quick Setup (3 steps):

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run setup:**
   ```bash
   python setup.py
   ```

3. **Start auto-update:**
   ```bash
   python auto_update.py
   ```

### Manual Usage:
```bash
# Update HTML pages only
python generate_html.py

# Update CV.tex and PDF only  
python generate_cv.py

# Force update everything
python auto_update.py --force
```

## ✨ Key Benefits

### 🎯 **Single Source of Truth**
- No more maintaining duplicate information
- One JSON file controls everything
- Eliminates synchronization errors

### ⚡ **Real-time Updates**
- Change cv-data.json → Everything updates automatically
- No manual file copying or updating
- Instant preview of changes

### 🔒 **Consistency Guaranteed**
- Website and CV always match
- Same data formatting everywhere
- Professional consistency maintained

### 🛠️ **Easy Maintenance**
- Simple JSON editing
- Clear structure and organization
- Version control friendly

### 📱 **Modern Workflow**
- Git-friendly (track changes in cv-data.json)
- CI/CD ready (can automate deployments)
- Professional development practices

## 📝 Example: Adding New Activity

Instead of updating multiple files, just edit cv-data.json:

```json
{
  "activities": [
    {
      "date": "15-16 March 2025",
      "event": "International Bioenergy Conference 2025",
      "location": "Berlin, Germany",
      "type": "conference",
      "description": "Presented research on AI-driven biogas optimization and attended sessions on renewable energy innovations."
    }
  ]
}
```

**Result**: The activity appears on your website automatically. If you enable activities in your CV config, it will appear there too - with full control over how many activities to show.

## 🔧 Advanced Features

### GitHub Actions Integration
- Automatic updates when you push changes to cv-data.json
- Deploy updated website automatically
- Generate and commit new CV.pdf

### Customization Options
- Modify HTML templates in generate_html.py
- Adjust LaTeX formatting in generate_cv.py
- Add new sections or pages easily
- Custom CSS styling support

### Monitoring and Logging
- Real-time file watching
- Error reporting and debugging
- Success confirmations
- File change notifications

## 🎯 What This Solves

### Before (Your Current Problem):
- ❌ Manually update CV.tex when website changes
- ❌ Risk of inconsistencies between website and CV
- ❌ Tedious duplicate data entry
- ❌ Forgetting to update one or the other
- ❌ Manual PDF generation

### After (With This System):
- ✅ Edit one file (cv-data.json) 
- ✅ Everything updates automatically
- ✅ Perfect synchronization guaranteed
- ✅ Professional workflow
- ✅ Automatic PDF generation

## 🚀 Future Enhancements

The system is designed to be extensible. You could add:

- **Web-based editor** for cv-data.json
- **Multiple CV templates** (academic, industry, etc.)
- **Multiple output formats** (Word, HTML, etc.)
- **Publication import** from ORCID/Google Scholar
- **Social media integration**
- **Analytics and tracking**

## 💡 Technical Architecture

The system follows modern software development principles:

- **Separation of Concerns**: Data, templates, and generation logic are separate
- **DRY (Don't Repeat Yourself)**: Single source of truth eliminates duplication
- **Modularity**: Each component has a specific responsibility
- **Extensibility**: Easy to add new features or modify existing ones
- **Maintainability**: Clear code structure and comprehensive documentation

This creates a robust, professional system that will save you significant time and ensure your CV and website are always perfectly synchronized.

---

**🎉 You now have a professional-grade automated CV and website synchronization system!**