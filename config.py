# -*- coding: utf-8 -*-
"""
تكوين التطبيق - Application Configuration
"""
import os
from datetime import timedelta


class Config:
    """Base configuration class"""
    
    # أساسيات التطبيق - Application basics
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # قاعدة البيانات - Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///shop_menu.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # رفع الملفات - File uploads
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024  # 1MB max file size
    UPLOAD_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.webp']
    
    # الأمان - Security
    WTF_CSRF_ENABLED = True
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # التدويل - Internationalization
    LANGUAGES = {
        'ar': 'العربية',
        'en': 'English',
        'fr': 'Français',
        'es': 'Español'
    }
    BABEL_DEFAULT_LOCALE = 'ar'
    BABEL_DEFAULT_TIMEZONE = 'UTC'
    
    # العملات المدعومة - Supported currencies
    CURRENCIES = {
        'EGP': 'جنيه مصري',
        'USD': 'دولار أمريكي', 
        'EUR': 'يورو',
        'SAR': 'ريال سعودي',
        'AED': 'درهم إماراتي'
    }
    DEFAULT_CURRENCY = 'EGP'
    
    # الألوان الافتراضية - Default colors
    DEFAULT_PRIMARY_COLOR = '#3B82F6'
    DEFAULT_SECONDARY_COLOR = '#10B981'


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

    # استخدم متغيرات البيئة في الإنتاج - Use environment variables in production
    SECRET_KEY = os.environ.get('SECRET_KEY') or Config.SECRET_KEY


class DeploymentConfig(ProductionConfig):
    """Deployment configuration - same as production"""
    pass


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False


# تكوين التطبيق حسب البيئة - Application config by environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'deployment': DeploymentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
