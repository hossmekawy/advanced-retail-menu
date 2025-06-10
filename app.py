# -*- coding: utf-8 -*-
"""
التطبيق الرئيسي - Main Application
"""
import os
from flask import Flask, session, request
# from dotenv import load_dotenv  # Uncomment after installing python-dotenv
from config import config
from extensions import init_extensions, db, login_manager
from models import User, Settings
from i18n import _, get_current_language

# Load environment variables from .env file
# load_dotenv()  # Uncomment after installing python-dotenv


def create_app(config_name=None):
    """مصنع التطبيق - Application factory"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # تهيئة الملحقات - Initialize extensions
    init_extensions(app)
    
    # تسجيل البلوبرينتس - Register blueprints
    from core import bp as core_bp
    from admin import bp as admin_bp
    from api import bp as api_bp
    
    app.register_blueprint(core_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # إعداد مدير تسجيل الدخول - Setup login manager
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # إعداد اللغة - Setup language (simplified without Babel)
    def get_locale():
        # التحقق من اللغة في الجلسة - Check language in session
        if 'lang' in session:
            return session['lang']

        # التحقق من اللغة في الإعدادات - Check language in settings
        settings = Settings.get_settings()
        if settings.default_lang:
            return settings.default_lang

        # استخدام اللغة الافتراضية - Use default language
        return 'ar'
    
    # متغيرات السياق العامة - Global context variables
    @app.context_processor
    def inject_global_vars():
        """حقن المتغيرات العامة في جميع القوالب - Inject global variables into all templates"""
        from models import ContentPage
        from flask_login import current_user
        settings = Settings.get_settings()
        footer_page = ContentPage.get_page('footer')
        return {
            'settings': settings,
            'footer_page': footer_page,
            'current_lang': get_locale(),
            'available_languages': app.config['LANGUAGES'],
            'available_currencies': app.config['CURRENCIES'],
            'current_user': current_user,  # Make current_user available in templates
            '_': _  # Make translation function available in templates
        }
    
    # معالج الأخطاء - Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('core/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('core/500.html'), 500
    
    # إنشاء الجداول والبيانات الأولية - Create tables and initial data
    with app.app_context():
        db.create_all()

        # إنشاء مستخدم افتراضي - Create default user
        if not User.query.first():
            admin_user = User(
                username='admin',
                email='admin@example.com'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()

        # إنشاء إعدادات افتراضية - Create default settings
        Settings.get_settings()
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
