#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
إضافة أعمدة الإعدادات الجديدة - Add new settings columns
"""
import sqlite3
import os

def add_columns():
    """إضافة الأعمدة الجديدة - Add new columns"""
    db_path = "instance/shop_menu.db"
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Add columns one by one
        columns_to_add = [
            ("phone", "VARCHAR(20)"),
            ("email", "VARCHAR(120)"),
            ("address", "TEXT"),
            ("tax_number", "VARCHAR(50)")
        ]
        
        for column_name, column_type in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE settings ADD COLUMN {column_name} {column_type}")
                print(f"✅ Added {column_name} column")
            except sqlite3.OperationalError as e:
                if "duplicate column name" in str(e):
                    print(f"⚠️ Column {column_name} already exists")
                else:
                    print(f"❌ Error adding {column_name}: {e}")
        
        conn.commit()
        conn.close()
        print("🎉 Migration completed!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    add_columns()
