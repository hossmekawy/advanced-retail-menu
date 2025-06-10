#!/usr/bin/env python3
"""
إضافة حقول التواصل الاجتماعي إلى جدول الإعدادات
Add social media fields to settings table
"""

import sqlite3
import os

def migrate_database():
    """إضافة حقول التواصل الاجتماعي - Add social media fields"""
    db_path = 'instance/shop_menu.db'
    
    if not os.path.exists(db_path):
        print("Database file not found. Please run the application first to create the database.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # التحقق من وجود الحقول - Check if fields exist
        cursor.execute("PRAGMA table_info(settings)")
        columns = [column[1] for column in cursor.fetchall()]
        
        # إضافة الحقول الجديدة إذا لم تكن موجودة - Add new fields if they don't exist
        new_fields = [
            'facebook_url',
            'twitter_url', 
            'instagram_url',
            'whatsapp_url'
        ]
        
        for field in new_fields:
            if field not in columns:
                print(f"Adding field: {field}")
                cursor.execute(f"ALTER TABLE settings ADD COLUMN {field} VARCHAR(500)")
            else:
                print(f"Field {field} already exists")
        
        conn.commit()
        print("Migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == '__main__':
    migrate_database()
