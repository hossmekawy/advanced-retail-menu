#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تهيئة بيانات المطعم - Restaurant Data Initialization
"""
from app import create_app
from extensions import db
from models import RestaurantTable, Category, Product

def init_restaurant_data():
    """تهيئة بيانات المطعم الأساسية - Initialize basic restaurant data"""
    app = create_app()
    
    with app.app_context():
        print("تهيئة بيانات المطعم...")
        
        # إنشاء الطاولات - Create tables
        tables_data = [
            {'table_number': 1, 'capacity': 2, 'status': 'available'},
            {'table_number': 2, 'capacity': 4, 'status': 'available'},
            {'table_number': 3, 'capacity': 4, 'status': 'available'},
            {'table_number': 4, 'capacity': 6, 'status': 'available'},
            {'table_number': 5, 'capacity': 2, 'status': 'available'},
            {'table_number': 6, 'capacity': 8, 'status': 'available'},
            {'table_number': 7, 'capacity': 4, 'status': 'available'},
            {'table_number': 8, 'capacity': 2, 'status': 'available'},
        ]
        
        for table_data in tables_data:
            existing_table = RestaurantTable.query.filter_by(table_number=table_data['table_number']).first()
            if not existing_table:
                table = RestaurantTable(**table_data)
                db.session.add(table)
                print(f"تم إنشاء طاولة رقم {table_data['table_number']}")
        
        # إنشاء فئات المنتجات إذا لم تكن موجودة - Create product categories if not exist
        categories_data = [
            {
                'name_ar': 'المشروبات الساخنة',
                'name_en': 'Hot Drinks',
                'description_ar': 'قهوة وشاي وشوكولاتة ساخنة',
                'description_en': 'Coffee, tea and hot chocolate',
                'icon': 'fas fa-coffee',
                'sort_order': 1
            },
            {
                'name_ar': 'المشروبات الباردة',
                'name_en': 'Cold Drinks',
                'description_ar': 'عصائر طبيعية ومشروبات غازية',
                'description_en': 'Fresh juices and soft drinks',
                'icon': 'fas fa-glass-whiskey',
                'sort_order': 2
            },
            {
                'name_ar': 'الوجبات الرئيسية',
                'name_en': 'Main Dishes',
                'description_ar': 'أطباق رئيسية متنوعة',
                'description_en': 'Various main dishes',
                'icon': 'fas fa-utensils',
                'sort_order': 3
            },
            {
                'name_ar': 'الحلويات',
                'name_en': 'Desserts',
                'description_ar': 'حلويات شرقية وغربية',
                'description_en': 'Eastern and western desserts',
                'icon': 'fas fa-birthday-cake',
                'sort_order': 4
            }
        ]
        
        for cat_data in categories_data:
            existing_cat = Category.query.filter_by(name_ar=cat_data['name_ar']).first()
            if not existing_cat:
                category = Category(**cat_data)
                db.session.add(category)
                print(f"تم إنشاء فئة: {cat_data['name_ar']}")
        
        # حفظ التغييرات - Save changes
        db.session.commit()
        
        # إنشاء منتجات تجريبية - Create sample products
        sample_products = [
            {
                'name_ar': 'قهوة عربية',
                'name_en': 'Arabic Coffee',
                'description_ar': 'قهوة عربية أصيلة محضرة بالطريقة التقليدية',
                'description_en': 'Authentic Arabic coffee prepared traditionally',
                'price': 15.00,
                'category_name': 'المشروبات الساخنة',
                'is_featured': True
            },
            {
                'name_ar': 'شاي بالنعناع',
                'name_en': 'Mint Tea',
                'description_ar': 'شاي أحمر طازج مع أوراق النعناع الطبيعية',
                'description_en': 'Fresh black tea with natural mint leaves',
                'price': 12.00,
                'category_name': 'المشروبات الساخنة'
            },
            {
                'name_ar': 'عصير برتقال طازج',
                'name_en': 'Fresh Orange Juice',
                'description_ar': 'عصير برتقال طبيعي 100% بدون إضافات',
                'description_en': '100% natural orange juice with no additives',
                'price': 20.00,
                'category_name': 'المشروبات الباردة',
                'is_featured': True
            },
            {
                'name_ar': 'برجر لحم',
                'name_en': 'Beef Burger',
                'description_ar': 'برجر لحم بقري مشوي مع الخضار والصوص الخاص',
                'description_en': 'Grilled beef burger with vegetables and special sauce',
                'price': 45.00,
                'category_name': 'الوجبات الرئيسية',
                'is_featured': True
            },
            {
                'name_ar': 'كنافة بالجبن',
                'name_en': 'Cheese Kunafa',
                'description_ar': 'كنافة طازجة محشوة بالجبن الحلو والقطر',
                'description_en': 'Fresh kunafa stuffed with sweet cheese and syrup',
                'price': 25.00,
                'category_name': 'الحلويات'
            }
        ]
        
        for prod_data in sample_products:
            category = Category.query.filter_by(name_ar=prod_data['category_name']).first()
            if category:
                existing_prod = Product.query.filter_by(name_ar=prod_data['name_ar']).first()
                if not existing_prod:
                    product = Product(
                        category_id=category.id,
                        name_ar=prod_data['name_ar'],
                        name_en=prod_data['name_en'],
                        description_ar=prod_data['description_ar'],
                        description_en=prod_data['description_en'],
                        price=prod_data['price'],
                        is_featured=prod_data.get('is_featured', False)
                    )
                    db.session.add(product)
                    print(f"تم إنشاء منتج: {prod_data['name_ar']}")
        
        # حفظ التغييرات النهائية - Save final changes
        db.session.commit()
        
        print("تم الانتهاء من تهيئة بيانات المطعم بنجاح!")
        print(f"عدد الطاولات: {RestaurantTable.query.count()}")
        print(f"عدد الفئات: {Category.query.count()}")
        print(f"عدد المنتجات: {Product.query.count()}")

if __name__ == '__main__':
    init_restaurant_data()
