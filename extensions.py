# -*- coding: utf-8 -*-
"""
ملحقات Flask - Flask Extensions
"""
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# تهيئة الملحقات - Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

# إعدادات مدير تسجيل الدخول - Login manager settings
login_manager.login_view = 'admin.login'
login_manager.login_message = 'يرجى تسجيل الدخول للوصول لهذه الصفحة'
login_manager.login_message_category = 'info'


def init_extensions(app):
    """تهيئة جميع الملحقات مع التطبيق - Initialize all extensions with app"""
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
