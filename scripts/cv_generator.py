#!/usr/bin/env python3
"""
CV Generator
Generates CV.tex and CV.pdf from cv_data.json
Supports both basic CV and tailored CV based on job description.

Usage:
    python cv_generator.py              # Interactive menu
    python cv_generator.py --basic      # Generate basic CV directly
    python cv_generator.py --tailored   # Generate tailored CV directly
"""

import json
import os
import re
import subprocess
import argparse
from typing import Dict, List, Any, Tuple
from collections import Counter


class CVGenerator:
    """Generates CV from JSON data with optional job description tailoring."""
    
    # Define keyword categories for matching (used in tailored mode)
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
    
    def __init__(self, data_file: str = None):
        """Initialize the generator with data file."""
        if data_file is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(script_dir, "..", "data", "cv_data.json")
        self.data_file = data_file
        self.data = self.load_data()
        self.job_keywords = {}
        self.keyword_scores = Counter()
        self.is_tailored = False
    
    def load_data(self) -> Dict[str, Any]:
        """Load CV data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file {self.data_file} not found")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.data_file}: {e}")
    
    def escape_latex(self, text: str) -> str:
        """Escape special LaTeX characters."""
        if not isinstance(text, str):
            return str(text)
        
        result = text
        replacements = [
            ('&', r'\&'),
            ('%', r'\%'),
            ('$', r'\$'),
            ('#', r'\#'),
            ('_', r'\_'),
            ('{', r'\{'),
            ('}', r'\}'),
            ('^', r'\^{}'),
            ('~', r'\~{}'),
        ]
        
        for char, replacement in replacements:
            result = result.replace(char, replacement)
        
        return result
    
    def format_date_range(self, start: str, end: str) -> str:
        """Format date range for LaTeX."""
        if end.lower() == 'present':
            return f"{start}--Present"
        return f"{start}--{end}"
    
    # ==================== Tailored Mode Methods ====================
    
    def extract_keywords(self, text: str) -> Dict[str, List[str]]:
        """Extract relevant keywords from job description."""
        text_lower = text.lower()
        found_keywords = {category: [] for category in self.SKILL_KEYWORDS}
        
        for category, keywords in self.SKILL_KEYWORDS.items():
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    found_keywords[category].append(keyword)
                    self.keyword_scores[category] += 1
        
        return found_keywords
    
    def calculate_relevance(self, item_text: str) -> float:
        """Calculate relevance score for an item based on keyword matching."""
        item_lower = item_text.lower()
        score = 0.0
        
        for category, keywords in self.job_keywords.items():
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = len(re.findall(pattern, item_lower))
                score += matches
        
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
    
    def sort_by_relevance(self, items: List[Dict], scorer_func) -> List[Tuple[Dict, float]]:
        """Sort items by relevance score."""
        scored = [(item, scorer_func(item)) for item in items]
        return sorted(scored, key=lambda x: x[1], reverse=True)
    
    # ==================== LaTeX Generation Methods ====================
    
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
    
    def generate_about_section(self) -> str:
        """Generate About Me section."""
        about = self.escape_latex(self.data['personal']['about'])
        
        section = "\\section{About Me}\n"
        section += f"\\cvitem{{}}{{\\textit{{{about}}}}}\n\n"
        
        if self.is_tailored and self.keyword_scores:
            top_categories = self.keyword_scores.most_common(3)
            if top_categories:
                skills_highlight = ", ".join([
                    cat.replace('_', ' ').title() 
                    for cat, _ in top_categories
                ])
                section += f"% Tailored for: {skills_highlight}\n\n"
        
        return section
    
    def generate_experience_section(self) -> str:
        """Generate Work Experience section."""
        section = "\\section{Work Experience}\n"
        
        experiences = self.data['experience']
        
        # Sort by relevance if in tailored mode
        if self.is_tailored:
            scored_exp = self.sort_by_relevance(experiences, self.score_experience)
            experiences = [(exp, score) for exp, score in scored_exp]
        else:
            experiences = [(exp, 0) for exp in experiences]
        
        for exp, score in experiences:
            date_range = self.format_date_range(exp['start_date'], exp['end_date'])
            position = self.escape_latex(exp['position'])
            organization = self.escape_latex(exp['organization'])
            location = self.escape_latex(exp['location'])
            
            if self.is_tailored:
                section += f"% Relevance score: {score:.2f}\n"
            
            # Build responsibilities as line-separated text
            responsibilities_text = ""
            for i, responsibility in enumerate(exp['responsibilities']):
                if i > 0:
                    responsibilities_text += " \\newline "
                responsibilities_text += f"\\textbullet\\ {self.escape_latex(responsibility)}"
            
            section += f"\\cventry{{{date_range}}}{{{position}}}{{{organization}}}{{{location}}}{{}}{{{responsibilities_text}}}\n"
        
        return section
    
    def generate_education_section(self) -> str:
        """Generate Education section."""
        section = "\\section{Education}\n"
        
        for edu in self.data['education']:
            date_range = self.format_date_range(edu['start_date'], edu['end_date'])
            degree = self.escape_latex(edu['degree'])
            institution = self.escape_latex(edu['institution'])
            location = self.escape_latex(edu['location'])
            
            section += f"\\cventry{{{date_range}}}{{{degree}}}{{{institution}}}{{{location}}}{{}}{{"
            
            if 'thesis' in edu:
                thesis = self.escape_latex(edu['thesis'])
                section += f"\\textbf{{Thesis:}} ``{thesis}''\\\\ "
            
            if 'supervisors' in edu:
                supervisors = " \\& ".join([self.escape_latex(sup) for sup in edu['supervisors']])
                section += f"\\textbf{{Supervisors:}} {supervisors}\\\\ "
            
            if 'co_direction' in edu:
                co_direction = self.escape_latex(edu['co_direction'])
                section += f"\\textbf{{Co-direction:}} {co_direction}\\\\ "
            
            if 'mobility' in edu:
                section += "\\textbf{International Mobility:} \\begin{itemize} "
                for mobility in edu['mobility']:
                    section += f"\\item {self.escape_latex(mobility)} "
                section += "\\end{itemize} "
            
            section += "}\n"
        
        return section
    
    def generate_projects_section(self) -> str:
        """Generate Research Projects section."""
        section = "\\section{Research Projects}\n"
        
        projects = self.data['projects']
        
        # Sort by relevance if in tailored mode
        if self.is_tailored:
            scored_projects = self.sort_by_relevance(projects, self.score_project)
            projects = [(proj, score) for proj, score in scored_projects]
        else:
            projects = [(proj, 0) for proj in projects]
        
        for project, score in projects:
            date_range = self.format_date_range(project['start_date'], project['end_date'])
            title = self.escape_latex(project['title'])
            organization = self.escape_latex(project['organization'])
            description = self.escape_latex(project['description'])
            
            if self.is_tailored:
                section += f"% Relevance score: {score:.2f}\n"
            
            section += f"\\cventry{{{date_range}}}{{{title}}}{{{organization}}}{{}}{{}}{{{description}}}\n"
        
        return section
    
    def generate_skills_section(self) -> str:
        """Generate Technical Skills section."""
        section = "\\section{Technical Skills}\n"
        skills = self.data['skills']
        
        def format_skills(skill_list: List[str]) -> str:
            formatted = []
            for skill in skill_list:
                skill_lower = skill.lower()
                is_relevant = False
                
                if self.is_tailored:
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
            section += f"\\cvitem{{{category_title}: }}{{{self.escape_latex(items)}}}\n"
        
        return section
    
    def generate_footer(self) -> str:
        """Generate LaTeX document footer."""
        return "\\end{document}\n"
    
    def generate_latex(self, job_description: str = None) -> str:
        """Generate complete LaTeX CV."""
        
        # Set tailored mode if job description provided
        if job_description:
            self.is_tailored = True
            self.job_keywords = self.extract_keywords(job_description)
        
        latex_content = ""
        latex_content += self.generate_header()
        latex_content += self.generate_about_section()
        latex_content += self.generate_experience_section()
        latex_content += self.generate_education_section()
        latex_content += self.generate_projects_section()
        latex_content += self.generate_skills_section()
        latex_content += self.generate_hobbies_section()
        latex_content += self.generate_footer()
        
        return latex_content
    
    def generate_matching_report(self) -> str:
        """Generate a report of keyword matching statistics."""
        if not self.is_tailored:
            return ""
        
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
    
    def save_and_compile(self, output_file: str, job_description: str = None) -> bool:
        """Generate LaTeX, save to file, and compile to PDF."""
        
        latex_content = self.generate_latex(job_description)
        
        # Save .tex file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        mode_str = "Tailored" if self.is_tailored else "Basic"
        print(f"✅ {mode_str} CV.tex generated: {output_file}")
        
        if self.is_tailored:
            print(self.generate_matching_report())
        
        # Compile to PDF
        return self.compile_pdf(output_file)
    
    def compile_pdf(self, tex_file: str) -> bool:
        """Compile LaTeX to PDF using pdflatex."""
        try:
            tex_file = os.path.abspath(tex_file)
            tex_dir = os.path.dirname(tex_file)
            tex_basename = os.path.basename(tex_file)
            
            print(f"📄 Compiling {tex_basename} to PDF...")
            
            # Run pdflatex twice for proper cross-references
            for i in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_basename],
                    capture_output=True,
                    text=True,
                    cwd=tex_dir
                )
                
                if result.returncode != 0:
                    print(f"❌ LaTeX compilation failed (attempt {i+1})")
                    # Show last 500 chars of output for debugging
                    print(result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
                    return False
            
            # Clean up auxiliary files
            base_name = os.path.splitext(tex_basename)[0]
            aux_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls']
            
            for ext in aux_extensions:
                aux_file = os.path.join(tex_dir, base_name + ext)
                if os.path.exists(aux_file):
                    os.remove(aux_file)
            
            pdf_path = os.path.join(tex_dir, base_name + ".pdf")
            print(f"✅ PDF compiled successfully: {pdf_path}")
            return True
            
        except FileNotFoundError:
            print("⚠️  pdflatex not found. Please install LaTeX to compile PDF.")
            return False
        except Exception as e:
            print(f"❌ Error compiling PDF: {e}")
            return False


def interactive_menu():
    """Display interactive menu and return user choice."""
    print("\n" + "="*60)
    print("           CV GENERATOR")
    print("="*60)
    print("\nChoose CV generation mode:\n")
    print("  [1] Basic CV       - Generate from cv_data.json")
    print("  [2] Tailored CV    - Generate from job_description.txt")
    print("  [3] Exit")
    print()
    
    while True:
        choice = input("Enter your choice (1/2/3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        print("Invalid choice. Please enter 1, 2, or 3.")


def main():
    """Main function to generate CV."""
    parser = argparse.ArgumentParser(
        description='Generate CV from JSON data with optional job description tailoring.'
    )
    parser.add_argument(
        '--basic', '-b',
        action='store_true',
        help='Generate basic CV directly (no menu)'
    )
    parser.add_argument(
        '--tailored', '-t',
        action='store_true',
        help='Generate tailored CV directly (no menu)'
    )
    parser.add_argument(
        '--job', '-j',
        type=str,
        help='Path to job description file (implies --tailored)'
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        default=None,
        help='Output file name (default: CV.tex)'
    )
    parser.add_argument(
        '--data', '-d',
        type=str,
        default=None,
        help='Path to CV data JSON file'
    )
    
    args = parser.parse_args()
    
    # Resolve paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    cv_dir = os.path.join(script_dir, "..", "cv")
    
    # Determine mode
    if args.basic:
        mode = '1'
    elif args.tailored or args.job:
        mode = '2'
    else:
        mode = interactive_menu()
    
    if mode == '3':
        print("Goodbye!")
        return
    
    try:
        # Initialize generator
        generator = CVGenerator(data_file=args.data)
        
        if mode == '1':
            # Basic CV mode
            output_file = args.output or os.path.join(cv_dir, "CV.tex")
            generator.save_and_compile(output_file)
            
        elif mode == '2':
            # Tailored CV mode
            job_file = args.job
            if not job_file:
                # Look for default job_description.txt
                job_file = os.path.join(script_dir, "..", "job_description.txt")
            
            if not os.path.exists(job_file):
                print(f"❌ Job description file not found: {job_file}")
                print("Please create job_description.txt in the project root or specify with --job")
                return
            
            with open(job_file, 'r', encoding='utf-8') as f:
                job_description = f.read()
            
            print(f"📄 Using job description: {job_file}")
            
            output_file = args.output or os.path.join(cv_dir, "CV.tex")
            generator.save_and_compile(output_file, job_description)
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
