# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات - Database Models
"""
from datetime import datetime
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(UserMixin, db.Model):
    """نموذج المستخدم - User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """تشفير كلمة المرور - Hash password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """التحقق من كلمة المرور - Check password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Settings(db.Model):
    """إعدادات المتجر - Shop settings"""
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(200), nullable=False, default='متجري')
    primary_color = db.Column(db.String(7), default='#3B82F6')
    secondary_color = db.Column(db.String(7), default='#10B981')
    logo_b64 = db.Column(db.Text)  # Base64 encoded logo
    default_currency = db.Column(db.String(3), default='EGP')
    default_lang = db.Column(db.String(2), default='ar')

    # روابط التواصل الاجتماعي - Social media links
    facebook_url = db.Column(db.String(500))
    twitter_url = db.Column(db.String(500))
    instagram_url = db.Column(db.String(500))
    whatsapp_url = db.Column(db.String(500))

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get_settings(cls):
        """الحصول على الإعدادات أو إنشاء إعدادات افتراضية - Get settings or create default"""
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings
    
    def __repr__(self):
        return f'<Settings {self.shop_name}>'


class Category(db.Model):
    """فئة المنتجات - Product category"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Font Awesome icon class
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات - Relationships
    subcategories = db.relationship('SubCategory', backref='category', lazy=True, cascade='all, delete-orphan')
    products = db.relationship('Product', backref='category', lazy=True)
    
    def get_name(self, lang='ar'):
        """الحصول على الاسم باللغة المحددة - Get name in specified language"""
        return getattr(self, f'name_{lang}', self.name_ar)
    
    def get_description(self, lang='ar'):
        """الحصول على الوصف باللغة المحددة - Get description in specified language"""
        return getattr(self, f'description_{lang}', self.description_ar)
    
    def __repr__(self):
        return f'<Category {self.name_ar}>'


class SubCategory(db.Model):
    """فئة فرعية - Subcategory"""
    __tablename__ = 'subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات - Relationships
    products = db.relationship('Product', backref='subcategory', lazy=True)
    
    def get_name(self, lang='ar'):
        """الحصول على الاسم باللغة المحددة - Get name in specified language"""
        return getattr(self, f'name_{lang}', self.name_ar)
    
    def get_description(self, lang='ar'):
        """الحصول على الوصف باللغة المحددة - Get description in specified language"""
        return getattr(self, f'description_{lang}', self.description_ar)
    
    def __repr__(self):
        return f'<SubCategory {self.name_ar}>'


class Product(db.Model):
    """منتج - Product"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'))
    name_ar = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    ingredients_ar = db.Column(db.Text)
    ingredients_en = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='EGP')
    photo_b64 = db.Column(db.Text)  # Base64 encoded image
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_name(self, lang='ar'):
        """الحصول على الاسم باللغة المحددة - Get name in specified language"""
        return getattr(self, f'name_{lang}', self.name_ar)
    
    def get_description(self, lang='ar'):
        """الحصول على الوصف باللغة المحددة - Get description in specified language"""
        return getattr(self, f'description_{lang}', self.description_ar)
    
    def get_ingredients(self, lang='ar'):
        """الحصول على المكونات باللغة المحددة - Get ingredients in specified language"""
        return getattr(self, f'ingredients_{lang}', self.ingredients_ar)
    
    def get_formatted_price(self):
        """الحصول على السعر منسق - Get formatted price"""
        return f"{self.price} {self.currency}"
    
    def __repr__(self):
        return f'<Product {self.name_ar}>'


class Translation(db.Model):
    """ترجمات تلقائية - Auto translations cache"""
    __tablename__ = 'translations'

    id = db.Column(db.Integer, primary_key=True)
    text_key = db.Column(db.String(255), nullable=False)
    source_lang = db.Column(db.String(2), nullable=False)
    target_lang = db.Column(db.String(2), nullable=False)
    source_text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('text_key', 'source_lang', 'target_lang'),
    )


class ContentPage(db.Model):
    """صفحات المحتوى القابلة للتحرير - Editable content pages"""
    __tablename__ = 'content_pages'

    id = db.Column(db.Integer, primary_key=True)
    page_key = db.Column(db.String(50), unique=True, nullable=False)  # about, contact, footer
    title_ar = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    content_ar = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text, nullable=False)
    meta_description_ar = db.Column(db.Text)
    meta_description_en = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_title(self, lang='ar'):
        """الحصول على العنوان حسب اللغة - Get title by language"""
        return getattr(self, f'title_{lang}', self.title_ar)

    def get_content(self, lang='ar'):
        """الحصول على المحتوى حسب اللغة - Get content by language"""
        return getattr(self, f'content_{lang}', self.content_ar)

    def get_meta_description(self, lang='ar'):
        """الحصول على وصف الميتا حسب اللغة - Get meta description by language"""
        return getattr(self, f'meta_description_{lang}', self.meta_description_ar)

    @staticmethod
    def get_page(page_key):
        """الحصول على صفحة بالمفتاح - Get page by key"""
        return ContentPage.query.filter_by(page_key=page_key, is_active=True).first()

    @staticmethod
    def get_or_create_page(page_key, default_title_ar, default_title_en, default_content_ar, default_content_en):
        """الحصول على صفحة أو إنشاؤها - Get or create page"""
        page = ContentPage.query.filter_by(page_key=page_key).first()
        if not page:
            page = ContentPage(
                page_key=page_key,
                title_ar=default_title_ar,
                title_en=default_title_en,
                content_ar=default_content_ar,
                content_en=default_content_en
            )
            db.session.add(page)
            db.session.commit()
        return page

    def __repr__(self):
        return f'<ContentPage {self.page_key}>'
    
    def __repr__(self):
        return f'<Translation {self.text_key} {self.source_lang}->{self.target_lang}>'
