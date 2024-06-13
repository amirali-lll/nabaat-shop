from datetime import timedelta
import os
from pathlib import Path
from environ import Env

env = Env()
Env.read_env()


VERSION  = "1"

BASE_URL = f"api/v{VERSION}"

BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
SECRET_KEY = env("SECRET_KEY")

DEBUG = False

ALLOWED_HOSTS = ['*']

CSRF_TRUSTED_ORIGINS=[
    'https://*.fiust.ir',
    'https://*.nabaat.shop',
    ]


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third party apps
    'rest_framework',
    'drf_yasg',
    # Local apps
    'core',
    'authentication',
    'store',

]

MIDDLEWARE = [
    'core.middleware.corsheaders.CorsMiddlewareDjango',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'nabaatshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'nabaatshop.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': env("DB_ENGINE"),
        'NAME': env("DB_NAME"),
        'USER': env("DB_USER"),
        'PASSWORD': env("DB_PASSWORD"),
        'HOST': env("DB_HOST"),
        'PORT': env("DB_PORT"),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'authentication.User'

LANGUAGE_CODE = 'en'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True


STATIC_URL = f'api/v{VERSION}/static/'

STATIC_ROOT = "/var/www/nabaatshop/static"

MEDIA_URL = f'api/v{VERSION}/media/'

MEDIA_ROOT = "/var/www/nabaatshop/media"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES" : ('JWT','Bearer'),
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=300),
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}


LOGGING ={
    'version':1,
    'disable_existing_loggers':False,
    'handlers':{
        'console':{
            'class':'logging.StreamHandler'
        },
        'file':{
            'class':'logging.FileHandler',
            'filename':'general.log',
            'formatter': 'verbose'
        }
    },
    'loggers':{
        '':{
            'handlers':['file','console'],
            'level':'INFO'
        }
    },
    'formatters':{
        'verbose':{
            'format':'{asctime} ({levelname}) - {name} - {message}',
            'style' :'{'
        }

    }
}


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
}

JAZZMIN_SETTINGS = {
    "site_title": "NABAAT",
    "site_brand": "Nabaat Administration",
    "site_logo": "core/img/logo.png",
    "custom_css": "core/css/custom.css",
    "welcome_sign": "Welcome to Nabaat shop",
    "copyright": "NABAAT",
    "related_modal_active": True,
    "topmenu_links": [

        {"name": "Home",  "url": "admin:index", "permissions": ["auth.view_user"]},

        {"model": "store.order"},

        {"app": "store"},
    ],
    "icons": {
        "authentication": "fas fa-users-cog",
        "authentication.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "store": "fas fa-store",
        
        "store.Address": "fas fa-home",
        "store.Customer": "fas fa-user-astronaut",
        "store.Plant": "fas fa-leaf",
        "store.Order": "fas fa-shopping-cart",
        "store.Accessory": "fas fa-dolly",
        "store.Category": "fas fa-stream",
        "store.Product": "fas fa-seedling",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-olive",
    "navbar": "navbar-gray navbar-dark",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-olive",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}
