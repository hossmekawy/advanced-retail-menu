#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ترقية قاعدة البيانات لنظام نقاط البيع - Database Migration for POS System
"""
import sqlite3
import os
from datetime import datetime

def migrate_database():
    """ترقية قاعدة البيانات - Migrate database"""
    db_path = 'instance/shop_menu.db'
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False
    
    print("🔄 Starting POS system database migration...")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Add payment_status column to orders table
        print("📝 Adding payment_status column to orders table...")
        try:
            cursor.execute("ALTER TABLE orders ADD COLUMN payment_status VARCHAR(20) DEFAULT 'unpaid'")
            print("✅ Added payment_status column")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e):
                print("ℹ️ payment_status column already exists")
            else:
                raise e
        
        # 2. Create payments table
        print("📝 Creating payments table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS payments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                payment_number VARCHAR(20) UNIQUE NOT NULL,
                order_id INTEGER NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                payment_method VARCHAR(20) NOT NULL,
                payment_status VARCHAR(20) DEFAULT 'pending',
                processed_by_user_id INTEGER NOT NULL,
                payment_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                reference_number VARCHAR(100),
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (processed_by_user_id) REFERENCES users (id)
            )
        """)
        print("✅ Created payments table")
        
        # 3. Create invoices table
        print("📝 Creating invoices table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number VARCHAR(20) UNIQUE NOT NULL,
                order_id INTEGER NOT NULL,
                subtotal DECIMAL(10, 2) NOT NULL,
                tax_rate DECIMAL(5, 2) DEFAULT 0,
                tax_amount DECIMAL(10, 2) DEFAULT 0,
                total_amount DECIMAL(10, 2) NOT NULL,
                created_by_user_id INTEGER NOT NULL,
                invoice_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (created_by_user_id) REFERENCES users (id)
            )
        """)
        print("✅ Created invoices table")
        
        # 4. Create cash_drawers table
        print("📝 Creating cash_drawers table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cash_drawers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                current_balance DECIMAL(10, 2) DEFAULT 0,
                currency VARCHAR(3) DEFAULT 'EGP',
                last_updated_by_user_id INTEGER,
                last_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (last_updated_by_user_id) REFERENCES users (id)
            )
        """)
        print("✅ Created cash_drawers table")
        
        # 5. Create cash_transactions table
        print("📝 Creating cash_transactions table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cash_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cash_drawer_id INTEGER NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                transaction_type VARCHAR(20) NOT NULL,
                description VARCHAR(200) NOT NULL,
                reference_id INTEGER,
                reference_type VARCHAR(20),
                user_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (cash_drawer_id) REFERENCES cash_drawers (id),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        print("✅ Created cash_transactions table")
        
        # 6. Create shifts table
        print("📝 Creating shifts table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS shifts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                shift_number VARCHAR(20) UNIQUE NOT NULL,
                user_id INTEGER NOT NULL,
                cash_drawer_id INTEGER NOT NULL,
                start_time DATETIME DEFAULT CURRENT_TIMESTAMP,
                end_time DATETIME,
                opening_balance DECIMAL(10, 2) NOT NULL,
                closing_balance DECIMAL(10, 2),
                expected_balance DECIMAL(10, 2),
                variance DECIMAL(10, 2),
                total_sales DECIMAL(10, 2) DEFAULT 0,
                cash_sales DECIMAL(10, 2) DEFAULT 0,
                card_sales DECIMAL(10, 2) DEFAULT 0,
                other_sales DECIMAL(10, 2) DEFAULT 0,
                total_orders INTEGER DEFAULT 0,
                total_payments INTEGER DEFAULT 0,
                status VARCHAR(20) DEFAULT 'active',
                notes TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (cash_drawer_id) REFERENCES cash_drawers (id)
            )
        """)
        print("✅ Created shifts table")
        
        # 7. Create default cash drawer if none exists
        print("📝 Creating default cash drawer...")
        cursor.execute("SELECT COUNT(*) FROM cash_drawers")
        if cursor.fetchone()[0] == 0:
            cursor.execute("""
                INSERT INTO cash_drawers (current_balance, currency, created_at)
                VALUES (0, 'EGP', ?)
            """, (datetime.now(),))
            print("✅ Created default cash drawer")
        else:
            print("ℹ️ Cash drawer already exists")
        
        # 8. Update existing orders to have payment_status = 'unpaid'
        print("📝 Updating existing orders payment status...")
        cursor.execute("UPDATE orders SET payment_status = 'unpaid' WHERE payment_status IS NULL")
        updated_orders = cursor.rowcount
        print(f"✅ Updated {updated_orders} orders with payment status")
        
        # Commit all changes
        conn.commit()
        print("✅ All changes committed successfully")
        
        # Show summary
        print("\n📊 Migration Summary:")
        cursor.execute("SELECT COUNT(*) FROM orders")
        orders_count = cursor.fetchone()[0]
        print(f"   📋 Orders: {orders_count}")
        
        cursor.execute("SELECT COUNT(*) FROM payments")
        payments_count = cursor.fetchone()[0]
        print(f"   💳 Payments: {payments_count}")
        
        cursor.execute("SELECT COUNT(*) FROM invoices")
        invoices_count = cursor.fetchone()[0]
        print(f"   🧾 Invoices: {invoices_count}")
        
        cursor.execute("SELECT COUNT(*) FROM cash_drawers")
        drawers_count = cursor.fetchone()[0]
        print(f"   💰 Cash Drawers: {drawers_count}")
        
        cursor.execute("SELECT COUNT(*) FROM cash_transactions")
        transactions_count = cursor.fetchone()[0]
        print(f"   🔄 Cash Transactions: {transactions_count}")
        
        cursor.execute("SELECT COUNT(*) FROM shifts")
        shifts_count = cursor.fetchone()[0]
        print(f"   ⏰ Shifts: {shifts_count}")
        
        conn.close()
        print("\n🎉 POS system migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        return False

if __name__ == "__main__":
    success = migrate_database()
    if success:
        print("\n✅ You can now start the application with: python run.py")
    else:
        print("\n❌ Migration failed. Please check the errors above.")
