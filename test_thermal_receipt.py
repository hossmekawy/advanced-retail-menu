#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار قالب الإيصال الحراري - Test thermal receipt template
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_thermal_receipt_template():
    """اختبار قالب الإيصال الحراري - Test thermal receipt template"""
    try:
        from app import create_app
        
        print("Creating Flask app...")
        app = create_app('development')
        
        print("Testing thermal receipt template...")
        with app.app_context():
            from flask import render_template_string
            
            # Test the exact line that was causing the error
            template = """
            <div style="font-size: 8px; margin-top: 1mm;">
                تم الطباعة في: {{ moment().format('YYYY-MM-DD HH:mm:ss') }}
            </div>
            """
            
            try:
                result = render_template_string(template)
                print(f"✓ Thermal receipt template rendered successfully")
                print(f"  Result: {result.strip()}")
                return True
            except Exception as e:
                print(f"✗ Thermal receipt template failed: {e}")
                import traceback
                traceback.print_exc()
                return False
                
    except Exception as e:
        print(f"✗ Error creating app: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_shift_report_template():
    """اختبار قالب تقرير الوردية - Test shift report template"""
    try:
        from app import create_app
        
        app = create_app('development')
        
        with app.app_context():
            from flask import render_template_string
            
            # Test the shift report template line
            template = """
            <p class="mb-2">تم إنشاء هذا التقرير في: {{ moment().format('YYYY-MM-DD HH:mm:ss') }}</p>
            """
            
            try:
                result = render_template_string(template)
                print(f"✓ Shift report template rendered successfully")
                print(f"  Result: {result.strip()}")
                return True
            except Exception as e:
                print(f"✗ Shift report template failed: {e}")
                return False
                
    except Exception as e:
        print(f"✗ Error testing shift report: {e}")
        return False

def test_start_shift_template():
    """اختبار قالب بدء الوردية - Test start shift template"""
    try:
        from app import create_app
        
        app = create_app('development')
        
        with app.app_context():
            from flask import render_template_string
            
            # Test the start shift template lines
            template = """
            <div>
                <span class="font-medium">التاريخ:</span> {{ moment().format('YYYY-MM-DD') }}
            </div>
            <div>
                <span class="font-medium">الوقت:</span> {{ moment().format('HH:mm:ss') }}
            </div>
            """
            
            try:
                result = render_template_string(template)
                print(f"✓ Start shift template rendered successfully")
                print(f"  Result: {result.strip()}")
                return True
            except Exception as e:
                print(f"✗ Start shift template failed: {e}")
                return False
                
    except Exception as e:
        print(f"✗ Error testing start shift: {e}")
        return False

def main():
    """الدالة الرئيسية - Main function"""
    print("🧪 Testing Templates with Moment Function")
    print("=" * 60)
    
    # Test thermal receipt template
    thermal_test = test_thermal_receipt_template()
    
    # Test shift report template
    shift_report_test = test_shift_report_template()
    
    # Test start shift template
    start_shift_test = test_start_shift_template()
    
    print("\n" + "=" * 60)
    print("📊 Test Results:")
    print(f"Thermal Receipt: {'✓ PASS' if thermal_test else '✗ FAIL'}")
    print(f"Shift Report: {'✓ PASS' if shift_report_test else '✗ FAIL'}")
    print(f"Start Shift: {'✓ PASS' if start_shift_test else '✗ FAIL'}")
    
    if thermal_test and shift_report_test and start_shift_test:
        print("\n🎉 All template tests passed! The moment function fix is working.")
        return 0
    else:
        print("\n❌ Some template tests failed.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
