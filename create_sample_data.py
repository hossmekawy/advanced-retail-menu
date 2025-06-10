#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
إنشاء بيانات تجريبية - Create Sample Data
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    from extensions import db
    from models import User, Settings, Category, SubCategory, Product
    
    def create_sample_data():
        """إنشاء بيانات تجريبية - Create sample data"""
        app = create_app('development')
        
        with app.app_context():
            print("🔄 Creating database tables...")
            db.create_all()
            
            # Check if admin user exists
            if not User.query.first():
                print("👤 Creating admin user...")
                admin = User(username='admin', email='admin@example.com')
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin user created (username: admin, password: admin123)")
            
            # Create settings
            print("⚙️ Creating default settings...")
            settings = Settings.get_settings()
            
            # Check if categories exist
            if Category.query.count() == 0:
                print("📂 Creating sample categories...")
                
                # Create categories
                categories_data = [
                    {
                        'name_ar': 'مشروبات ساخنة',
                        'name_en': 'Hot Beverages',
                        'description_ar': 'مشروبات ساخنة متنوعة',
                        'description_en': 'Various hot beverages',
                        'icon': 'fas fa-coffee',
                        'sort_order': 1
                    },
                    {
                        'name_ar': 'مشروبات باردة',
                        'name_en': 'Cold Beverages',
                        'description_ar': 'مشروبات باردة منعشة',
                        'description_en': 'Refreshing cold beverages',
                        'icon': 'fas fa-glass-whiskey',
                        'sort_order': 2
                    },
                    {
                        'name_ar': 'وجبات خفيفة',
                        'name_en': 'Snacks',
                        'description_ar': 'وجبات خفيفة لذيذة',
                        'description_en': 'Delicious snacks',
                        'icon': 'fas fa-cookie-bite',
                        'sort_order': 3
                    }
                ]
                
                created_categories = []
                for cat_data in categories_data:
                    category = Category(**cat_data, is_active=True)
                    db.session.add(category)
                    created_categories.append(category)
                
                db.session.commit()
                print(f"✅ Created {len(created_categories)} categories")
                
                # Create subcategories
                print("📁 Creating sample subcategories...")
                subcategories_data = [
                    {
                        'category': created_categories[0],  # Hot Beverages
                        'name_ar': 'قهوة',
                        'name_en': 'Coffee',
                        'description_ar': 'أنواع القهوة المختلفة',
                        'description_en': 'Different types of coffee',
                        'sort_order': 1
                    },
                    {
                        'category': created_categories[0],  # Hot Beverages
                        'name_ar': 'شاي',
                        'name_en': 'Tea',
                        'description_ar': 'أنواع الشاي المختلفة',
                        'description_en': 'Different types of tea',
                        'sort_order': 2
                    },
                    {
                        'category': created_categories[1],  # Cold Beverages
                        'name_ar': 'عصائر طبيعية',
                        'name_en': 'Fresh Juices',
                        'description_ar': 'عصائر طبيعية طازجة',
                        'description_en': 'Fresh natural juices',
                        'sort_order': 1
                    }
                ]
                
                created_subcategories = []
                for subcat_data in subcategories_data:
                    category = subcat_data.pop('category')
                    subcategory = SubCategory(
                        category_id=category.id,
                        **subcat_data,
                        is_active=True
                    )
                    db.session.add(subcategory)
                    created_subcategories.append(subcategory)
                
                db.session.commit()
                print(f"✅ Created {len(created_subcategories)} subcategories")
                
                # Create sample products
                print("🛍️ Creating sample products...")
                products_data = [
                    {
                        'category_id': created_categories[0].id,  # Hot Beverages
                        'subcategory_id': created_subcategories[0].id,  # Coffee
                        'name_ar': 'قهوة عربية',
                        'name_en': 'Arabic Coffee',
                        'description_ar': 'قهوة عربية أصيلة ومميزة بطعم رائع',
                        'description_en': 'Authentic Arabic coffee with amazing taste',
                        'ingredients_ar': 'حبوب قهوة عربية، هيل، زعفران',
                        'ingredients_en': 'Arabic coffee beans, cardamom, saffron',
                        'price': 25.50,
                        'currency': 'EGP',
                        'sort_order': 1,
                        'is_active': True,
                        'is_featured': True
                    },
                    {
                        'category_id': created_categories[0].id,  # Hot Beverages
                        'subcategory_id': created_subcategories[0].id,  # Coffee
                        'name_ar': 'كابتشينو',
                        'name_en': 'Cappuccino',
                        'description_ar': 'كابتشينو كريمي بالحليب المرغي',
                        'description_en': 'Creamy cappuccino with foamed milk',
                        'ingredients_ar': 'إسبريسو، حليب، رغوة حليب',
                        'ingredients_en': 'Espresso, milk, milk foam',
                        'price': 30.00,
                        'currency': 'EGP',
                        'sort_order': 2,
                        'is_active': True,
                        'is_featured': False
                    },
                    {
                        'category_id': created_categories[0].id,  # Hot Beverages
                        'subcategory_id': created_subcategories[1].id,  # Tea
                        'name_ar': 'شاي أحمر',
                        'name_en': 'Black Tea',
                        'description_ar': 'شاي أحمر تقليدي بنكهة قوية',
                        'description_en': 'Traditional black tea with strong flavor',
                        'ingredients_ar': 'أوراق شاي أحمر، سكر',
                        'ingredients_en': 'Black tea leaves, sugar',
                        'price': 15.00,
                        'currency': 'EGP',
                        'sort_order': 1,
                        'is_active': True,
                        'is_featured': False
                    },
                    {
                        'category_id': created_categories[1].id,  # Cold Beverages
                        'subcategory_id': created_subcategories[2].id,  # Fresh Juices
                        'name_ar': 'عصير برتقال طازج',
                        'name_en': 'Fresh Orange Juice',
                        'description_ar': 'عصير برتقال طبيعي 100% بدون إضافات',
                        'description_en': '100% natural orange juice with no additives',
                        'ingredients_ar': 'برتقال طازج',
                        'ingredients_en': 'Fresh oranges',
                        'price': 20.00,
                        'currency': 'EGP',
                        'sort_order': 1,
                        'is_active': True,
                        'is_featured': True
                    },
                    {
                        'category_id': created_categories[2].id,  # Snacks
                        'subcategory_id': None,
                        'name_ar': 'كرواسون بالجبن',
                        'name_en': 'Cheese Croissant',
                        'description_ar': 'كرواسون طازج محشو بالجبن الكريمي',
                        'description_en': 'Fresh croissant filled with creamy cheese',
                        'ingredients_ar': 'دقيق، زبدة، جبن كريمي، بيض',
                        'ingredients_en': 'Flour, butter, cream cheese, eggs',
                        'price': 35.00,
                        'currency': 'EGP',
                        'sort_order': 1,
                        'is_active': True,
                        'is_featured': False
                    }
                ]
                
                for product_data in products_data:
                    product = Product(**product_data)
                    db.session.add(product)
                
                db.session.commit()
                print(f"✅ Created {len(products_data)} products")
            
            # Show final statistics
            print("\n📊 Database Statistics:")
            print(f"   👥 Users: {User.query.count()}")
            print(f"   📂 Categories: {Category.query.count()}")
            print(f"   📁 Subcategories: {SubCategory.query.count()}")
            print(f"   🛍️ Products: {Product.query.count()}")
            
            print("\n🎉 Sample data created successfully!")
            print("🔗 You can now run the application with: python app.py")
            print("🔑 Admin login: username=admin, password=admin123")
    
    if __name__ == '__main__':
        create_sample_data()
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
