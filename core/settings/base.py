from pathlib import Path

# Base settings for both environments
BASE_DIR = Path(__file__).resolve().parent.parent.parent

import os
from dotenv import load_dotenv

dotenv_path = os.path.join(BASE_DIR, ".env")
if os.path.isfile(dotenv_path):
    load_dotenv(dotenv_path=dotenv_path)
else:
    print(f".env file not found at {dotenv_path}")

SECRET_KEY = os.getenv("SECRET_KEY", "g$hkBq>=B$fzOYV")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")

print(f"LOADED API_VERSION: {os.getenv('API_VERSION')}")


def get_modules_for_version(api_version):
    modules_path = Path(BASE_DIR) / "src" / "api" / api_version / "modules"

    if not modules_path.exists():
        print(f"Path does not exist: {modules_path}")

    modules = []
    for module in modules_path.glob("*"):
        if module.is_dir():
            module_name = f"src.api.{api_version}.modules.{module.name}"
            print(f"INITIALIZING MODULE: {module_name}")
            modules.append(module_name)

    return modules


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
] + get_modules_for_version(os.getenv("API_VERSION"))

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = "/static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

APPEND_SLASH = False
