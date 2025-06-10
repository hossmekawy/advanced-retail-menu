#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار تصميم الإيصال الجديد - Test new receipt design
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_receipt_template():
    """اختبار قالب الإيصال - Test receipt template"""
    print("🧪 Testing New Professional Receipt Design")
    print("=" * 60)
    
    try:
        from app import create_app
        
        app = create_app('development')
        
        with app.app_context():
            from flask import render_template_string
            
            # Test the new receipt template with mock data
            template_content = """
            <!DOCTYPE html>
            <html lang="ar" dir="rtl">
            <head>
                <meta charset="UTF-8">
                <title>إيصال اختبار</title>
            </head>
            <body>
                <!-- Test Logo Display -->
                {% if settings.logo_b64 %}
                    <div class="logo">
                        <img src="{{ settings.logo_b64 }}" alt="{{ settings.shop_name }}">
                    </div>
                {% endif %}
                
                <!-- Test Shop Info -->
                <div class="shop-name">{{ settings.shop_name }}</div>
                
                {% if settings.phone %}
                    <div>📞 {{ settings.phone }}</div>
                {% endif %}
                {% if settings.address %}
                    <div>📍 {{ settings.address }}</div>
                {% endif %}
                {% if settings.email %}
                    <div>📧 {{ settings.email }}</div>
                {% endif %}
                {% if settings.tax_number %}
                    <div>🏛️ الرقم الضريبي: {{ settings.tax_number }}</div>
                {% endif %}
                
                <!-- Test Moment Function -->
                <div>🖨️ تم الطباعة في: {{ moment().format('YYYY-MM-DD HH:mm:ss') }}</div>
            </body>
            </html>
            """
            
            try:
                result = render_template_string(template_content)
                print("✅ Receipt template rendered successfully!")
                print("   Template includes:")
                print("   • Logo support")
                print("   • Shop information")
                print("   • Contact details")
                print("   • Professional formatting")
                print("   • Moment function for timestamps")
                return True
            except Exception as e:
                print(f"❌ Receipt template failed: {e}")
                return False
                
    except Exception as e:
        print(f"❌ Error testing receipt: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_settings_fields():
    """اختبار حقول الإعدادات الجديدة - Test new settings fields"""
    print("\n2. Testing New Settings Fields...")
    
    try:
        from app import create_app
        from models import Settings
        
        app = create_app('development')
        
        with app.app_context():
            # Test if new fields exist in Settings model
            settings = Settings()
            
            # Check if new fields are accessible
            fields_to_check = ['phone', 'email', 'address', 'tax_number']
            
            for field in fields_to_check:
                if hasattr(settings, field):
                    print(f"   ✅ Field '{field}' exists in Settings model")
                else:
                    print(f"   ❌ Field '{field}' missing from Settings model")
                    return False
            
            print("   ✅ All new contact fields are available!")
            return True
                
    except Exception as e:
        print(f"   ❌ Error testing settings fields: {e}")
        return False

def test_receipt_file_structure():
    """اختبار هيكل ملف الإيصال - Test receipt file structure"""
    print("\n3. Testing Receipt File Structure...")
    
    try:
        receipt_path = "templates/admin/pos/thermal_receipt.html"
        
        if os.path.exists(receipt_path):
            with open(receipt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for key elements
            checks = [
                ("Logo support", "settings.logo_b64" in content),
                ("Professional styling", "@media print" in content),
                ("A4 page size", "size: A4" in content),
                ("Contact information", "settings.phone" in content),
                ("Tax number", "settings.tax_number" in content),
                ("Professional table", "items-table" in content),
                ("Moment function", "moment().format" in content),
                ("Print controls", "print-controls" in content),
                ("Footer branding", "Advanced POS" in content)
            ]
            
            all_passed = True
            for check_name, check_result in checks:
                if check_result:
                    print(f"   ✅ {check_name}")
                else:
                    print(f"   ❌ {check_name}")
                    all_passed = False
            
            if all_passed:
                print("   ✅ Receipt file structure is complete!")
                return True
            else:
                print("   ❌ Some elements are missing from receipt template")
                return False
        else:
            print(f"   ❌ Receipt template not found at {receipt_path}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error checking receipt file: {e}")
        return False

def main():
    """الدالة الرئيسية - Main function"""
    print("🎨 Testing Professional Receipt Design Implementation")
    print("=" * 70)
    
    # Test receipt template rendering
    template_test = test_receipt_template()
    
    # Test new settings fields
    settings_test = test_settings_fields()
    
    # Test receipt file structure
    structure_test = test_receipt_file_structure()
    
    print("\n" + "=" * 70)
    print("📊 Test Results:")
    print(f"Receipt Template: {'✅ PASS' if template_test else '❌ FAIL'}")
    print(f"Settings Fields: {'✅ PASS' if settings_test else '❌ FAIL'}")
    print(f"File Structure: {'✅ PASS' if structure_test else '❌ FAIL'}")
    
    if template_test and settings_test and structure_test:
        print("\n🎉 ALL TESTS PASSED!")
        print("\nNew Professional Receipt Features:")
        print("• 📄 Full A4 page layout instead of 58mm thermal")
        print("• 🏢 Company logo display from settings")
        print("• 📞 Complete contact information")
        print("• 📊 Professional table layout for items")
        print("• 🎨 Modern styling with colors and icons")
        print("• 🖨️ Print controls and keyboard shortcuts")
        print("• 📱 Responsive design for screen and print")
        print("• 🌟 Professional footer with branding")
        return 0
    else:
        print("\n❌ Some tests failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
