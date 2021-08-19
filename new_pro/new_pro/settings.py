"""
Django settings for new_pro project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
import django.contrib.sessions.backends.base
import django_redis.client

BASE_DIR = Path(__file__).resolve().parent.parent
import os

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-y16y45sjey6jc#pq!!_cwdb4^f+)=$efk8j3rh86pkoqqipx34'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'new_pro.urls'

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

WSGI_APPLICATION = 'new_pro.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'newblog',
        'USER': 'root',
        'PASSWORD': '1819332785',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
#redis配置
CACHES={
    "default":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://127.0.0.1:6379/0",
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient"
        }
    },
    "session":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://127.0.0.1:6379/1",
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient"
        }
    }
}
SESSION_ENGINE="django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS="session"

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
#静态资源配置
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#日志
LOGGING={
    'version':1,
    'disable_existing_loggers':False,#禁用已存在的日志器
    #日志信息显示的格式
    'formatters':{
        'verbose':{
            'format':'%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple':{
            'format':'%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    # #对日志进行过滤
    # 'filters':{
    #     'require_debug_true':{
    #         '()':'django.utils.log.RequireDebugTure',
    #     },
    # },
    #日志处理方法
    'handlers':{
        #向终端中输出日志
        # 'console':{
        #     'level':'INFO',
        #     'filters':['require_debug_true'],
        #     'class':'logging.StreamHandler',
        #     'formatter':'simple'
        # },
        #向文件中输出日志
        'file':{
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename':os.path.join(BASE_DIR,'logs/blog.log'),
            'maxBytes':300*1024*1024,
            'backupCount':10,
            'formatter':'verbose'
        },
    },
    #日志器
    'loggers':{
        #定义名为django的日志器
        'django':{
            #向文件中输出日志
            'handlers':['file'],
            #是否继续传递日志信息
            'propagate':True,
            #日志器接受的最低日志级别
            'level':'INFO'
        }
    }
}
#替换自带的user模型
AUTH_USER_MODEL='users.User'

#修改系统自动跳转链接
LOGIN_URL='/login/'

#设置上传图片保存路径
MEDIA_ROOT=os.path.join(BASE_DIR,'media/')

#设置图片访问的同一路由
MEDIA_URL='/media/'