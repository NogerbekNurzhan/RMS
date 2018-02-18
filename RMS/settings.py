import os
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = ''

DEBUG = True

ALLOWED_HOSTS = [
    'rms',
    '127.0.0.1'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'account',  # django-registration-redux
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rosetta',  # django-rosetta
    'captcha',  # django-recaptcha
    'social_django',  # python-social-auth
    'project',
    'widget_tweaks',  # django-widget-tweaks
    'reversion',  # django-reversion
    'django_select2',  # django_select2
    'el_pagination',  # django_el_pagination
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'RMS.urls'

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
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'RMS.wsgi.application'

# Django backend for Microsoft SQL Server | (django-pyodbc-azure package)
DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'host_is_server': True,
            'autocommit': True,
            'unicode_results': True,
            'extra_params': 'tds_version=8.0'
        },
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

LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# START: Static and Media files settings
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media_root')
MEDIA_URL = '/media/'
# END: Static and Media files settings

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

# START: SMTP settings
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = True
SERVER_EMAIL = None
# END: SMTP settings

# START: LOGIN and LOGOUT URLs
LOGIN_URL = reverse_lazy('auth_login')
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL = reverse_lazy('auth_logout')
LOGOUT_REDIRECT_URL = reverse_lazy('home')
# END: LOGIN and LOGOUT URLs

# START: Django Registration Redux settings
SITE_ID = 1
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True  # If REGISTRATION_AUTO_LOGIN is True, users will automatically log in when they click on the activation link in their email.
# END: Django Registration Redux settings

# START: Google ReCAPTCHA settings
RECAPTCHA_PUBLIC_KEY = ''
RECAPTCHA_PRIVATE_KEY = ''
NOCAPTCHA = True
# END: Google ReCAPTCHA settings

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = ''
SOCIAL_AUTH_FACEBOOK_SECRET = ''
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'fields': 'name, email'}

SOCIAL_AUTH_VK_OAUTH2_KEY = ''  # ID приложения
SOCIAL_AUTH_VK_OAUTH2_SECRET = ''  # Защищённый ключ
SOCIAL_AUTH_VK_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = ''
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email']

SOCIAL_AUTH_GITHUB_KEY = ''
SOCIAL_AUTH_GITHUB_SECRET = ''
SOCIAL_AUTH_GITHUB_SCOPE = ['email']

# Used to redirect new registered users, will be used in place of SOCIAL_AUTH_LOGIN_REDIRECT_URL if defined.
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = reverse_lazy('set_password')

SOCIAL_AUTH_PIPELINE = (
    # Get the information we can about the user and return it in a simple format to create the user instance later.
    # On some cases the details are already part of the auth response from the provider, but sometimes this could hit a provider API.
    'social.pipeline.social_auth.social_details',

    # Get the social uid from whichever service we're using through.
    # The uid is the unique identifier of the given user in the provider.
    'social.pipeline.social_auth.social_uid',

    # Verifies that the current auth process is valid within the current project, this is where emails and domains whitelists are applied (if defined).
    'social.pipeline.social_auth.auth_allowed',

    # Checks if the current social-account is already associated in the site.
    'social.pipeline.social_auth.social_user',

    # Make up a username for this person, appends a random string at the end if  there's any collision.
    'social.pipeline.user.get_username',

    # Send a validation email to the user to verify its email address. Disabled by default.
    'social.pipeline.mail.mail_validation',

    # Associates the current social details with another user account with a similar email address. Disabled by default.
    'social.pipeline.social_auth.associate_by_email',

    # Create a user account if we haven't found one yet.
    'social.pipeline.user.create_user',

    # Create the record that associates the social account with the user.
    'social.pipeline.social_auth.associate_user',

    # Populate the extra_data field in the social record with the values specified by settings (and the default ones like access_token, etc).
    'social.pipeline.social_auth.load_extra_data',

    # Update the user record with any changed info from the auth service.
    # Update user details using data from provider.
    'social.pipeline.user.user_details'
)
