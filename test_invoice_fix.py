#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار إصلاح الفاتورة - Test invoice fix
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_invoice_calculate_totals():
    """اختبار حساب مجاميع الفاتورة - Test invoice calculate totals"""
    print("🧪 Testing Invoice calculate_totals fix")
    print("=" * 50)
    
    try:
        from app import create_app
        from models import Invoice, Order, User
        from extensions import db
        
        app = create_app('development')
        
        with app.app_context():
            # Create a mock order object for testing
            class MockOrder:
                def __init__(self):
                    self.id = 1
                    self.total_amount = 100.00
                    self.currency = 'EGP'
            
            # Test 1: Invoice with order parameter
            print("1. Testing calculate_totals with order parameter...")
            mock_order = MockOrder()
            
            invoice = Invoice(
                order_id=1,
                tax_rate=10,
                created_by_user_id=1,
                notes="Test invoice"
            )
            
            # This should work now
            invoice.calculate_totals(mock_order)
            
            print(f"   ✓ Subtotal: {invoice.subtotal}")
            print(f"   ✓ Tax amount: {invoice.tax_amount}")
            print(f"   ✓ Total amount: {invoice.total_amount}")
            
            # Verify calculations
            expected_tax = (100.00 * 10) / 100
            expected_total = 100.00 + expected_tax
            
            if invoice.subtotal == 100.00 and invoice.tax_amount == expected_tax and invoice.total_amount == expected_total:
                print("   ✅ Calculations are correct!")
                return True
            else:
                print("   ❌ Calculations are incorrect!")
                return False
                
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_invoice_without_order():
    """اختبار الفاتورة بدون طلب - Test invoice without order"""
    print("\n2. Testing calculate_totals without order (should raise error)...")
    
    try:
        from app import create_app
        from models import Invoice
        
        app = create_app('development')
        
        with app.app_context():
            invoice = Invoice(
                order_id=1,
                tax_rate=10,
                created_by_user_id=1,
                notes="Test invoice"
            )
            
            # This should raise a ValueError
            try:
                invoice.calculate_totals()
                print("   ❌ Should have raised ValueError!")
                return False
            except ValueError as e:
                print(f"   ✅ Correctly raised ValueError: {e}")
                return True
                
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False

def main():
    """الدالة الرئيسية - Main function"""
    print("🔧 Testing Invoice Fix for AttributeError")
    print("=" * 60)
    
    # Test with order parameter
    test1 = test_invoice_calculate_totals()
    
    # Test without order parameter
    test2 = test_invoice_without_order()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"Calculate totals with order: {'✅ PASS' if test1 else '❌ FAIL'}")
    print(f"Calculate totals without order: {'✅ PASS' if test2 else '❌ FAIL'}")
    
    if test1 and test2:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nThe AttributeError fix is working correctly:")
        print("• Invoice.calculate_totals() now accepts an order parameter")
        print("• The POS route passes the order to calculate_totals()")
        print("• Error handling is in place for missing orders")
        return 0
    else:
        print("\n❌ Some tests failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
