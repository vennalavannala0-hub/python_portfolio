"""Placeholder portfolio content. Replace everything via Django Admin."""

from datetime import date

from .models import (
    Certification,
    Education,
    Experience,
    Project,
    SiteProfile,
    Skill,
)

ABOUT_TEXT = """I am a Python developer focused on Django: well-structured models, careful request/response flows, and APIs that other teams can trust.

Most of my work lives at the intersection of product and infrastructure — translating product requirements into maintainable backends, then shipping them with tests, migrations, and clear documentation.

I care about readable code, thoughtful data models, and deployments that do not become a second job."""

CAREER_SUMMARY = """I started with Python scripts and data work, then moved into full Django applications: authentication, REST APIs, background jobs, and production configuration.

These days I look for backend-heavy roles where I can own a service end to end — from schema design through Render or similar PaaS deploys."""


def seed_portfolio(replace_existing=False):
    if replace_existing:
        SiteProfile.objects.all().delete()
        Skill.objects.all().delete()
        Project.objects.all().delete()
        Experience.objects.all().delete()
        Education.objects.all().delete()
        Certification.objects.all().delete()

    profile, created = SiteProfile.objects.get_or_create(
        pk=1,
        defaults={
            "full_name": "Jordan Hale",
            "headline": "Python Developer",
            "short_intro": (
                "I design and ship Django applications, REST APIs, and PostgreSQL-backed "
                "services that stay understandable after they leave my laptop."
            ),
            "about_text": ABOUT_TEXT,
            "career_summary": CAREER_SUMMARY,
            "location": "Remote · Open to hybrid",
            "availability": "Open to backend roles and selected freelance Django work",
            "email": "hello@jordanhale.dev",
            "github_url": "https://github.com/your-username",
            "linkedin_url": "https://www.linkedin.com/in/your-username/",
            "meta_title": "Jordan Hale — Python Developer",
            "meta_description": (
                "Portfolio of Jordan Hale, a Python/Django developer building "
                "reliable web applications, REST APIs, and production backends."
            ),
        },
    )

    skills = [
        ("Python", "language", "Core language for services, scripts, and data work.", "python", 10),
        ("Django", "framework", "Full-stack web apps, admin, auth, and ORM-first design.", "django", 20),
        ("Django REST Framework", "framework", "Versioned APIs with serializers, viewsets, and auth.", "drf", 30),
        ("HTML", "frontend", "Semantic markup that stays accessible and crawlable.", "html", 40),
        ("CSS", "frontend", "Responsive layouts, design systems, and modern CSS.", "css", 50),
        ("JavaScript", "frontend", "Progressive enhancement without a heavy SPA.", "javascript", 60),
        ("SQL", "data", "Query design, indexing awareness, and data integrity.", "sql", 70),
        ("PostgreSQL", "data", "Production database of choice for Django apps.", "postgres", 80),
        ("Git/GitHub", "tooling", "Branching, reviews, and a clean commit history.", "git", 90),
        ("REST APIs", "tooling", "Resource modeling, status codes, and client-friendly errors.", "api", 100),
        ("Docker", "tooling", "Reproducible local environments and deployable images.", "docker", 110),
    ]
    for name, category, summary, icon_key, order in skills:
        Skill.objects.get_or_create(
            name=name,
            defaults={
                "category": category,
                "summary": summary,
                "icon_key": icon_key,
                "display_order": order,
                "is_active": True,
            },
        )

    projects = [
        {
            "title": "Atlas Inventory API",
            "slug": "atlas-inventory-api",
            "description": (
                "A Django REST Framework service for warehouse stock, purchase orders, "
                "and low-inventory alerts. Includes token auth, filtered list endpoints, "
                "and an admin workflow for receiving shipments."
            ),
            "technologies": "Python, Django, DRF, PostgreSQL, Docker",
            "github_url": "https://github.com/your-username/atlas-inventory-api",
            "live_url": "",
            "is_featured": True,
            "display_order": 10,
        },
        {
            "title": "Harbor Notes",
            "slug": "harbor-notes",
            "description": (
                "A private notes app with Django auth, tagged search, and Markdown "
                "rendering. Built as a study in clean models, form validation, and "
                "a calm, accessible interface."
            ),
            "technologies": "Python, Django, HTML, CSS, JavaScript, SQLite",
            "github_url": "https://github.com/your-username/harbor-notes",
            "live_url": "",
            "is_featured": True,
            "display_order": 20,
        },
        {
            "title": "Civic Pulse Dashboard",
            "slug": "civic-pulse-dashboard",
            "description": (
                "Ingests public CSV feeds into PostgreSQL and exposes summary metrics "
                "through a Django admin and a small JSON API for charts."
            ),
            "technologies": "Python, Django, PostgreSQL, SQL, REST APIs",
            "github_url": "https://github.com/your-username/civic-pulse",
            "live_url": "",
            "is_featured": False,
            "display_order": 30,
        },
        {
            "title": "Deploykit",
            "slug": "deploykit",
            "description": (
                "A reference Django project showing WhiteNoise, Gunicorn, environment-based "
                "settings, and a Render-ready PostgreSQL configuration — the same patterns "
                "used to ship this portfolio."
            ),
            "technologies": "Django, Gunicorn, WhiteNoise, Docker, Render",
            "github_url": "https://github.com/your-username/deploykit",
            "live_url": "",
            "is_featured": False,
            "display_order": 40,
        },
    ]
    for payload in projects:
        Project.objects.get_or_create(slug=payload["slug"], defaults=payload)

    experiences = [
        {
            "role": "Python Developer",
            "organization": "Northline Software",
            "location": "Remote",
            "start_date": date(2023, 3, 1),
            "end_date": None,
            "description": (
                "Build and maintain Django services used by internal tools and client portals. "
                "Own schema changes, REST endpoints, and production deploys on PostgreSQL."
            ),
            "display_order": 10,
        },
        {
            "role": "Junior Backend Developer",
            "organization": "Field & Form Studio",
            "location": "Austin, TX",
            "start_date": date(2021, 6, 1),
            "end_date": date(2023, 2, 1),
            "description": (
                "Implemented Django admin workflows, form validation, and reporting queries. "
                "Helped migrate a legacy SQLite prototype to PostgreSQL."
            ),
            "display_order": 20,
        },
        {
            "role": "Python Intern",
            "organization": "Lakeview Analytics",
            "location": "Hybrid",
            "start_date": date(2020, 5, 1),
            "end_date": date(2021, 5, 1),
            "description": (
                "Wrote Python ETL scripts, cleaned datasets, and documented SQL transformations "
                "used by the research team."
            ),
            "display_order": 30,
        },
    ]
    for payload in experiences:
        Experience.objects.get_or_create(
            role=payload["role"],
            organization=payload["organization"],
            defaults=payload,
        )

    education = [
        {
            "credential": "B.S. Computer Science",
            "institution": "State University",
            "field_of_study": "Software systems",
            "start_year": 2016,
            "end_year": 2020,
            "description": "Coursework in databases, algorithms, and web systems. Senior project: a Django course catalog.",
            "display_order": 10,
        },
        {
            "credential": "Backend Web Development Certificate",
            "institution": "Independent study / professional certificate",
            "field_of_study": "Python and Django",
            "start_year": 2021,
            "end_year": 2021,
            "description": "Focused on REST APIs, relational modeling, and deploying Python web apps.",
            "display_order": 20,
        },
    ]
    for payload in education:
        Education.objects.get_or_create(
            credential=payload["credential"],
            institution=payload["institution"],
            defaults=payload,
        )

    certifications = [
        {
            "title": "Django for Professionals",
            "issuer": "Self-paced professional coursework",
            "year": 2024,
            "credential_url": "",
            "display_order": 10,
        },
        {
            "title": "PostgreSQL for Developers",
            "issuer": "Independent study",
            "year": 2023,
            "credential_url": "",
            "display_order": 20,
        },
        {
            "title": "REST API Design",
            "issuer": "Workshop series",
            "year": 2023,
            "credential_url": "",
            "display_order": 30,
        },
    ]
    for payload in certifications:
        Certification.objects.get_or_create(
            title=payload["title"],
            issuer=payload["issuer"],
            defaults=payload,
        )

    return profile, created
