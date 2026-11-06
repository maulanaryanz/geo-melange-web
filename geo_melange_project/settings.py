import os
from pathlib import Path
from dotenv import load_dotenv

# Menentukan direktori dasar proyek (D:\Geo Melange Project)
BASE_DIR = Path(__file__).resolve().parent.parent

# Memuat konfigurasi dari berkas .env di folder utama proyek
load_dotenv(BASE_DIR / '.env')


# ==============================================================================
# 1. KONFIGURASI INTI & KEAMANAN DASAR (DARI .ENV)
# ==============================================================================

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-kunci-cadangan-lokal-sementara'
)

# Bernilai True jika di .env tertulis DEBUG=True, selain itu otomatis False
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Mengambil daftar domain dari .env dan memisahkannya berdasarkan tanda koma
ALLOWED_HOSTS = [
    host.strip() 
    for host in os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') 
    if host.strip()
]

CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://127.0.0.1:8000').split(',')
    if origin.strip()
]

# ==============================================================================
# 2. APLIKASI & MIDDLEWARE
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Aplikasi utama CV. Geo Melange
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Mengelola file statis saat di-hosting
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

PROJECT_FOLDER = Path(__file__).resolve().parent.name

ROOT_URLCONF = f'{PROJECT_FOLDER}.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

# PENTING: Sesuaikan nama 'geomelange' di bawah ini dengan nama folder tempat settings.py Anda berada
WSGI_APPLICATION = f'{PROJECT_FOLDER}.wsgi.application'


# ==============================================================================
# 3. BASIS DATA (DATABASE)
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ==============================================================================
# 4. VALIDASI KATA SANDI ADMIN
# ==============================================================================

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


# ==============================================================================
# 5. LOKALISASI BAHASA & ZONA WAKTU
# ==============================================================================

LANGUAGE_CODE = 'id'

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_TZ = True


# ==============================================================================
# 6. PENGATURAN FILE STATIS, MEDIA, & BATAS UPLOAD
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Otomatis membaca folder static lokal jika folder tersebut tersedia
if (BASE_DIR / 'static').exists():
    STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Batas ukuran unggahan di level server (Default: 2.5 MB = 2621440 Bytes)
MAX_UPLOAD_SIZE = int(os.environ.get('MAX_UPLOAD_SIZE', 2621440))
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_UPLOAD_SIZE

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# 7. KEAMANAN SERVER PRODUKSI (AKTIF OTOMATIS SAAT DEBUG=False DI HOSTING)
# ==============================================================================

if not DEBUG:
    #SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True