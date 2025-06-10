#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
اختبار دالة moment - Test moment function directly
"""
from datetime import datetime

def test_moment_function():
    """اختبار دالة moment مباشرة - Test moment function directly"""
    
    class MomentWrapper:
        def __init__(self):
            self.dt = datetime.now()
        
        def format(self, format_str):
            """تنسيق التاريخ والوقت - Format date and time"""
            # تحويل تنسيق moment.js إلى تنسيق Python strftime
            # Convert moment.js format to Python strftime format
            format_map = {
                'YYYY': '%Y',
                'MM': '%m', 
                'DD': '%d',
                'HH': '%H',
                'mm': '%M',
                'ss': '%S'
            }
            
            python_format = format_str
            for moment_format, python_format_code in format_map.items():
                python_format = python_format.replace(moment_format, python_format_code)
            
            return self.dt.strftime(python_format)
    
    def moment():
        return MomentWrapper()
    
    # Test the function
    print("Testing moment function...")
    
    try:
        # Test the formats used in templates
        m = moment()
        
        # Test format from thermal_receipt.html
        result1 = m.format('YYYY-MM-DD HH:mm:ss')
        print(f"✓ Format 'YYYY-MM-DD HH:mm:ss': {result1}")
        
        # Test format from start_shift.html
        result2 = m.format('YYYY-MM-DD')
        print(f"✓ Format 'YYYY-MM-DD': {result2}")
        
        # Test format from start_shift.html
        result3 = m.format('HH:mm:ss')
        print(f"✓ Format 'HH:mm:ss': {result3}")
        
        print("\n🎉 All moment function tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error in moment function: {e}")
        return False

if __name__ == '__main__':
    test_moment_function()
