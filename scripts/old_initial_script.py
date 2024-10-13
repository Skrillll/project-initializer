import os
import yaml
from datetime import datetime

def create_directory(path):
    """Create a directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)

def create_file(path, content=''):
    """Create a file with the given content."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def create_markdown_file(path, title, tags):
    """Create a Markdown file with metadata."""
    metadata = {
        'title': title,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'last_updated': datetime.now().strftime('%Y-%m-%d'),
        'tags': tags
    }
    content = '---\n' + yaml.dump(metadata) + '---\n\n# ' + title + '\n\nContenu à remplir.'
    create_file(path, content)

def init_project_structure():
    """Initialize the project structure."""
    root = 'OmniIntelligence'
    create_directory(root)

    # Define main directories
    dirs = [
        'docs', 'docs/ai_organization', 'ai_agents', 'ai_agents/agent_nexus',
        'ai_agents/future_agents', 'knowledge_base', 'knowledge_base/personal',
        'knowledge_base/professional', 'knowledge_base/ai_research', 'projects',
        'projects/omni_intelligence', 'projects/omni_intelligence/src',
        'projects/omni_intelligence/tests', 'projects/omni_intelligence/docs',
        'tools', 'tools/content_management', 'tools/knowledge_management',
        'tools/documentation_generator'
    ]
    
    for dir in dirs:
        create_directory(os.path.join(root, dir))

    # Create Markdown files in docs/
    markdown_files = [
        ('profile.md', 'Profil d\'Omar El Mountassir', ['personnel', 'professionnel', 'auto-entrepreneur']),
        ('technical_environment.md', 'Environnement Technique', ['développement', 'outils']),
        ('skills_and_experience.md', 'Compétences et Expérience', ['compétences', 'expérience']),
        ('learning_resources.md', 'Ressources d\'Apprentissage', ['apprentissage', 'ressources']),
        ('project_objectives.md', 'Objectifs du Projet OmniIntelligence', ['objectifs', 'projet']),
    ]

    for filename, title, tags in markdown_files:
        create_markdown_file(os.path.join(root, 'docs', filename), title, tags)

    # Create files in docs/ai_organization/
    ai_org_files = [
        ('overview.md', 'Aperçu de l\'Organisation IA', ['IA', 'organisation']),
        ('roles_and_responsibilities.md', 'Rôles et Responsabilités', ['IA', 'rôles']),
        ('ai_integration_strategy.md', 'Stratégie d\'Intégration IA', ['IA', 'stratégie']),
    ]

    for filename, title, tags in ai_org_files:
        create_markdown_file(os.path.join(root, 'docs', 'ai_organization', filename), title, tags)

    # Create instructions for Agent Nexus
    create_markdown_file(os.path.join(root, 'ai_agents', 'agent_nexus', 'instructions.md'), 
                         'Instructions pour Agent Nexus', ['IA', 'agent', 'instructions'])

    # Create roadmap.md at the root
    roadmap_content = """# Feuille de Route du Projet OmniIntelligence

1. Initialiser la structure du projet
2. Remplir les documents de base dans `docs/`
3. Définir la stratégie d'intégration IA dans `docs/ai_organization/`
4. Développer les premiers outils de gestion de contenu et de connaissances
5. Commencer le développement du projet OmniIntelligence
6. Itérer et améliorer continuellement la structure et les processus
"""
    create_file(os.path.join(root, 'roadmap.md'), roadmap_content)

    print("Structure du projet initialisée avec succès.")

if __name__ == "__main__":
    init_project_structure()