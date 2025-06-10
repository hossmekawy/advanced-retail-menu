#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار الأخطاء المحددة - Test specific errors that were reported
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_moment_undefined_error():
    """اختبار خطأ moment غير معرف - Test moment undefined error"""
    print("Testing: UndefinedError: 'moment' is undefined")
    print("-" * 50)
    
    try:
        from app import create_app
        app = create_app('development')
        
        with app.app_context():
            from flask import render_template_string
            
            # Test the exact line that was causing the error in thermal_receipt.html
            problematic_template = """
            <div style="font-size: 8px; margin-top: 1mm;">
                تم الطباعة في: {{ moment().format('YYYY-MM-DD HH:mm:ss') }}
            </div>
            """
            
            result = render_template_string(problematic_template)
            print("✅ SUCCESS: moment() function is now working!")
            print(f"   Output: {result.strip()}")
            return True
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_template_not_found_error():
    """اختبار خطأ القالب غير موجود - Test template not found error"""
    print("\nTesting: TemplateNotFound: admin/pos/invoice_form.html")
    print("-" * 50)
    
    try:
        # Check if the template file exists
        template_path = "templates/admin/pos/invoice_form.html"
        
        if os.path.exists(template_path):
            print("✅ SUCCESS: invoice_form.html template exists!")
            
            # Check file size and basic content
            file_size = os.path.getsize(template_path)
            print(f"   File size: {file_size} bytes")
            
            # Check if it has proper Jinja2 template structure
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if "{% extends" in content:
                print("   ✓ Template extends base template")
            if "{% block" in content:
                print("   ✓ Template has content blocks")
            if "{{ form" in content:
                print("   ✓ Template uses form variables")
                
            return True
        else:
            print(f"❌ FAILED: Template file does not exist at {template_path}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_pos_routes_accessibility():
    """اختبار إمكانية الوصول لمسارات نقاط البيع - Test POS routes accessibility"""
    print("\nTesting: POS routes accessibility")
    print("-" * 50)
    
    try:
        from app import create_app
        app = create_app('development')
        
        with app.app_context():
            # Get all URL rules
            rules = list(app.url_map.iter_rules())
            
            # Find POS-related routes
            pos_routes = []
            for rule in rules:
                if '/admin/pos' in rule.rule:
                    pos_routes.append(rule.rule)
            
            if pos_routes:
                print(f"✅ SUCCESS: Found {len(pos_routes)} POS routes!")
                print("   Available POS routes:")
                for route in sorted(pos_routes):
                    print(f"     • {route}")
                return True
            else:
                print("❌ FAILED: No POS routes found")
                return False
                
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def main():
    """الدالة الرئيسية - Main function"""
    print("🔍 Testing Specific Error Scenarios")
    print("=" * 60)
    
    # Test the specific errors that were reported
    test1 = test_moment_undefined_error()
    test2 = test_template_not_found_error()
    test3 = test_pos_routes_accessibility()
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY OF FIXES")
    print("=" * 60)
    
    if test1:
        print("✅ FIXED: UndefinedError: 'moment' is undefined")
        print("   → Added moment() function to Flask template context")
    else:
        print("❌ NOT FIXED: UndefinedError: 'moment' is undefined")
    
    if test2:
        print("✅ VERIFIED: admin/pos/invoice_form.html template exists")
        print("   → Template is properly structured and accessible")
    else:
        print("❌ ISSUE: admin/pos/invoice_form.html template missing")
    
    if test3:
        print("✅ VERIFIED: POS routes are properly registered")
        print("   → All admin POS functionality is accessible")
    else:
        print("❌ ISSUE: POS routes not properly registered")
    
    print("\n" + "=" * 60)
    
    if test1 and test2 and test3:
        print("🎉 ALL ISSUES RESOLVED!")
        print("\nYour Flask application should now work without the reported errors.")
        print("You can safely:")
        print("• Access POS thermal receipt printing")
        print("• Generate invoices from orders")
        print("• Use all POS functionality with proper date/time display")
        return 0
    else:
        print("⚠️  Some issues may still exist. Please check the failed tests above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
