#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار نظام الطلبات - Test Order System
"""
from app import create_app
from extensions import db
from models import Product, RestaurantTable, Order, OrderItem

def test_order_system():
    """اختبار نظام الطلبات - Test order system"""
    app = create_app()
    
    with app.app_context():
        print("🧪 اختبار نظام الطلبات...")
        
        # التحقق من وجود المنتجات - Check products exist
        products = Product.query.filter_by(is_active=True).all()
        print(f"📦 عدد المنتجات المتاحة: {len(products)}")
        
        for product in products[:5]:  # عرض أول 5 منتجات
            print(f"   - {product.name_ar}: {product.price} {product.currency or 'EGP'}")
        
        # التحقق من وجود الطاولات - Check tables exist
        tables = RestaurantTable.query.filter_by(is_active=True).all()
        print(f"🪑 عدد الطاولات المتاحة: {len(tables)}")
        
        available_tables = RestaurantTable.query.filter_by(is_active=True, status='available').all()
        print(f"✅ عدد الطاولات المتاحة للحجز: {len(available_tables)}")
        
        for table in available_tables[:3]:  # عرض أول 3 طاولات
            print(f"   - طاولة {table.table_number}: {table.capacity} أشخاص")
        
        # التحقق من الطلبات الموجودة - Check existing orders
        orders = Order.query.all()
        print(f"📋 عدد الطلبات الموجودة: {len(orders)}")
        
        active_orders = Order.query.filter(Order.status.in_(['pending', 'preparing', 'ready'])).all()
        print(f"🔄 عدد الطلبات النشطة: {len(active_orders)}")
        
        if active_orders:
            print("الطلبات النشطة:")
            for order in active_orders:
                print(f"   - {order.order_number}: {order.customer_name} - طاولة {order.table.table_number} - {order.get_status_text('ar')}")
        
        # إنشاء طلب تجريبي إذا لم توجد طلبات - Create test order if no orders exist
        if not orders and products and available_tables:
            print("\n🆕 إنشاء طلب تجريبي...")
            
            # اختيار منتج وطاولة - Select product and table
            test_product = products[0]
            test_table = available_tables[0]
            
            # إنشاء الطلب - Create order
            test_order = Order(
                customer_name="أحمد محمد",
                customer_phone="01234567890",
                table_id=test_table.id,
                total_amount=test_product.price * 2,  # كمية 2
                notes="طلب تجريبي للاختبار"
            )
            test_order.order_number = test_order.generate_order_number()
            
            db.session.add(test_order)
            db.session.flush()
            
            # إضافة عنصر الطلب - Add order item
            test_order_item = OrderItem(
                order_id=test_order.id,
                product_id=test_product.id,
                quantity=2,
                unit_price=test_product.price,
                total_price=test_product.price * 2
            )
            
            db.session.add(test_order_item)
            
            # تحديث حالة الطاولة - Update table status
            test_table.status = 'order_placed'
            
            db.session.commit()
            
            print(f"✅ تم إنشاء طلب تجريبي: {test_order.order_number}")
            print(f"   العميل: {test_order.customer_name}")
            print(f"   الطاولة: {test_table.table_number}")
            print(f"   المنتج: {test_product.name_ar} × {test_order_item.quantity}")
            print(f"   المجموع: {test_order.get_formatted_total()}")
        
        print("\n📊 ملخص النظام:")
        print(f"   📦 المنتجات: {len(products)}")
        print(f"   🪑 الطاولات: {len(tables)}")
        print(f"   ✅ طاولات متاحة: {len(available_tables)}")
        print(f"   📋 إجمالي الطلبات: {len(orders)}")
        print(f"   🔄 طلبات نشطة: {len(active_orders)}")
        
        print("\n🎉 انتهى الاختبار بنجاح!")

if __name__ == '__main__':
    test_order_system()
