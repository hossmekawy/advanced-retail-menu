#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار شامل للإصلاحات - Comprehensive test for all fixes
"""
import sys
import os
import traceback

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_creation():
    """اختبار إنشاء التطبيق - Test app creation"""
    print("1. Testing Flask app creation...")
    try:
        from app import create_app
        app = create_app('development')
        print("   ✓ Flask app created successfully")
        return app
    except Exception as e:
        print(f"   ✗ Failed to create Flask app: {e}")
        traceback.print_exc()
        return None

def test_moment_function_in_context(app):
    """اختبار دالة moment في سياق التطبيق - Test moment function in app context"""
    print("2. Testing moment function in app context...")
    try:
        with app.app_context():
            from flask import render_template_string
            
            # Test all the moment formats used in templates
            test_cases = [
                ("YYYY-MM-DD HH:mm:ss", "Full datetime format"),
                ("YYYY-MM-DD", "Date only format"),
                ("HH:mm:ss", "Time only format")
            ]
            
            for format_str, description in test_cases:
                template = f"{{{{ moment().format('{format_str}') }}}}"
                result = render_template_string(template)
                print(f"   ✓ {description}: {result}")
            
            return True
    except Exception as e:
        print(f"   ✗ Moment function test failed: {e}")
        traceback.print_exc()
        return False

def test_thermal_receipt_template(app):
    """اختبار قالب الإيصال الحراري - Test thermal receipt template"""
    print("3. Testing thermal receipt template...")
    try:
        with app.app_context():
            from flask import render_template_string
            
            # Test the exact problematic line from thermal_receipt.html
            template = """
            <div style="font-size: 8px; margin-top: 1mm;">
                تم الطباعة في: {{ moment().format('YYYY-MM-DD HH:mm:ss') }}
            </div>
            """
            
            result = render_template_string(template)
            print("   ✓ Thermal receipt template rendered successfully")
            print(f"   Result: {result.strip()}")
            return True
    except Exception as e:
        print(f"   ✗ Thermal receipt template failed: {e}")
        return False

def test_invoice_form_template(app):
    """اختبار قالب نموذج الفاتورة - Test invoice form template"""
    print("4. Testing invoice form template existence...")
    try:
        template_path = "templates/admin/pos/invoice_form.html"
        if os.path.exists(template_path):
            print("   ✓ Invoice form template exists")
            
            # Check if template can be imported (basic syntax check)
            with app.app_context():
                # We can't fully render this template without proper context,
                # but we can check if it exists and has basic structure
                with open(template_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if "{% extends" in content and "{% block" in content:
                        print("   ✓ Invoice form template has proper structure")
                        return True
                    else:
                        print("   ✗ Invoice form template missing proper structure")
                        return False
        else:
            print("   ✗ Invoice form template does not exist")
            return False
    except Exception as e:
        print(f"   ✗ Invoice form template test failed: {e}")
        return False

def test_all_moment_templates(app):
    """اختبار جميع القوالب التي تستخدم moment - Test all templates using moment"""
    print("5. Testing all templates with moment function...")
    try:
        with app.app_context():
            from flask import render_template_string
            
            # Test templates that use moment function
            templates_to_test = [
                ("Shift Report", "تم إنشاء هذا التقرير في: {{ moment().format('YYYY-MM-DD HH:mm:ss') }}"),
                ("Start Shift Date", "التاريخ: {{ moment().format('YYYY-MM-DD') }}"),
                ("Start Shift Time", "الوقت: {{ moment().format('HH:mm:ss') }}"),
            ]
            
            for template_name, template_content in templates_to_test:
                try:
                    result = render_template_string(template_content)
                    print(f"   ✓ {template_name}: {result.strip()}")
                except Exception as e:
                    print(f"   ✗ {template_name} failed: {e}")
                    return False
            
            return True
    except Exception as e:
        print(f"   ✗ Template testing failed: {e}")
        return False

def test_admin_routes_structure(app):
    """اختبار هيكل مسارات الإدارة - Test admin routes structure"""
    print("6. Testing admin routes structure...")
    try:
        with app.app_context():
            # Check if admin blueprint is registered
            blueprints = app.blueprints
            if 'admin' in blueprints:
                print("   ✓ Admin blueprint is registered")
                
                # Check if POS routes are available
                rules = [rule.rule for rule in app.url_map.iter_rules()]
                pos_routes = [rule for rule in rules if '/admin/pos' in rule]
                
                if pos_routes:
                    print(f"   ✓ Found {len(pos_routes)} POS routes")
                    return True
                else:
                    print("   ✗ No POS routes found")
                    return False
            else:
                print("   ✗ Admin blueprint not registered")
                return False
    except Exception as e:
        print(f"   ✗ Admin routes test failed: {e}")
        return False

def main():
    """الدالة الرئيسية - Main function"""
    print("🧪 Comprehensive Test for Flask Application Fixes")
    print("=" * 60)
    
    # Test results
    results = []
    
    # 1. Test app creation
    app = test_app_creation()
    results.append(("App Creation", app is not None))
    
    if app:
        # 2. Test moment function
        moment_result = test_moment_function_in_context(app)
        results.append(("Moment Function", moment_result))
        
        # 3. Test thermal receipt template
        thermal_result = test_thermal_receipt_template(app)
        results.append(("Thermal Receipt", thermal_result))
        
        # 4. Test invoice form template
        invoice_result = test_invoice_form_template(app)
        results.append(("Invoice Form", invoice_result))
        
        # 5. Test all moment templates
        all_templates_result = test_all_moment_templates(app)
        results.append(("All Moment Templates", all_templates_result))
        
        # 6. Test admin routes
        admin_routes_result = test_admin_routes_structure(app)
        results.append(("Admin Routes", admin_routes_result))
    else:
        # If app creation failed, mark all other tests as failed
        for test_name in ["Moment Function", "Thermal Receipt", "Invoice Form", "All Moment Templates", "Admin Routes"]:
            results.append((test_name, False))
    
    # Print results
    print("\n" + "=" * 60)
    print("📊 Final Test Results:")
    print("-" * 60)
    
    all_passed = True
    for test_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{test_name:<20}: {status}")
        if not passed:
            all_passed = False
    
    print("-" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! The fixes are working correctly.")
        print("\nThe following issues have been resolved:")
        print("• UndefinedError: 'moment' is undefined")
        print("• TemplateNotFound: admin/pos/invoice_form.html")
        return 0
    else:
        print("❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
