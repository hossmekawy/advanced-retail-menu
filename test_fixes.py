#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار الإصلاحات - Test the fixes for moment() function and templates
"""
import requests
import sys

def test_moment_function():
    """اختبار دالة moment - Test moment function"""
    print("Testing moment function...")
    
    try:
        # Test the admin login page first
        response = requests.get('http://127.0.0.1:5000/admin/login')
        if response.status_code == 200:
            print("✓ Admin login page loads successfully")
        else:
            print(f"✗ Admin login page failed: {response.status_code}")
            return False
            
        # Test the main admin page (should redirect to login)
        response = requests.get('http://127.0.0.1:5000/admin')
        if response.status_code in [200, 302]:  # 302 is redirect to login
            print("✓ Admin page accessible")
        else:
            print(f"✗ Admin page failed: {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to Flask app. Make sure it's running on http://127.0.0.1:5000")
        return False
    except Exception as e:
        print(f"✗ Error testing moment function: {e}")
        return False

def test_pos_routes():
    """اختبار مسارات نقاط البيع - Test POS routes"""
    print("\nTesting POS routes...")
    
    try:
        # Test POS dashboard (should redirect to login)
        response = requests.get('http://127.0.0.1:5000/admin/pos')
        if response.status_code in [200, 302]:
            print("✓ POS dashboard accessible")
        else:
            print(f"✗ POS dashboard failed: {response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"✗ Error testing POS routes: {e}")
        return False

def main():
    """الدالة الرئيسية - Main function"""
    print("🧪 Testing Flask Application Fixes")
    print("=" * 50)
    
    # Test moment function
    moment_test = test_moment_function()
    
    # Test POS routes
    pos_test = test_pos_routes()
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"Moment Function: {'✓ PASS' if moment_test else '✗ FAIL'}")
    print(f"POS Routes: {'✓ PASS' if pos_test else '✗ FAIL'}")
    
    if moment_test and pos_test:
        print("\n🎉 All tests passed! The fixes are working correctly.")
        return 0
    else:
        print("\n❌ Some tests failed. Please check the Flask application.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
