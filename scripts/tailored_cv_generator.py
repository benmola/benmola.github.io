#!/usr/bin/env python3
"""
Tailored CV LaTeX Generator
Generates a customized CV.tex based on job description matching.
Uses keyword extraction and relevance scoring to prioritize content.

Usage:
    python tailored_cv_generator.py --job-description job_posting.txt
    python tailored_cv_generator.py --interactive
    python tailored_cv_generator.py --job-description job_posting.txt --output CV_tailored.tex
"""

import json
import os
import re
import argparse
from datetime import datetime
from typing import Dict, List, Any, Tuple
from collections import Counter

class TailoredCVGenerator:
    """Generates tailored CV based on job description matching."""
    
    # Define keyword categories for matching
    SKILL_KEYWORDS = {
        'programming': [
            'python', 'matlab', 'simulink', 'c++', 'c#', 'java', 'javascript',
            'r', 'julia', 'sql', 'pytorch', 'tensorflow', 'keras', 'scikit-learn',
            'pandas', 'numpy', 'scipy', 'pyomo', 'gurobi', 'cplex'
        ],
        'machine_learning': [
            'machine learning', 'ml', 'deep learning', 'neural network', 'lstm',
            'gaussian process', 'bayesian', 'optimization', 'reinforcement learning',
            'supervised learning', 'unsupervised learning', 'regression', 'classification',
            'data-driven', 'data driven', 'ai', 'artificial intelligence'
        ],
        'control': [
            'control', 'mpc', 'model predictive control', 'pid', 'feedback',
            'state estimation', 'kalman filter', 'observer', 'controller',
            'automation', 'automatics', 'dynamical systems', 'system identification'
        ],
        'process_engineering': [
            'biogas', 'anaerobic digestion', 'bioenergy', 'renewable energy',
            'process optimization', 'process modelling', 'process modeling',
            'cfd', 'adm1', 'am2', 'chemostat', 'bioreactor', 'digester',
            'htc', 'hydrothermal', 'waste treatment', 'bioprocess'
        ],
        'data_science': [
            'data science', 'data analysis', 'statistics', 'time series',
            'forecasting', 'prediction', 'modelling', 'modeling', 'simulation',
            'dmd', 'dynamic mode decomposition', 'koopman', 'sindy'
        ],
        'research': [
            'research', 'phd', 'publication', 'journal', 'conference',
            'academic', 'thesis', 'dissertation', 'paper', 'manuscript'
        ],
        'industry': [
            'industry', 'industrial', 'commercial', 'scale-up', 'pilot',
            'plant', 'operations', 'real-time', 'deployment', 'production'
        ],
        'soft_skills': [
            'communication', 'teamwork', 'collaboration', 'leadership',
            'presentation', 'teaching', 'mentoring', 'project management'
        ]
    }
    
    def __init__(self, data_file: str = "../data/cv_data.json"):
        """Initialize the generator with data file."""
        self.data_file = data_file
        self.data = self.load_data()
        self.job_keywords = {}
        self.keyword_scores = Counter()
        
    def load_data(self) -> Dict[str, Any]:
        """Load CV data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file {self.data_file} not found")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.data_file}: {e}")
    
    def extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """Extract relevant keywords from job description."""
        text_lower = text.lower()
        found_keywords = {category: [] for category in self.SKILL_KEYWORDS}
        
        for category, keywords in self.SKILL_KEYWORDS.items():
            for keyword in keywords:
                # Use word boundary for better matching
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    found_keywords[category].append(keyword)
                    self.keyword_scores[category] += 1
        
        return found_keywords
    
    def calculate_relevance(self, item_text: str, weights: Dict[str, float] = None) -> float:
        """Calculate relevance score for an item based on keyword matching."""
        if weights is None:
            weights = {cat: 1.0 for cat in self.SKILL_KEYWORDS}
        
        item_lower = item_text.lower()
        score = 0.0
        
        for category, keywords in self.job_keywords.items():
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, item_lower))
                score += matches * weights.get(category, 1.0)
        
        return score
    
    def score_experience(self, exp: Dict) -> float:
        """Score an experience entry based on relevance."""
        text = f"{exp.get('position', '')} {exp.get('organization', '')} "
        text += f"{exp.get('description', '')} "
        text += " ".join(exp.get('responsibilities', []))
        return self.calculate_relevance(text)
    
    def score_project(self, project: Dict) -> float:
        """Score a project based on relevance."""
        text = f"{project.get('title', '')} {project.get('description', '')} "
        text += f"{project.get('organization', '')}"
        return self.calculate_relevance(text)
    
    def score_publication(self, pub: Dict) -> float:
        """Score a publication based on relevance."""
        text = f"{pub.get('title', '')} {pub.get('abstract', '')} "
        text += f"{pub.get('venue', '')}"
        return self.calculate_relevance(text)
    
    def sort_by_relevance(self, items: List[Dict], scorer_func) -> List[Tuple[Dict, float]]:
        """Sort items by relevance score."""
        scored = [(item, scorer_func(item)) for item in items]
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    def escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        if not isinstance(text, str):
            return str(text)
        
        replacements = {
            '&': r'\&',
            '%': r'\%',
            '$': r'\$',
            '#': r'\#',
            '^': r'\textasciicircum{}',
            '_': r'\_',
            '{': r'\{',
            '}': r'\}',
            '~': r'\textasciitilde{}',
            '\\': r'\textbackslash{}'
        }
        
        result = text
        for char, replacement in replacements.items():
            result = result.replace(char, replacement)
        
        return result
    
    def format_date_range(self, start: str, end: str) -> str:
        """Format date range for LaTeX."""
        if end.lower() == 'present':
            return f"{start}--Present"
        return f"{start}--{end}"
    
    def generate_tailored_about(self) -> str:
        """Generate a tailored About Me section based on matched keywords."""
        about = self.data['personal']['about']
        
        section = "\\section{About Me}\n"
        section += f"\\cvitem{{}}{{\\textit{{{self.escape_latex(about)}}}}}\n\n"
        
        # Add a note about tailored skills if we have keyword matches
        if self.keyword_scores:
            top_categories = self.keyword_scores.most_common(3)
            if top_categories:
                skills_highlight = ", ".join([
                    cat.replace('_', ' ').title() 
                    for cat, _ in top_categories
                ])
                section += f"% Tailored for: {skills_highlight}\n\n"
        
        return section
    
    def generate_header(self) -> str:
        """Generate LaTeX document header."""
        personal = self.data['personal']
        
        header = r"""\documentclass[11pt,a4paper]{moderncv}
\moderncvstyle{classic}
\moderncvcolor{blue}
\usepackage[scale=0.8]{geometry}
\usepackage{multicol}
\usepackage{academicons}
\usepackage{lmodern}

% Personal Information
"""
        
        header += f"\\name{{{self.escape_latex(personal['name']['first'])}}}{{{self.escape_latex(personal['name']['last'])}}}\n"
        header += f"\\title{{{self.escape_latex(personal['title'])}}}\n"
        
        # Contact information
        contact = personal['contact']
        social = personal['social']
        
        header += "\\extrainfo{\n"
        header += f"    \\faEnvelope\\enspace\\href{{mailto:{contact['email_surrey']}}}{{{contact['email_surrey']}}} \\quad \n"
        header += f"    \\faMobile\\enspace{contact['phone']} \\quad\n"
        header += f"    \\faGlobe\\enspace\\href{{{contact['website']}}}{{Webpage}} \\\\\n"
        header += f"    \\faGraduationCap\\enspace\\href{{{social['google_scholar']}}}{{Google Scholar}} \\quad\n"
        header += f"    \\faResearchgate\\enspace\\href{{{social['researchgate']}}}{{ResearchGate}} \\quad\n"
        header += f"    \\faLinkedin\\enspace\\href{{{social['linkedin']}}}{{LinkedIn}} \\quad\n"
        header += f"    \\faGithub\\enspace\\href{{{social['github']}}}{{GitHub}}\n"
        header += "}\n\n"
        
        header += "\\begin{document}\n\n\\makecvtitle\n\n"
        
        return header
    
    def generate_experience_section(self, max_items: int = None) -> str:
        """Generate tailored Work Experience section."""
        section = "\\section{Work Experience}\n"
        
        # Score and sort experiences
        scored_exp = self.sort_by_relevance(self.data['experience'], self.score_experience)
        
        if max_items:
            scored_exp = scored_exp[:max_items]
        
        for exp, score in scored_exp:
            date_range = self.format_date_range(exp['start_date'], exp['end_date'])
            position = self.escape_latex(exp['position'])
            organization = self.escape_latex(exp['organization'])
            location = self.escape_latex(exp['location'])
            
            # Add relevance indicator as a comment
            section += f"% Relevance score: {score:.2f}\n"
            section += f"\\cventry{{{date_range}}}{{{position}}}{{{organization}}}{{{location}}}{{}}{{\\begin{{itemize}}"
            
            for responsibility in exp['responsibilities']:
                section += f"\\item {self.escape_latex(responsibility)}"
            
            section += "\\end{itemize}}\n"
        
        return section
    
    def generate_education_section(self) -> str:
        """Generate Education section."""
        section = "\\section{Education}\n"
        
        for edu in self.data['education']:
            date_range = self.format_date_range(edu['start_date'], edu['end_date'])
            degree = self.escape_latex(edu['degree'])
            institution = self.escape_latex(edu['institution'])
            location = self.escape_latex(edu['location'])
            
            section += f"\\cventry{{{date_range}}}{{{degree}}}{{{institution}}}{{{location}}}{{}}{{\\\n"
            
            if 'thesis' in edu:
                thesis = self.escape_latex(edu['thesis'])
                section += f"\\textbf{{Thesis:}} ``{thesis}''\\\\\\\n"
            
            if 'supervisors' in edu:
                supervisors = " \\& ".join([self.escape_latex(sup) for sup in edu['supervisors']])
                section += f"\\textbf{{Supervisors:}} {supervisors}\\\\\\\n"
            
            if 'co_direction' in edu:
                co_direction = self.escape_latex(edu['co_direction'])
                section += f"\\textbf{{Co-direction:}} {co_direction}\\\\\\\n"
            
            if 'mobility' in edu:
                section += "\\textbf{International Mobility:}\\\n\\begin{itemize}\\\n"
                for mobility in edu['mobility']:
                    section += f"\\item {self.escape_latex(mobility)}\\\n"
                section += "\\end{itemize}\\\n"
            
            section += "}\n"
        
        return section
    
    def generate_projects_section(self, max_items: int = None) -> str:
        """Generate tailored Research Projects section."""
        section = "\\section{Research Projects}\n"
        
        # Score and sort projects
        scored_projects = self.sort_by_relevance(self.data['projects'], self.score_project)
        
        if max_items:
            scored_projects = scored_projects[:max_items]
        
        for project, score in scored_projects:
            date_range = self.format_date_range(project['start_date'], project['end_date'])
            title = self.escape_latex(project['title'])
            organization = self.escape_latex(project['organization'])
            description = self.escape_latex(project['description'])
            
            section += f"% Relevance score: {score:.2f}\n"
            section += f"\\cventry{{{date_range}}}{{{title}}}{{{organization}}}{{}}{{}}{{\\\n{description}\\\n}}\\\n"
        
        return section
    
    def generate_skills_section(self) -> str:
        """Generate Technical Skills section with relevant skills emphasized."""
        section = "\\section{Technical Skills}\n"
        skills = self.data['skills']
        
        # Emphasize skills that match job keywords
        def format_skills(skill_list: List[str]) -> str:
            formatted = []
            for skill in skill_list:
                skill_lower = skill.lower()
                is_relevant = False
                for keywords in self.job_keywords.values():
                    for kw in keywords:
                        if kw in skill_lower:
                            is_relevant = True
                            break
                    if is_relevant:
                        break
                
                if is_relevant:
                    formatted.append(f"\\textbf{{{self.escape_latex(skill)}}}")
                else:
                    formatted.append(self.escape_latex(skill))
            return ", ".join(formatted)
        
        section += "\\cvitem{Process Engineering}{" + format_skills(skills['process_engineering']) + "}\n"
        section += "\\cvitem{Data Science}{" + format_skills(skills['data_science']) + "}\n"
        section += "\\cvitem{Programming}{" + format_skills(skills['programming']) + "}\n"
        section += "\\cvitem{Languages}{" + format_skills(skills['languages']) + "}\n\n"
        
        return section
    
    def generate_hobbies_section(self) -> str:
        """Generate Hobbies & Interests section."""
        section = "\\section{Hobbies \\& Interests}\n"
        hobbies = self.data['hobbies']
        
        for category, items in hobbies.items():
            category_title = category.replace('_', ' ').title()
            section += f"\\cvitem{{{category_title}: }}{{{self.escape_latex(items)}}}\\\n"
        
        return section
    
    def generate_footer(self) -> str:
        """Generate LaTeX document footer."""
        return "\\end{document}\n"
    
    def generate_matching_report(self) -> str:
        """Generate a report of keyword matching statistics."""
        report = "\n" + "="*60 + "\n"
        report += "CV TAILORING REPORT\n"
        report += "="*60 + "\n\n"
        
        report += "MATCHED KEYWORD CATEGORIES:\n"
        report += "-"*40 + "\n"
        
        if not self.keyword_scores:
            report += "No keywords matched from job description.\n"
        else:
            for category, count in self.keyword_scores.most_common():
                keywords = self.job_keywords.get(category, [])
                report += f"\n{category.replace('_', ' ').title()}: {count} matches\n"
                if keywords:
                    report += f"  Keywords: {', '.join(keywords)}\n"
        
        report += "\n" + "="*60 + "\n"
        return report
    
    def generate_tailored_cv(self, job_description: str, 
                              max_experience: int = None,
                              max_projects: int = None) -> str:
        """Generate complete tailored LaTeX CV."""
        
        # Extract keywords from job description
        self.job_keywords = self.extract_keywords(job_description)
        
        # Build the CV
        latex_content = ""
        latex_content += self.generate_header()
        latex_content += self.generate_tailored_about()
        latex_content += self.generate_experience_section(max_experience)
        latex_content += self.generate_education_section()
        latex_content += self.generate_projects_section(max_projects)
        latex_content += self.generate_skills_section()
        latex_content += self.generate_hobbies_section()
        latex_content += self.generate_footer()
        
        return latex_content
    
    def save_tailored_cv(self, job_description: str, 
                         output_file: str = "CV_tailored.tex",
                         max_experience: int = None,
                         max_projects: int = None) -> None:
        """Generate and save tailored CV."""
        
        latex_content = self.generate_tailored_cv(
            job_description, 
            max_experience, 
            max_projects
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"✅ Tailored CV generated: {output_file}")
        print(self.generate_matching_report())


def get_interactive_job_description() -> str:
    """Get job description interactively from user."""
    print("\n" + "="*60)
    print("TAILORED CV GENERATOR")
    print("="*60)
    print("\nEnter the job description (paste or type).")
    print("When finished, enter a blank line or type 'END' on a new line.\n")
    
    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == 'END' or (not line.strip() and lines):
                break
            lines.append(line)
        except EOFError:
            break
    
    return '\n'.join(lines)


def main():
    """Main function to generate tailored CV."""
    parser = argparse.ArgumentParser(
        description='Generate a tailored CV based on job description matching.'
    )
    parser.add_argument(
        '--job-description', '-j',
        type=str,
        help='Path to job description file (text file)'
    )
    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Enter job description interactively'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default='CV_tailored.tex',
        help='Output file name (default: CV_tailored.tex)'
    )
    parser.add_argument(
        '--data', '-d',
        type=str,
        default=None,
        help='Path to CV data JSON file (default: ../data/cv_data.json relative to script)'
    )
    parser.add_argument(
        '--max-experience',
        type=int,
        default=None,
        help='Maximum number of experience entries to include'
    )
    parser.add_argument(
        '--max-projects',
        type=int,
        default=None,
        help='Maximum number of projects to include'
    )
    parser.add_argument(
        '--compile-pdf',
        action='store_true',
        help='Compile the generated LaTeX to PDF'
    )
    
    args = parser.parse_args()
    
    # Get job description
    job_description = ""
    
    if args.job_description:
        try:
            with open(args.job_description, 'r', encoding='utf-8') as f:
                job_description = f.read()
            print(f"📄 Loaded job description from: {args.job_description}")
        except FileNotFoundError:
            print(f"❌ Error: File not found: {args.job_description}")
            return
    elif args.interactive:
        job_description = get_interactive_job_description()
    else:
        print("❌ Error: Please specify either --job-description or --interactive")
        print("Usage examples:")
        print("  python tailored_cv_generator.py --job-description job.txt")
        print("  python tailored_cv_generator.py --interactive")
        return
    
    if not job_description.strip():
        print("❌ Error: Empty job description provided")
        return
    
    try:
        # Resolve data file path
        data_file = args.data
        if data_file is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(script_dir, "..", "data", "cv_data.json")
        
        generator = TailoredCVGenerator(data_file=data_file)
        generator.save_tailored_cv(
            job_description=job_description,
            output_file=args.output,
            max_experience=args.max_experience,
            max_projects=args.max_projects
        )
        
        if args.compile_pdf:
            compile_pdf(args.output)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def compile_pdf(tex_file: str) -> bool:
    """Compile LaTeX to PDF using pdflatex."""
    try:
        import subprocess
        
        print(f"\n📄 Compiling {tex_file} to PDF...")
        
        # Run pdflatex twice for proper cross-references
        for i in range(2):
            result = subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', tex_file],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print(f"❌ LaTeX compilation failed (attempt {i+1})")
                return False
        
        # Clean up auxiliary files
        base_name = tex_file.replace('.tex', '')
        aux_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls']
        
        for ext in aux_extensions:
            aux_file = base_name + ext
            if os.path.exists(aux_file):
                os.remove(aux_file)
        
        print(f"✅ PDF compiled successfully: {base_name}.pdf")
        return True
        
    except FileNotFoundError:
        print("⚠️  pdflatex not found. Please install LaTeX to compile PDF.")
        return False
    except Exception as e:
        print(f"❌ Error compiling PDF: {e}")
        return False


if __name__ == "__main__":
    main()
