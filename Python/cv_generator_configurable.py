#!/usr/bin/env python3
"""
Configurable CV LaTeX Generator
Generates CV.tex from cv-data.json with configurable sections
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

class ConfigurableCVGenerator:
    def __init__(self, data_file: str = "cv-data.json", config_file: str = "cv-config.json"):
        """Initialize the generator with data and config files."""
        self.data_file = data_file
        self.config_file = config_file
        self.data = self.load_data()
        self.config = self.load_config()
    
    def load_data(self) -> Dict[str, Any]:
        """Load CV data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file {self.data_file} not found")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.data_file}: {e}")
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration settings."""
        default_config = {
            "cv_sections": {
                "about": True,
                "experience": True,
                "education": True,
                "projects": True,
                "publications": False,  # NOT included by default
                "activities": False,  # NOT included by default
                "skills": True,
                "hobbies": True
            },
            "cv_settings": {
                "max_projects": None,  # None = all projects, or set number like 3
                "max_experience": None,  # None = all experience
                "max_publications": 5,  # If publications enabled
                "max_activities": None,  # None = all activities, or set number like 10
                "include_abstracts": False,  # For publications
                "projects_status_filter": None,  # None = all, "ongoing", "completed"
                "activities_type_filter": None  # None = all, "conference", "workshop", etc.
            },
            "latex_settings": {
                "document_class": "moderncv",
                "style": "classic",
                "color": "blue",
                "geometry": "scale=0.8"
            }
        }
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # Merge with defaults
                config = default_config.copy()
                config.update(user_config)
                return config
        except FileNotFoundError:
            # Create default config file
            self.save_config(default_config)
            print(f"✨ Created default config file: {self.config_file}")
            return default_config
    
    def save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
    
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
        latex_settings = self.config['latex_settings']
        
        header = f"""\\documentclass[11pt,a4paper]{{{latex_settings['document_class']}}}
\\moderncvstyle{{{latex_settings['style']}}}
\\moderncvcolor{{{latex_settings['color']}}}
\\usepackage[{latex_settings['geometry']}]{{geometry}}
\\usepackage{{multicol}}
\\usepackage{{academicons}}
\\usepackage{{lmodern}}

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
        if not self.config['cv_sections']['about']:
            return ""
        
        about = self.escape_latex(self.data['personal']['about'])
        
        section = "\\section{About Me}\n"
        section += f"\\cvitem{{}}{{\\textit{{{about}}}}}\n\n"
        
        return section
    
    def generate_experience_section(self) -> str:
        """Generate Work Experience section."""
        if not self.config['cv_sections']['experience']:
            return ""
        
        section = "\\section{Work Experience}\n"
        
        experience_list = self.data['experience']
        max_exp = self.config['cv_settings']['max_experience']
        
        if max_exp:
            experience_list = experience_list[:max_exp]
        
        for exp in experience_list:
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
        if not self.config['cv_sections']['education']:
            return ""
        
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
        if not self.config['cv_sections']['projects']:
            return ""
        
        section = "\\section{Research Projects}\n"
        
        projects_list = self.data['projects']
        
        # Filter by status if specified
        status_filter = self.config['cv_settings']['projects_status_filter']
        if status_filter:
            projects_list = [p for p in projects_list if p.get('status') == status_filter]
        
        # Limit number if specified
        max_projects = self.config['cv_settings']['max_projects']
        if max_projects:
            projects_list = projects_list[:max_projects]
        
        for project in projects_list:
            date_range = self.format_date_range(project['start_date'], project['end_date'])
            title = self.escape_latex(project['title'])
            organization = self.escape_latex(project['organization'])
            description = self.escape_latex(project['description'])
            
            section += f"\\cventry{{{date_range}}}{{{title}}}{{{organization}}}{{}}{{}}{{\\n{description}\\n}}\\n"
        
        return section
    
    def generate_publications_section(self) -> str:
        """Generate Publications section (only if enabled)."""
        if not self.config['cv_sections']['publications']:
            return ""
        
        section = "\\section{Publications}\n"
        
        publications_list = self.data.get('publications', [])
        
        # Limit number if specified
        max_pubs = self.config['cv_settings']['max_publications']
        if max_pubs:
            publications_list = publications_list[:max_pubs]
        
        include_abstracts = self.config['cv_settings']['include_abstracts']
        
        for pub in publications_list:
            year = pub['year']
            title = self.escape_latex(pub['title'])
            venue = self.escape_latex(pub['venue'])
            
            if include_abstracts and 'abstract' in pub:
                abstract = self.escape_latex(pub['abstract'][:200] + "..." if len(pub['abstract']) > 200 else pub['abstract'])
                section += f"\\cvitem{{{year}}}{{\\textit{{{title}}}. {venue}. \\\\\\textbf{{Abstract:}} {abstract}}}\\n"
            else:
                section += f"\\cvitem{{{year}}}{{\\textit{{{title}}}. {venue}.}}\\n"
        
        return section
    
    def generate_activities_section(self) -> str:
        """Generate Activities section (only if enabled)."""
        if not self.config['cv_sections']['activities']:
            return ""
        
        section = "\\section{Activities}\n"
        
        activities_list = self.data.get('activities', [])
        
        # Filter by type if specified
        type_filter = self.config['cv_settings']['activities_type_filter']
        if type_filter:
            activities_list = [a for a in activities_list if a.get('type') == type_filter]
        
        # Limit number if specified
        max_activities = self.config['cv_settings']['max_activities']
        if max_activities:
            activities_list = activities_list[:max_activities]
        
        for activity in activities_list:
            date = self.escape_latex(activity['date'])
            event = self.escape_latex(activity['event'])
            location = self.escape_latex(activity.get('location', ''))
            description = self.escape_latex(activity.get('description', ''))
            
            if location:
                section += f"\\cvitem{{{date}}}{{\\textbf{{{event}}}, {location}. {description}}}\\n"
            else:
                section += f"\\cvitem{{{date}}}{{\\textbf{{{event}}}. {description}}}\\n"
        
        return section
    
    def generate_skills_section(self) -> str:
        """Generate Technical Skills section."""
        if not self.config['cv_sections']['skills']:
            return ""
        
        section = "\\section{Technical Skills}\n"
        skills = self.data['skills']
        
        section += "\\cvitem{Process Engineering}{" + ", ".join([self.escape_latex(skill) for skill in skills['process_engineering']]) + "}\n"
        section += "\\cvitem{Data Science}{" + ", ".join([self.escape_latex(skill) for skill in skills['data_science']]) + "}\n"
        section += "\\cvitem{Programming}{" + ", ".join([self.escape_latex(skill) for skill in skills['programming']]) + "}\n"
        section += "\\cvitem{Languages}{" + ", ".join([self.escape_latex(skill) for skill in skills['languages']]) + "}\n\n"
        
        return section
    
    def generate_hobbies_section(self) -> str:
        """Generate Hobbies & Interests section."""
        if not self.config['cv_sections']['hobbies']:
            return ""
        
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
        """Generate complete LaTeX CV based on configuration."""
        latex_content = ""
        latex_content += self.generate_header()
        
        # Generate sections based on configuration
        if self.config['cv_sections']['about']:
            latex_content += self.generate_about_section()
        
        if self.config['cv_sections']['experience']:
            latex_content += self.generate_experience_section()
        
        if self.config['cv_sections']['education']:
            latex_content += self.generate_education_section()
        
        if self.config['cv_sections']['projects']:
            latex_content += self.generate_projects_section()
        
        if self.config['cv_sections']['publications']:
            latex_content += self.generate_publications_section()
        
        if self.config['cv_sections']['activities']:
            latex_content += self.generate_activities_section()
        
        if self.config['cv_sections']['skills']:
            latex_content += self.generate_skills_section()
        
        if self.config['cv_sections']['hobbies']:
            latex_content += self.generate_hobbies_section()
        
        latex_content += self.generate_footer()
        
        return latex_content
    
    def save_latex(self, output_file: str = "CV.tex") -> None:
        """Save generated LaTeX to file."""
        latex_content = self.generate_latex()
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        enabled_sections = [k for k, v in self.config['cv_sections'].items() if v]
        print(f"✅ CV.tex generated with sections: {', '.join(enabled_sections)}")
    
    def compile_pdf(self, tex_file: str = "CV.tex") -> bool:
        """Compile LaTeX to PDF using pdflatex."""
        try:
            import subprocess
            
            # Run pdflatex twice for proper cross-references
            for i in range(2):
                result = subprocess.run(
                    ['pdflatex', '-interaction=nonstopmode', tex_file],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode != 0:
                    print(f"LaTeX compilation failed (attempt {i+1}):")
                    print(result.stdout)
                    print(result.stderr)
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

def main():
    """Main function to generate CV."""
    try:
        generator = ConfigurableCVGenerator()
        generator.save_latex()
        
        # Show current configuration
        print(f"\n📋 Current CV Configuration:")
        for section, enabled in generator.config['cv_sections'].items():
            status = "✅ Enabled" if enabled else "❌ Disabled"
            print(f"   {section.title()}: {status}")
        
        print(f"\n💡 Edit {generator.config_file} to customize which sections appear in your CV")
        
        # Optionally compile to PDF
        compile_pdf = input("\nCompile to PDF? (y/n): ").lower().strip() == 'y'
        if compile_pdf:
            generator.compile_pdf()
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
