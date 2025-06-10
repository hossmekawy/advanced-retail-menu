# -*- coding: utf-8 -*-
"""
إعدادات الاختبارات - Test Configuration
"""
import pytest
import tempfile
import os
from app import create_app
from extensions import db
from models import User, Settings, Category, Product


@pytest.fixture
def app():
    """إنشاء تطبيق للاختبار - Create test application"""
    # إنشاء ملف قاعدة بيانات مؤقت - Create temporary database file
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        
        # إنشاء بيانات تجريبية - Create test data
        create_test_data()
        
        yield app
        
        # تنظيف - Cleanup
        db.drop_all()
        os.close(db_fd)
        os.unlink(db_path)


@pytest.fixture
def client(app):
    """عميل الاختبار - Test client"""
    return app.test_client()


@pytest.fixture
def runner(app):
    """منفذ أوامر الاختبار - Test CLI runner"""
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    """مساعد المصادقة - Authentication helper"""
    class AuthActions:
        def __init__(self, client):
            self._client = client
        
        def login(self, username='admin', password='admin123'):
            return self._client.post('/admin/login', data={
                'username': username,
                'password': password
            })
        
        def logout(self):
            return self._client.get('/admin/logout')
    
    return AuthActions(client)


def create_test_data():
    """إنشاء بيانات تجريبية - Create test data"""
    # إنشاء مستخدم إداري - Create admin user
    admin = User(username='admin', email='admin@test.com')
    admin.set_password('admin123')
    db.session.add(admin)
    
    # إنشاء إعدادات - Create settings
    settings = Settings(
        shop_name='متجر تجريبي',
        primary_color='#3B82F6',
        secondary_color='#10B981',
        default_currency='EGP',
        default_lang='ar'
    )
    db.session.add(settings)
    
    # إنشاء فئة تجريبية - Create test category
    category = Category(
        name_ar='مشروبات',
        name_en='Beverages',
        description_ar='مشروبات متنوعة',
        description_en='Various beverages',
        is_active=True
    )
    db.session.add(category)
    db.session.commit()
    
    # إنشاء منتج تجريبي - Create test product
    product = Product(
        category_id=category.id,
        name_ar='قهوة عربية',
        name_en='Arabic Coffee',
        description_ar='قهوة عربية أصيلة',
        description_en='Authentic Arabic coffee',
        price=25.00,
        currency='EGP',
        is_active=True
    )
    db.session.add(product)
    db.session.commit()
