import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "dev-secret-key")

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]  # Render le pondrá el dominio real

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",  # 👈 agregado
    "playlist",     # tu app
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # 👈 agregado
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'reproductor.wsgi.application'

# 👇 AGREGA ESTA LÍNEA para quitar el warning de claves primarias
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Permitir llamadas desde tu frontend en Vercel
CORS_ALLOWED_ORIGINS = [
    "https://tu-frontend.vercel.app",  # 👈 cambia por el dominio real de Vercel
]

# Base de datos (Render usa Postgres)
DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///" + str(BASE_DIR / "db.sqlite3"),
        conn_max_age=600,
        ssl_require=True,
    )
}

# Archivos estáticos para Render
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
