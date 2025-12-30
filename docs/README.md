# benmola.github.io - Personal Portfolio Website

## Project Structure

```
benmola.github.io/
├── index.html              # Main landing page (kept at root for GitHub Pages)
├── src/                    # Source files
│   ├── css/               # Stylesheets
│   │   └── styles.css     # Main stylesheet
│   ├── components/        # Reusable HTML components
│   │   └── sidebar.html   # Sidebar template
│   └── js/                # JavaScript files
├── pages/                  # Individual page files
│   ├── publications.html
│   ├── education.html
│   ├── experience.html
│   ├── projects.html
│   └── skills.html
├── data/                   # JSON data files
│   ├── cv_data.json       # CV/resume data
│   └── publications.json  # Publications list
├── scripts/                # Python scripts
│   ├── generate_cv.py             # Basic CV generator
│   ├── tailored_cv_generator.py   # AI-powered tailored CV generator
│   └── requirements.txt           # Python dependencies
├── cv/                     # CV files
│   ├── CV.tex             # LaTeX source
│   └── CV.pdf             # Generated PDF
├── images/                 # Image assets
│   └── MyPhoto.png
└── docs/                   # Documentation
    └── README.md          # This file
```

## Tailored CV Generator

The `tailored_cv_generator.py` script creates customized CVs based on job descriptions.

### Usage

```bash
# Using a job description file
python scripts/tailored_cv_generator.py --job-description job_posting.txt

# Interactive mode
python scripts/tailored_cv_generator.py --interactive

# With options
python scripts/tailored_cv_generator.py -j job.txt -o CV_for_company.tex --max-projects 3
```

### Features

- **Keyword extraction**: Identifies relevant skills, technologies, and domains from job descriptions
- **Relevance scoring**: Scores experiences and projects based on keyword matches
- **Automatic prioritization**: Reorders CV sections to highlight most relevant content
- **Skill highlighting**: Bolds matching skills in the output

## Development

### Local Preview

Open `index.html` directly in a browser or use a local server:

```bash
python -m http.server 8000
```

Then visit `http://localhost:8000`

### Updating Publications

1. Edit `data/publications.json` to add new publications
2. Run the appropriate update script to regenerate HTML

### Generating CV

```bash
cd scripts
python generate_cv.py  # Basic CV
python tailored_cv_generator.py -i  # Tailored CV with job matching
```

## Technologies

- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Icons**: Font Awesome, Academicons
- **Python**: CV generation scripts
- **LaTeX**: CV document compilation
