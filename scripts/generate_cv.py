#!/usr/bin/env python3
"""
CV LaTeX Generator
Generates CV.tex from cv_data.json
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class CVLatexGenerator:
    def __init__(self, data_file: str = None):
        """Initialize the generator with data file."""
        if data_file is None:
            # Default to data folder relative to script location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            data_file = os.path.join(script_dir, "..", "data", "cv_data.json")
        self.data_file = data_file
        self.data = self.load_data()
    
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
    
    def generate_about_section(self) -> str:
        """Generate About Me section."""
        about = self.escape_latex(self.data['personal']['about'])
        
        section = "\\section{About Me}\n"
        section += f"\\cvitem{{}}{{\\textit{{{about}}}}}\n\n"
        
        return section
    
    def generate_experience_section(self) -> str:
        """Generate Work Experience section."""
        section = "\\section{Work Experience}\n"
        
        for exp in self.data['experience']:
            date_range = self.format_date_range(exp['start_date'], exp['end_date'])
            position = self.escape_latex(exp['position'])
            organization = self.escape_latex(exp['organization'])
            location = self.escape_latex(exp['location'])
            
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
            
            section += f"\\cventry{{{date_range}}}{{{degree}}}{{{institution}}}{{{location}}}{{}}{{\\n"
            
            if 'thesis' in edu:
                thesis = self.escape_latex(edu['thesis'])
                section += f"\\textbf{{Thesis:}} ``{thesis}''\\\\\\n"
            
            if 'supervisors' in edu:
                supervisors = " \\& ".join([self.escape_latex(sup) for sup in edu['supervisors']])
                section += f"\\textbf{{Supervisors:}} {supervisors}\\\\\\n"
            
            if 'co_direction' in edu:
                co_direction = self.escape_latex(edu['co_direction'])
                section += f"\\textbf{{Co-direction:}} {co_direction}\\\\\\n"
            
            if 'mobility' in edu:
                section += "\\textbf{International Mobility:}\\n\\begin{itemize}\\n"
                for mobility in edu['mobility']:
                    section += f"\\item {self.escape_latex(mobility)}\\n"
                section += "\\end{itemize}\\n"
            
            section += "}\n"
        
        return section
    
    def generate_projects_section(self) -> str:
        """Generate Research Projects section."""
        section = "\\section{Research Projects}\n"
        
        for project in self.data['projects']:
            date_range = self.format_date_range(project['start_date'], project['end_date'])
            title = self.escape_latex(project['title'])
            organization = self.escape_latex(project['organization'])
            description = self.escape_latex(project['description'])
            
            section += f"\\cventry{{{date_range}}}{{{title}}}{{{organization}}}{{}}{{}}{{\\n{description}\\n}}\\n"
        
        return section
    
    def generate_skills_section(self) -> str:
        """Generate Technical Skills section."""
        section = "\\section{Technical Skills}\n"
        skills = self.data['skills']
        
        section += "\\cvitem{Process Engineering}{" + ", ".join([self.escape_latex(skill) for skill in skills['process_engineering']]) + "}\n"
        section += "\\cvitem{Data Science}{" + ", ".join([self.escape_latex(skill) for skill in skills['data_science']]) + "}\n"
        section += "\\cvitem{Programming}{" + ", ".join([self.escape_latex(skill) for skill in skills['programming']]) + "}\n"
        section += "\\cvitem{Languages}{" + ", ".join([self.escape_latex(skill) for skill in skills['languages']]) + "}\n\n"
        
        return section
    
    def generate_hobbies_section(self) -> str:
        """Generate Hobbies & Interests section."""
        section = "\\section{Hobbies \\& Interests}\n"
        hobbies = self.data['hobbies']
        
        for category, items in hobbies.items():
            category_title = category.replace('_', ' ').title()
            section += f"\\cvitem{{{category_title}: }}{{{self.escape_latex(items)}}}\\n"
        
        return section
    
    def generate_footer(self) -> str:
        """Generate LaTeX document footer."""
        return "\\end{document}\n"
    
    def generate_latex(self) -> str:
        """Generate complete LaTeX CV."""
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
    
    def save_latex(self, output_file: str = None) -> None:
        """Save generated LaTeX to file."""
        if output_file is None:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(script_dir, "..", "cv", "CV.tex")
        
        latex_content = self.generate_latex()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        print(f"CV.tex generated successfully: {output_file}")
    
    def compile_pdf(self, tex_file: str = None) -> bool:
        """Compile LaTeX to PDF using pdflatex."""
        try:
            import subprocess
            
            # Default to CV.tex in the cv folder
            if tex_file is None:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                tex_file = os.path.join(script_dir, "..", "cv", "CV.tex")
            
            # Get absolute path and directory
            tex_file = os.path.abspath(tex_file)
            tex_dir = os.path.dirname(tex_file)
            tex_basename = os.path.basename(tex_file)
            
            # Run pdflatex twice for proper cross-references
            for i in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_basename],
                    capture_output=True,
                    text=True,
                    cwd=tex_dir  # Change to the directory containing the .tex file
                )
                
                if result.returncode != 0:
                    print(f"LaTeX compilation failed (attempt {i+1}):")
                    print(result.stdout)
                    print(result.stderr)
                    return False
            
            # Clean up auxiliary files
            base_name = os.path.splitext(tex_basename)[0]
            aux_extensions = ['.aux', '.log', '.out', '.fdb_latexmk', '.fls']
            
            for ext in aux_extensions:
                aux_file = os.path.join(tex_dir, base_name + ext)
                if os.path.exists(aux_file):
                    os.remove(aux_file)
            
            pdf_path = os.path.join(tex_dir, base_name + ".pdf")
            print(f"PDF compiled successfully: {pdf_path}")
            return True
            
        except FileNotFoundError:
            print("pdflatex not found. Please install LaTeX to compile PDF.")
            return False
        except Exception as e:
            print(f"Error compiling PDF: {e}")
            return False

def main():
    """Main function to generate CV."""
    try:
        generator = CVLatexGenerator()
        generator.save_latex()
        
        # Optionally compile to PDF
        compile_pdf = input("Compile to PDF? (y/n): ").lower().strip() == 'y'
        if compile_pdf:
            generator.compile_pdf()
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
