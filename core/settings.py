import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')


DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS if host.strip()]  # Убираем пустые значения

SITE_DOMAIN = os.getenv('SITE_DOMAIN', 'http://localhost:8000')

# ✅ Гарантируем, что `SITE_DOMAIN` входит в `ALLOWED_HOSTS`
if SITE_DOMAIN.replace("http://", "").replace("https://", "").rstrip("/") not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(SITE_DOMAIN.replace("http://", "").replace("https://", "").rstrip("/"))


INSTALLED_APPS = [
    'jazzmin',
    'tinymce',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shop.apps.ShopConfig',
    'cart.apps.CartConfig',
    'wishlist.apps.WishlistConfig',
    'account.apps.AccountConfig',
    'orders.apps.OrdersConfig',
    'about.apps.AboutConfig',
    'slider.apps.SliderConfig',
    'partners.apps.PartnersConfig',
    'parameters.apps.ParametersConfig',
    'coupons.apps.CouponsConfig',
    'mptt',
    'import_export',
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # DEBUG-TOOLBAR
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
                'wishlist.context_processors.wishlist',
                'parameters.context_processors.contact_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
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

LANGUAGE_CODE = 'az'

TIME_ZONE = 'Asia/Baku'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'shop/static'),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

CART_SESSION_ID = 'cart'
WISHLIST_SESSION_ID = 'wishlist'

AUTH_USER_MODEL = 'account.Account'
LOGIN_REDIRECT_URL = 'shop:index'
LOGIN_URL = 'account:login'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('E_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('E_H_PASSWORD')
DEFAULT_FROM_EMAIL = 'emineliyev87@gmail.com'
ADMINS = [('Admin', 'emineliyev87@gmail.com')]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',  # Адрес и порт Redis
        'OPTIONS': {
            'db': 1,  # Номер базы данных Redis
        },
        'KEY_PREFIX': 'core',  # Префикс ключей кеша
    }
}

JAZZMIN_SETTINGS = {
    "site_title": "Rafig Jewellery",
    "site_header": "İdarə etmə paneli",
    "welcome_sign": "Sistemə xoş gəlmisiniz",
    "search_model": ["auth.User", "shop.Product"],
    # Иконки моделей в боковом меню (используйте FontAwesome 5)
    "icons": {
        "account.Account": "fas fa-user",
        "auth.Group": "fas fa-users",
        "shop.Product": "fas fa-box",
        "shop.Comment": "fas fa-comment",
        "orders.Order": "fas fa-wallet",
        "about.About": "fa-solid fa-info",
        "account.Country": "fa-solid fa-globe",
        "account.City": "fa-solid fa-city",
        "shop.Category": "fa-solid fa-list",
        "shop.SuperSale": "fa-solid fa-percent",
        "slider.Slider": "fa-solid fa-camera-retro",
        "shop.Material": "fa-brands fa-slack",
        "partners.Partner": "fa-solid fa-handshake",
        "parameters.Phone": "fas fa-phone-volume",
        "parameters.Email": "fas fa-at",
        "parameters.ReturnsAndRefunds": "fas fa-sync-alt",
        "parameters.DeliveryInformation": "fas fa-truck",
        "parameters.TermsAndConditions": "fas fa-scale-balanced",
        "parameters.PrivacyPolicy": "fas fa-user-secret",
        "parameters.Contact": "fas fa-address-book",
        "coupons.Coupon": "fas fa-ticket",
    },

    # Настройки бокового меню
    "order_with_respect_to": ["auth", "myapp"],  # Сортировка моделей
    "navigation_expanded": False,  # Открытое меню по умолчанию
    "hide_apps": ["unwanted_app"],  # Скрыть приложения
    "hide_models": ["myapp.OldModel"],  # Скрыть модели
    "custom_links": {
        "myapp": [
            {
                "name": "Добавить продукт",
                "url": "admin:myapp_product_add",
                "icon": "fas fa-plus",
            }
        ]
    },
    # Цветовая схема
    "theme": "darkly",  # Выберите тему (см. список тем ниже)
    "show_ui_builder": True,  # Показывать кнопку UI Builder

    # Логотип (путь к статике)
    "site_logo": "assets/images/logoAdmin.png",
    "site_logo_classes": "img-circle"

}

TINYMCE_DEFAULT_CONFIG = {
    'height': 300,
    'width': '100%',
    'menubar': 'file edit view insert format tools table help',
    'plugins': 'advlist autolink lists link image charmap print preview hr anchor pagebreak',
    'toolbar': 'undo redo | styleselect | bold italic | alignleft aligncenter alignright alignjustify | '
               'bullist numlist outdent indent | link image | print preview media fullpage | '
               'forecolor backcolor emoticons',
    'image_advtab': True,
}

# DEBUG-TOOLBAR
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
