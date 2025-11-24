#!/usr/bin/env python3
"""
HTML Pages Generator
Generates all HTML pages from cv-data.json
"""

import json
import os
from typing import Dict, List, Any
from jinja2 import Template, Environment, FileSystemLoader

class HTMLGenerator:
    def __init__(self, data_file: str = "cv-data.json"):
        """Initialize the generator with data file."""
        self.data_file = data_file
        self.data = self.load_data()
        self.env = Environment(loader=FileSystemLoader('.'))
    
    def load_data(self) -> Dict[str, Any]:
        """Load CV data from JSON file."""
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Data file {self.data_file} not found")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.data_file}: {e}")
    
    def get_base_template(self) -> str:
        """Return the base HTML template."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ personal.name.first }} {{ personal.name.last }}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/academicons@1.9.1/css/academicons.min.css">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link href="assets/styles.css" rel="stylesheet">
</head>
<body>
    <div class="sidebar text-center">
        <div class="avatar">
            <img src="MyPhoto.png" alt="{{ personal.name.first }} {{ personal.name.last }}">
        </div>
        <h3>{{ personal.name.first }} {{ personal.name.last }}</h3>
        <p class="text-muted">{{ personal.title }}</p>
        <div class="social-icons mb-3">
            <a href="{{ personal.social.github }}" target="_blank"><i class="fab fa-github"></i></a>
            <a href="{{ personal.social.linkedin }}" target="_blank"><i class="fab fa-linkedin"></i></a>
            <a href="{{ personal.social.twitter }}" target="_blank"><i class="fab fa-twitter"></i></a>
            <a href="{{ personal.social.researchgate }}" target="_blank"><i class="ai ai-researchgate"></i></a>
            <a href="{{ personal.social.google_scholar }}" target="_blank"><i class="ai ai-google-scholar"></i></a>
            <a href="{{ personal.social.orcid }}" target="_blank"><i class="ai ai-orcid"></i></a>
        </div>
        <div class="nav flex-column mb-3">
            <a class="nav-link {% if page == 'home' %}active{% endif %}" href="home.html"><i class="fas fa-home"></i> Home</a>
            <a class="nav-link {% if page == 'publications' %}active{% endif %}" href="publications.html"><i class="fas fa-book"></i> Publications</a>
            <a class="nav-link {% if page == 'education' %}active{% endif %}" href="education.html"><i class="fas fa-graduation-cap"></i> Education</a>
            <a class="nav-link {% if page == 'experience' %}active{% endif %}" href="experience.html"><i class="fas fa-briefcase"></i> Experience</a>
            <a class="nav-link {% if page == 'projects' %}active{% endif %}" href="projects.html"><i class="fas fa-project-diagram"></i> Projects</a>
            <a class="nav-link {% if page == 'skills' %}active{% endif %}" href="skills.html"><i class="fas fa-tools"></i> Skills & Hobbies</a>
        </div>
        <div class="mt-3">
            <a href="mailto:{{ personal.contact.email_surrey }}" class="text-muted d-block mb-2"><i class="fas fa-envelope"></i> Surrey Email</a>
            <a href="mailto:{{ personal.contact.email_tlemcen }}" class="text-muted d-block"><i class="fas fa-envelope"></i> UTL Email</a>
            <a href="CV.pdf" class="btn-download"><i class="fas fa-file-download"></i> Download CV</a>
        </div>
    </div>
    
    <div class="main-content">
        {% block content %}{% endblock %}
    </div>
    
    <script src="index.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""
    
    def generate_home_page(self) -> str:
        """Generate home page content."""
        template_str = self.get_base_template().replace(
            '{% block content %}{% endblock %}',
            """<h1 class="section-header">Welcome!</h1>
        
        <li class="list-group-item card mb-3 card-hover-effect">
            <div class="card-body">
                <h2 class="section-title">About Me</h2>
                <p>{{ personal.about }}</p>
            </div>
        </li>
        
        <div class="row">
            <div class="col-md-6">
                <li class="list-group-item card mb-3 card-hover-effect">
                    <div class="card-body">
                        <h3 class="section-title">Research Interests</h3>
                        <ul>
                            {% for skill in skills.data_science %}
                            <li>{{ skill }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </li>
            </div>
            <div class="col-md-6">
                <li class="list-group-item card mb-3 card-hover-effect">
                    <div class="card-body">
                        <h3 class="section-title">Keywords</h3>
                        <ul class="list-unstyled mt-3 mb-0">
                            {% for skill in skills.process_engineering %}
                            <li>🌿 {{ skill }}</li>
                            {% endfor %}
                            {% for skill in skills.programming %}
                            <li>🖥️ {{ skill }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </li>
            </div>
        </div>"""
        )
        
        template = Template(template_str)
        return template.render(page='home', **self.data)
    
    def generate_education_page(self) -> str:
        """Generate education page content."""
        template_str = self.get_base_template().replace(
            '{% block content %}{% endblock %}',
            """<div class="container mt-5">
        <h1 class="section-header">Education</h1>
        <ul class="timeline list-group list-group-flush">
            {% for edu in education %}
            <li class="list-group-item card mb-3 card-hover-effect">
                <div class="card-body">
                    <h2 class="section-title">{{ edu.degree }}</h2>
                    <h6 class="card-subtitle mb-2 text-muted">{{ edu.institution }}, {{ edu.location }} ({{ edu.start_date }} – {{ edu.end_date }})
                    {% if edu.co_direction %}<br>In co-direction with {{ edu.co_direction }}{% endif %}</h6>
                    <ul>
                        {% if edu.thesis %}
                        <li><strong>Thesis:</strong> "{{ edu.thesis }}"</li>
                        {% endif %}
                        {% if edu.supervisors %}
                        <li><strong>Supervisors:</strong> {{ edu.supervisors | join(' & ') }}</li>
                        {% endif %}
                        {% if edu.mobility %}
                        {% for mobility in edu.mobility %}
                        <li><strong>International Mobility:</strong> {{ mobility }}</li>
                        {% endfor %}
                        {% endif %}
                    </ul>
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>"""
        )
        
        template = Template(template_str)
        return template.render(page='education', **self.data)
    
    def generate_experience_page(self) -> str:
        """Generate experience page content."""
        template_str = self.get_base_template().replace(
            '{% block content %}{% endblock %}',
            """<div class="container mt-5">
        <h1 class="section-header">Experience</h1>
        <ul class="timeline list-group list-group-flush">
            {% for exp in experience %}
            <li class="list-group-item card mb-3 card-hover-effect">
                <div class="card-body">
                    <h2 class="section-title">{{ exp.position }}</h2>
                    <h6 class="card-subtitle mb-2 text-muted">{{ exp.organization }}, {{ exp.location }} · {{ exp.start_date }} – {{ exp.end_date }}</h6>
                    <p class="card-text">
                        <strong>Job description:</strong> {{ exp.description }}
                    </p>
                    {% if exp.responsibilities %}
                    <ul>
                        {% for responsibility in exp.responsibilities %}
                        <li>{{ responsibility }}</li>
                        {% endfor %}
                    </ul>
                    {% endif %}
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>"""
        )
        
        template = Template(template_str)
        return template.render(page='experience', **self.data)
    
    def generate_projects_page(self) -> str:
        """Generate projects page content."""
        template_str = self.get_base_template().replace(
            '{% block content %}{% endblock %}',
            """<div class="container mt-5">
        <h1 class="section-header">Projects</h1>
        <h2 class="section-title mt-5">Research Projects</h2>
        
        {% for project in projects %}
        <div class="card mb-3 card-hover-effect">
            <div class="card-body position-relative">
                <span class="project-status status-{{ project.status }}">{{ project.status.title() }}</span>
                <h4 class="card-title">{{ project.title }}</h4>
                <h6 class="card-subtitle mb-2 text-muted">{{ project.organization }} | {{ project.start_date }} - {{ project.end_date }}</h6>
                <p class="card-text">{{ project.description }}</p>
            </div>
        </div>
        {% endfor %}
    </div>"""
        )
        
        template = Template(template_str)
        return template.render(page='projects', **self.data)
    
    def generate_publications_page(self) -> str:
        """Generate publications page content."""
        template_str = self.get_base_template().replace(
            '{% block content %}{% endblock %}',
            """<div class="container mt-5">
        <h1 class="section-header">Publications</h1>
        <ul class="timeline list-group list-group-flush">
            {% for pub in publications %}
            <li class="list-group-item card mb-3 card-hover-effect">
                <div class="card-body">
                    <h5 class="card-title">
                        {% if pub.doi %}
                        <a href="{{ pub.doi }}" target="_blank">{{ pub.title }}</a>
                        {% else %}
                        {{ pub.title }}
                        {% endif %}
                    </h5>
                    <h6 class="card-subtitle mb-2 text-muted">Published in: {{ pub.venue }}, {{ pub.year }}</h6>
                    {% if pub.abstract %}
                    <p class="card-text"><strong>Abstract:</strong> {{ pub.abstract }}</p>
                    {% endif %}
                </div>
            </li>
            {% endfor %}
        </ul>
    </div>"""
        )
        
        template = Template(template_str)
        return template.render(page='publications', **self.data)
    
    def generate_skills_page(self) -> str:
        """Generate skills page content."""
        template_str = self.get_base_template().replace(
            '{% block content %}{% endblock %}',
            """<div class="container mt-5">
        <h1 class="section-header">Skills, Activities & Hobbies</h1>
        
        <div class="card mb-3 card-hover-effect">
            <div class="card-body">
                <h2 class="section-title">Technical Skills</h2>
                <div class="row">
                    <div class="col-md-3">
                        <h4>Process Engineering</h4>
                        <ul class="list-group list-group-flush">
                            {% for skill in skills.process_engineering %}
                            <li class="list-group-item">{{ skill }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    <div class="col-md-3">
                        <h4>Data Science</h4>
                        <ul class="list-group list-group-flush">
                            {% for skill in skills.data_science %}
                            <li class="list-group-item">{{ skill }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    <div class="col-md-3">
                        <h4>Programming</h4>
                        <ul class="list-group list-group-flush">
                            {% for skill in skills.programming %}
                            <li class="list-group-item">{{ skill }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                    <div class="col-md-3">
                        <h4>Languages</h4>
                        <ul class="list-group list-group-flush">
                            {% for lang in skills.languages %}
                            <li class="list-group-item">{{ lang }}</li>
                            {% endfor %}
                        </ul>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-3 card-hover-effect">
            <div class="card-body">
                <h2 class="section-title">Activities</h2>
                <ul class="timeline list-group list-group-flush">
                    {% for activity in activities %}
                    <li class="list-group-item">
                        <strong>{{ activity.date }}:</strong> 
                        {% if activity.type == 'conference' %}📊{% elif activity.type == 'workshop' %}🛠️{% elif activity.type == 'training' %}📚{% elif activity.type == 'presentation' %}🎤{% elif activity.type == 'summer_school' %}🏫{% elif activity.type == 'spring_school' %}🌱{% elif activity.type == 'webinar' %}💻{% elif activity.type == 'symposium' %}🎯{% elif activity.type == 'seminar' %}📋{% else %}📅{% endif %} 
                        {{ activity.description }}
                        {% if activity.location %} <em>({{ activity.location }})</em>{% endif %}
                    </li>
                    {% endfor %}
                </ul>
            </div>
        </div>
        
        <div class="card mb-3 card-hover-effect">
            <div class="card-body">
                <h2 class="section-title">Hobbies & Interests</h2>
                {% for category, items in hobbies.items() %}
                <div class="mb-3">
                    <h4>{{ category.replace('_', ' ').title() }}</h4>
                    <p>{{ items }}</p>
                </div>
                {% endfor %}
            </div>
        </div>
    </div>"""
        )
        
        template = Template(template_str)
        return template.render(page='skills', **self.data)
    
    def generate_all_pages(self) -> None:
        """Generate all HTML pages."""
        pages = {
            'home.html': self.generate_home_page(),
            'education.html': self.generate_education_page(),
            'experience.html': self.generate_experience_page(),
            'projects.html': self.generate_projects_page(),
            'publications.html': self.generate_publications_page(),
            'skills.html': self.generate_skills_page()
        }
        
        for filename, content in pages.items():
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Generated: {filename}")
        
        # Also update index.html to redirect to home.html
        index_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url=home.html">
    <title>Redirecting...</title>
</head>
<body>
    <p>Redirecting to <a href="home.html">home page</a>...</p>
</body>
</html>"""
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_content)
        print("Generated: index.html (redirect)")

def main():
    """Main function to generate HTML pages."""
    try:
        generator = HTMLGenerator()
        generator.generate_all_pages()
        print("All HTML pages generated successfully!")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
