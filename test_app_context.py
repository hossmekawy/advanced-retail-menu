#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار سياق التطبيق - Test application context
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_app_context():
    """اختبار سياق التطبيق - Test application context"""
    try:
        from app import create_app
        
        print("Creating Flask app...")
        app = create_app('development')
        
        print("Testing app context...")
        with app.app_context():
            # Test if we can render a template with moment function
            from flask import render_template_string
            
            # Simple template test
            template = "Current time: {{ moment().format('YYYY-MM-DD HH:mm:ss') }}"
            
            try:
                result = render_template_string(template)
                print(f"✓ Template rendered successfully: {result}")
                return True
            except Exception as e:
                print(f"✗ Template rendering failed: {e}")
                return False
                
    except Exception as e:
        print(f"✗ Error creating app or context: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_template_files():
    """اختبار ملفات القوالب - Test template files"""
    try:
        from app import create_app
        
        app = create_app('development')
        
        with app.app_context():
            from flask import render_template
            
            # Test if admin login template can be rendered
            try:
                result = render_template('admin/login.html')
                print("✓ Admin login template rendered successfully")
                return True
            except Exception as e:
                print(f"✗ Admin login template failed: {e}")
                return False
                
    except Exception as e:
        print(f"✗ Error testing templates: {e}")
        return False

def main():
    """الدالة الرئيسية - Main function"""
    print("🧪 Testing Flask Application Context")
    print("=" * 50)
    
    # Test app context
    context_test = test_app_context()
    
    # Test template files
    template_test = test_template_files()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"App Context: {'✓ PASS' if context_test else '✗ FAIL'}")
    print(f"Template Files: {'✓ PASS' if template_test else '✗ FAIL'}")
    
    if context_test and template_test:
        print("\n🎉 All tests passed! The moment function is working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the implementation.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
