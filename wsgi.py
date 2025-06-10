# -*- coding: utf-8 -*-
"""
نقطة دخول WSGI للنشر - WSGI entry point for deployment
"""
import os
from app import create_app

# إنشاء التطبيق - Create application
app = create_app(os.environ.get('FLASK_ENV', 'production'))

if __name__ == "__main__":
    app.run()
