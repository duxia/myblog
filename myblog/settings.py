"""
Django settings for myblog project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*+l)f)!k!&nx-$i6uhs%#^j3e)088wwb$vc&1pv+2@s1!fq9=+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

#ckeditor
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
CKEDITOR_UPLOAD_PATH = "uploads/"
#CKEDITOR_JQUERY_URL = "/static/jquery/jquery.min.js"
CKEDITOR_CONFIGS = {
    'default': {
        'extraPlugins' : 'clipboard,lineutils,widget,dialog,codesnippet,lineheight',
        'toolbar': (
            ['div','Source','-','Save','NewPage','Preview','-','Templates'], 
            ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print','SpellChecker','Scayt'], 
            ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'], 
            ['Form','Checkbox','Radio','TextField','Textarea','Select','Button', 'ImageButton','HiddenField'], 
            ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'], 
            ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'], 
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'], 
            ['Link','Unlink','Anchor'], 
            ['CodeSnippet','Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'], 
            ['Styles','Format','Font','FontSize','lineheight'],
            ['TextColor','BGColor'], 
            ['Maximize','ShowBlocks','-','About', 'pbckcode'],
        ),
        'height':1000,
    },
}

INSTALLED_APPS = (
    'django_admin_bootstrapped.bootstrap3',#bootstrap admin
    'django_admin_bootstrapped',#bootstrap admin
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',
    'ckeditor',
    'mptt',
    'social_login',
    'captcha',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_login.middleware.SocialLoginUser',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    #'django.core.context_processors.request',
    'social_login.context_processors.social_sites',
)

ROOT_URLCONF = 'myblog.urls'

WSGI_APPLICATION = 'myblog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


SOCIAL_LOGIN_USER_INFO_MODEL='blog.UserInfo'
SOCIAL_LOGIN_ERROR_REDIRECT_URL = '/account/login/error'
SOCIALOAUTH_SITES = (
    ('qq', 'socialoauth.sites.qq.QQ', 'QQ',
        {
          'redirect_uri': 'http://test.codeshift.org/account/oauth/qq',
          'client_id': 'YOUR ID',
          'client_secret': 'YOUR SECRET',
        }
    ),
)
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

# STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)