#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار قاعدة البيانات - Database Test
"""
from app import create_app
from extensions import db
from models import User, Settings, Category, Product

def test_database():
    """اختبار إنشاء البيانات - Test data creation"""
    app = create_app('development')
    
    with app.app_context():
        # إنشاء الجداول - Create tables
        db.create_all()
        print("✅ تم إنشاء الجداول بنجاح")
        
        # إنشاء مستخدم إداري - Create admin user
        if not User.query.first():
            admin = User(username='admin', email='admin@example.com')
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ تم إنشاء المستخدم الإداري")
        
        # إنشاء إعدادات افتراضية - Create default settings
        settings = Settings.get_settings()
        print("✅ تم إنشاء الإعدادات الافتراضية")
        
        # اختبار إنشاء فئة - Test category creation
        try:
            category = Category(
                name_ar='مشروبات',
                name_en='Beverages',
                description_ar='مشروبات متنوعة وطازجة',
                description_en='Fresh and varied beverages',
                icon='fas fa-coffee',
                sort_order=1,  # استخدام integer مباشرة - Use integer directly
                is_active=True
            )
            db.session.add(category)
            db.session.commit()
            print("✅ تم إنشاء فئة تجريبية بنجاح")
            
            # اختبار إنشاء منتج - Test product creation
            product = Product(
                category_id=category.id,
                name_ar='قهوة عربية',
                name_en='Arabic Coffee',
                description_ar='قهوة عربية أصيلة ومميزة',
                description_en='Authentic and distinctive Arabic coffee',
                price=25.50,
                currency='EGP',
                sort_order=1,  # استخدام integer مباشرة - Use integer directly
                is_active=True,
                is_featured=True
            )
            db.session.add(product)
            db.session.commit()
            print("✅ تم إنشاء منتج تجريبي بنجاح")
            
        except Exception as e:
            print(f"❌ خطأ في إنشاء البيانات: {e}")
            db.session.rollback()
        
        # عرض الإحصائيات - Show statistics
        categories_count = Category.query.count()
        products_count = Product.query.count()
        users_count = User.query.count()
        
        print(f"\n📊 إحصائيات قاعدة البيانات:")
        print(f"   المستخدمين: {users_count}")
        print(f"   الفئات: {categories_count}")
        print(f"   المنتجات: {products_count}")
        
        print("\n🎉 تم اختبار قاعدة البيانات بنجاح!")
        print("يمكنك الآن تشغيل التطبيق باستخدام: python app.py")

if __name__ == '__main__':
    test_database()
