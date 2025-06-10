#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
التحقق النهائي - Final verification
"""
import os

def verify_fixes():
    """التحقق من الإصلاحات - Verify fixes"""
    print("🔍 Final Verification of Fixes")
    print("=" * 40)
    
    # 1. Check if moment function is added to app.py
    print("1. Checking moment function in app.py...")
    try:
        with open('app.py', 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'def moment():' in content and "'moment': moment" in content:
            print("   ✅ Moment function properly added to template context")
        else:
            print("   ❌ Moment function not found")
            return False
    except Exception as e:
        print(f"   ❌ Error reading app.py: {e}")
        return False
    
    # 2. Check if invoice_form.html exists
    print("2. Checking invoice_form.html template...")
    template_path = "templates/admin/pos/invoice_form.html"
    if os.path.exists(template_path):
        file_size = os.path.getsize(template_path)
        print(f"   ✅ Template exists ({file_size} bytes)")
    else:
        print("   ❌ Template not found")
        return False
    
    # 3. Check thermal_receipt.html for moment usage
    print("3. Checking thermal_receipt.html...")
    thermal_path = "templates/admin/pos/thermal_receipt.html"
    if os.path.exists(thermal_path):
        with open(thermal_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if "moment().format('YYYY-MM-DD HH:mm:ss')" in content:
            print("   ✅ Thermal receipt uses moment function")
        else:
            print("   ❌ Moment function not used in thermal receipt")
            return False
    else:
        print("   ❌ Thermal receipt template not found")
        return False
    
    print("\n🎉 ALL FIXES VERIFIED SUCCESSFULLY!")
    print("\nSummary of fixes:")
    print("• Added moment() function to Flask template context")
    print("• Verified invoice_form.html template exists")
    print("• Confirmed thermal receipt template uses moment function")
    print("\nYour Flask application should now work without the reported errors.")
    
    return True

if __name__ == '__main__':
    verify_fixes()
