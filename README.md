# Python Developer Portfolio

A production-minded Django portfolio site for a Python developer. Content is stored in the database and edited through Django Admin — names, bio, photo, skills, projects, experience, education, certifications, and social links can all be changed without touching templates.

The public site is a single-page layout with sticky navigation, a dark/light theme, a validated contact form, and SEO basics (title, meta description, Open Graph tags, `robots.txt`, and a sitemap).

## Features

- Hero, About, Skills, Projects, Experience/Education, Certifications, Contact, and Footer
- Django models + Admin for all portfolio content
- Contact form with CSRF protection, field validation, honeypot, and stored messages
- Responsive layout, sticky nav, mobile menu, theme toggle, reduced-motion support
- WhiteNoise for compressed static files
- SQLite locally, PostgreSQL in production via `DATABASE_URL`
- Render Blueprint (`render.yaml`) with Gunicorn

## Tech stack

- Python 3.13+ (local 3.14 is fine; Render is pinned to 3.13 in `runtime.txt`)
- Django 5.2
- HTML5, CSS3, JavaScript
- SQLite / PostgreSQL
- Gunicorn
- WhiteNoise
- Pillow (project and profile images)

## Project structure

```text
python_portfolio/
├── config/                 # Django project package
│   ├── settings/
│   │   ├── base.py         # Shared settings
│   │   ├── development.py  # DEBUG, SQLite, local hosts
│   │   └── production.py   # HTTPS, secure cookies, WhiteNoise hashes
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── portfolio/              # Main app (models, admin, views, seed data)
├── templates/              # Template inheritance + section includes
├── static/                 # CSS, JS, favicon, placeholder images
├── media/                  # User uploads (gitignored except .gitkeep)
├── manage.py
├── gunicorn.conf.py
├── render.yaml
├── requirements.txt
└── runtime.txt
```

## Local setup

```bash
cd python_portfolio
python -m venv .venv

# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env   # Windows
# cp .env.example .env   # macOS / Linux
```

Generate a secret key if you want something unique:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Paste it into `.env` as `SECRET_KEY`.

## Environment variables

| Variable | Local | Production |
| --- | --- | --- |
| `SECRET_KEY` | required (a fallback exists only in development) | **required** |
| `DEBUG` | `True` | `False` |
| `ALLOWED_HOSTS` | `127.0.0.1,localhost` | your Render host, e.g. `your-app.onrender.com,.onrender.com` |
| `CSRF_TRUSTED_ORIGINS` | `http://127.0.0.1:8000,http://localhost:8000` | `https://your-app.onrender.com` |
| `DATABASE_URL` | empty = SQLite | Render PostgreSQL URL |
| `DATABASE_SSL_REQUIRE` | `False` | `True` |
| `DJANGO_SETTINGS_MODULE` | `config.settings.development` (default in `manage.py`) | `config.settings.production` |

## Database setup

Local development uses SQLite (`db.sqlite3`) when `DATABASE_URL` is empty.

```bash
python manage.py migrate
python manage.py seed_portfolio
```

`migrate` already loads placeholder content. `seed_portfolio` is safe to re-run; use `--replace` only if you want to wipe portfolio rows and restore the demo content.

To use PostgreSQL locally:

```bash
# .env
DATABASE_URL=postgres://USER:PASSWORD@localhost:5432/portfolio
```

Then migrate again.

## Django Admin

```bash
python manage.py createsuperuser
```

Open http://127.0.0.1:8000/admin/ and update:

- **Site profile** — name, title, intro, about copy, photo, email, GitHub, LinkedIn, SEO
- **Skills** — badges and copy (`icon_key` values: `python`, `django`, `drf`, `html`, `css`, `javascript`, `sql`, `postgres`, `git`, `api`, `docker`)
- **Projects** — title, description, technologies, image, GitHub, live URL, featured flag
- **Experience / Education / Certifications**
- **Contact messages** — inbound form submissions

## How to run locally

```bash
python manage.py runserver
```

Visit http://127.0.0.1:8000/

Useful checks:

```bash
python manage.py check
python manage.py collectstatic --no-input
```

## GitHub setup

```bash
git init
git add .
git commit -m "Initial Django portfolio"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

Do not commit `.env` or `db.sqlite3`.

## Render deployment

### Option A — Blueprint (`render.yaml`)

1. Push the repo to GitHub.
2. In Render: **New → Blueprint**.
3. Connect the repository.
4. Render creates the web service and a PostgreSQL database from `render.yaml`.
5. After the first deploy, create a superuser (see below).
6. Set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to your real `https://<service>.onrender.com` URL if you want them locked down instead of the `*.onrender.com` wildcard.

### Option B — Manual web service

1. **New → PostgreSQL**. Copy the **Internal Database URL**.
2. **New → Web Service**, connect the GitHub repo.
3. Runtime: Python.
4. Build command:

   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate
   ```

5. Start command:

   ```bash
   gunicorn --config gunicorn.conf.py config.wsgi:application
   ```

   Equivalent form:

   ```bash
   gunicorn config.wsgi:application
   ```

   (`gunicorn.conf.py` binds `0.0.0.0:$PORT`.)

6. Environment variables:

   | Key | Value |
   | --- | --- |
   | `DJANGO_SETTINGS_MODULE` | `config.settings.production` |
   | `SECRET_KEY` | generate in Render or use a long random string |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `your-service.onrender.com,.onrender.com` |
   | `CSRF_TRUSTED_ORIGINS` | `https://your-service.onrender.com` |
   | `DATABASE_URL` | from the Render Postgres instance |
   | `DATABASE_SSL_REQUIRE` | `True` |
   | `PYTHON_VERSION` | `3.13.4` |

### Create a superuser on Render

In the service **Shell**:

```bash
python manage.py createsuperuser
```

Then sign in at `https://your-service.onrender.com/admin/`.

### Media files on Render

The local disk on a free web service is ephemeral. Profile and project images uploaded in Admin will disappear on rebuild unless you attach a **persistent disk** mounted at the project `media/` directory, or switch to object storage later. Placeholder SVGs in `static/img/` always ship with the app.

## Replacing placeholder content

Demo identity is **Jordan Hale**. Change it in Admin → Site profile (and GitHub/LinkedIn/email). Project repos point at `your-username` on purpose so you can swap URLs in one place.

## License

Use and modify freely for your own portfolio.
