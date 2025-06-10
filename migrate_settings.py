#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ترحيل قاعدة البيانات لإضافة حقول الإعدادات الجديدة - Database migration for new settings fields
"""
import sqlite3
import os

def migrate_settings_table():
    """ترحيل جدول الإعدادات - Migrate settings table"""
    print("🔄 Migrating Settings Table...")

    db_path = "instance/shop_menu.db"
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if new columns already exist
        cursor.execute("PRAGMA table_info(settings)")
        columns = [column[1] for column in cursor.fetchall()]
        
        new_columns = ['phone', 'email', 'address', 'tax_number']
        columns_to_add = []
        
        for col in new_columns:
            if col not in columns:
                columns_to_add.append(col)
        
        if not columns_to_add:
            print("✅ All columns already exist!")
            conn.close()
            return True
        
        print(f"📝 Adding columns: {', '.join(columns_to_add)}")
        
        # Add new columns
        for column in columns_to_add:
            if column == 'phone':
                cursor.execute("ALTER TABLE settings ADD COLUMN phone VARCHAR(20)")
                print("   ✅ Added phone column")
            elif column == 'email':
                cursor.execute("ALTER TABLE settings ADD COLUMN email VARCHAR(120)")
                print("   ✅ Added email column")
            elif column == 'address':
                cursor.execute("ALTER TABLE settings ADD COLUMN address TEXT")
                print("   ✅ Added address column")
            elif column == 'tax_number':
                cursor.execute("ALTER TABLE settings ADD COLUMN tax_number VARCHAR(50)")
                print("   ✅ Added tax_number column")
        
        conn.commit()
        conn.close()
        
        print("🎉 Settings table migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        if 'conn' in locals():
            conn.close()
        return False

def verify_migration():
    """التحقق من نجاح الترحيل - Verify migration success"""
    print("\n🔍 Verifying Migration...")

    db_path = "instance/shop_menu.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check table structure
        cursor.execute("PRAGMA table_info(settings)")
        columns = cursor.fetchall()
        
        expected_columns = ['phone', 'email', 'address', 'tax_number']
        found_columns = [col[1] for col in columns]
        
        all_found = True
        for col in expected_columns:
            if col in found_columns:
                print(f"   ✅ Column '{col}' exists")
            else:
                print(f"   ❌ Column '{col}' missing")
                all_found = False
        
        conn.close()
        
        if all_found:
            print("✅ Migration verification successful!")
            return True
        else:
            print("❌ Migration verification failed!")
            return False
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def test_flask_app():
    """اختبار تشغيل تطبيق Flask - Test Flask app startup"""
    print("\n🧪 Testing Flask App Startup...")
    
    try:
        import sys
        import os
        
        # Add current directory to path
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from app import create_app
        
        app = create_app('development')
        
        with app.app_context():
            from models import Settings
            
            # Try to get settings
            settings = Settings.get_settings()
            print(f"   ✅ Settings loaded: {settings.shop_name}")
            
            # Test new fields
            print(f"   📞 Phone: {settings.phone or 'Not set'}")
            print(f"   📧 Email: {settings.email or 'Not set'}")
            print(f"   📍 Address: {settings.address or 'Not set'}")
            print(f"   🏛️ Tax Number: {settings.tax_number or 'Not set'}")
            
            print("✅ Flask app startup test successful!")
            return True
            
    except Exception as e:
        print(f"❌ Flask app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية - Main function"""
    print("🗄️ Database Migration for Professional Receipt Design")
    print("=" * 60)
    
    # Step 1: Migrate database
    migration_success = migrate_settings_table()
    
    # Step 2: Verify migration
    verification_success = verify_migration() if migration_success else False
    
    # Step 3: Test Flask app
    app_test_success = test_flask_app() if verification_success else False
    
    print("\n" + "=" * 60)
    print("📊 Migration Results:")
    print(f"Database Migration: {'✅ SUCCESS' if migration_success else '❌ FAILED'}")
    print(f"Verification: {'✅ SUCCESS' if verification_success else '❌ FAILED'}")
    print(f"Flask App Test: {'✅ SUCCESS' if app_test_success else '❌ FAILED'}")
    
    if migration_success and verification_success and app_test_success:
        print("\n🎉 MIGRATION COMPLETED SUCCESSFULLY!")
        print("\nYou can now:")
        print("• Start the Flask application")
        print("• Access admin settings to add contact information")
        print("• Generate professional receipts with company logo")
        print("• Use the new A4 receipt format")
        return 0
    else:
        print("\n❌ Migration failed. Please check the errors above.")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())
