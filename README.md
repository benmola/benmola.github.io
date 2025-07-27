# Automated CV and Website Synchronization System

This system automatically synchronizes your CV.tex file with your website content, ensuring that whenever you update your website, your CV is automatically updated and a new PDF is generated.

## 🚀 Features

- **Single Source of Truth**: All your data is stored in one JSON file
- **Automatic Synchronization**: Changes in data automatically update both HTML and LaTeX
- **PDF Generation**: Automatically compiles LaTeX to PDF
- **File Watching**: Monitors changes and updates files in real-time
- **Template-Based**: Easy to customize and extend

## 📁 File Structure

```
Webpage-project/
├── cv-data.json          # Single source of data
├── generate_cv.py        # LaTeX CV generator
├── generate_html.py      # HTML pages generator
├── auto_update.py        # Auto-update watcher
├── requirements.txt      # Python dependencies
├── assets/
│   └── styles.css       # CSS styles
├── MyPhoto.png          # Your photo
├── CV.tex               # Generated LaTeX file
├── CV.pdf               # Generated PDF file
├── home.html            # Generated HTML pages
├── education.html
├── experience.html
├── projects.html
├── publications.html
├── skills.html
└── index.html
```

## 🛠️ Setup Instructions

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install LaTeX (for PDF generation)

**On Ubuntu/Debian:**
```bash
sudo apt-get install texlive-latex-extra texlive-fonts-recommended
```

**On macOS:**
```bash
brew install --cask mactex
```

**On Windows:**
- Download and install [MiKTeX](https://miktex.org/) or [TeX Live](https://www.tug.org/texlive/)

### 3. Prepare Your Data

1. **Create or update `cv-data.json`** with your information (see the provided template)
2. **Add your photo** as `MyPhoto.png` in the root directory
3. **Customize CSS** in `assets/styles.css` if needed

### 4. Generate Initial Files

```bash
# Generate HTML pages
python generate_html.py

# Generate LaTeX CV
python generate_cv.py

# Compile PDF (if you have LaTeX installed)
# This is optional - the CV generator can do this automatically
```

## 🔄 Usage

### Option 1: Manual Generation

Update your `cv-data.json` file and run:

```bash
python generate_html.py  # Updates HTML pages
python generate_cv.py    # Updates CV.tex and optionally compiles PDF
```

### Option 2: Automatic Watching (Recommended)

Start the auto-update watcher:

```bash
python auto_update.py
```

Now, whenever you modify `cv-data.json`, the system will automatically:
1. Regenerate all HTML pages
2. Update CV.tex
3. Compile the PDF
4. Clean up temporary files

### Option 3: Force Update

To force update all files regardless of changes:

```bash
python auto_update.py --force
```

## 📝 Editing Your Data

### Adding New Experience

Edit `cv-data.json` and add to the `experience` array:

```json
{
  "position": "Your New Position",
  "organization": "Company Name",
  "location": "City, Country",
  "start_date": "Jan 2024",
  "end_date": "Present",
  "description": "Brief description of the role",
  "responsibilities": [
    "First responsibility",
    "Second responsibility"
  ]
}
```

### Adding New Publications

Add to the `publications` array:

```json
{
  "title": "Your Paper Title",
  "authors": ["Your Name", "Co-author"],
  "venue": "Journal or Conference Name",
  "year": "2024",
  "doi": "https://doi.org/10.xxxx/xxxxx",
  "type": "journal"
}
```

### Adding New Projects

Add to the `projects` array:

```json
{
  "title": "Project Name",
  "organization": "Funding Organization",
  "start_date": "Jan 2024",
  "end_date": "Dec 2024",
  "description": "Project description",
  "status": "ongoing"
}
```

## 🎨 Customization

### HTML Templates

The HTML generator uses Jinja2 templates embedded in the code. To customize:

1. Edit the template strings in `generate_html.py`
2. Modify CSS in `assets/styles.css`
3. Update the base template structure as needed

### LaTeX Formatting

To customize the CV format:

1. Edit the LaTeX generation methods in `generate_cv.py`
2. Modify the document class, packages, or styling
3. Add new sections or change the layout

### Adding New Pages

To add a new page (e.g., "Awards"):

1. Add the data structure to `cv-data.json`
2. Create a new generation method in `generate_html.py`
3. Add the page to the navigation menu
4. Optionally add a corresponding section to the LaTeX generator

## 🔧 Troubleshooting

### Common Issues

**1. "pdflatex not found"**
- Install LaTeX as described in setup instructions
- Ensure `pdflatex` is in your system PATH

**2. "jinja2 not found"**
- Install dependencies: `pip install -r requirements.txt`

**3. "Permission denied" errors**
- Ensure you have write permissions in the directory
- Check that files aren't open in other applications

**4. PDF compilation fails**
- Check that all required LaTeX packages are installed
- Look at the LaTeX error messages for missing packages
- Try compiling manually: `pdflatex CV.tex`

### Debug Mode

For more verbose output, you can modify the scripts to include debug information:

```python
# Add to the beginning of any script
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📋 Workflow Examples

### Daily Workflow

1. **Update your data**: Edit `cv-data.json` with new information
2. **Auto-update**: If the watcher is running, files update automatically
3. **Review changes**: Check the generated HTML pages and PDF
4. **Commit changes**: Add all files to version control

### Publication Workflow

1. **Add publication**: Update the `publications` array in `cv-data.json`
2. **Verify formatting**: Check that the publication appears correctly on the publications page
3. **Update CV**: Ensure the publication is included in the PDF
4. **Deploy**: Upload updated files to your website

### Project Update Workflow

1. **Add/Update project**: Modify the `projects` array
2. **Check status**: Ensure project status is correctly reflected
3. **Update descriptions**: Keep project descriptions current
4. **Sync with website**: Verify changes appear on the projects page

## 🚀 Advanced Features

### GitHub Actions Integration

Create `.github/workflows/cv-update.yml`:

```yaml
name: Update CV
on:
  push:
    paths:
      - 'cv-data.json'
jobs:
  update-cv:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          sudo apt-get install texlive-latex-extra
      - name: Generate files
        run: |
          python generate_html.py
          python generate_cv.py
      - name: Commit changes
        run: |
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .
          git commit -m "Auto-update CV and website" || exit 0
          git push
```

### Docker Support

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    texlive-latex-extra \
    texlive-fonts-recommended \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "auto_update.py"]
```

### Web Interface

You could extend this system with a simple web interface for editing:

```python
# web_editor.py
from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

@app.route('/')
def editor():
    with open('cv-data.json', 'r') as f:
        data = json.load(f)
    return render_template('editor.html', data=data)

@app.route('/save', methods=['POST'])
def save_data():
    data = request.json
    with open('cv-data.json', 'w') as f:
        json.dump(data, f, indent=2)
    return jsonify({'status': 'saved'})

if __name__ == '__main__':
    app.run(debug=True)
```

## 📄 License

This system is open source and can be freely modified and distributed.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve this system.

---

**Happy CV updating! 🎉**