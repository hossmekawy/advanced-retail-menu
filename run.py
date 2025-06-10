#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Run Script - سكريبت تشغيل بسيط
Use this to run the application with proper environment setup
"""

import os
import sys
from app import create_app

def main():
    """Main function to run the application"""
    
    # Set default environment if not set
    if 'FLASK_ENV' not in os.environ:
        os.environ['FLASK_ENV'] = 'development'
    
    print("🚀 Starting Advanced Retail Menu Application...")
    print(f"📊 Environment: {os.environ.get('FLASK_ENV', 'development')}")
    print("📱 Application will be available at:")
    print("   - Local: http://127.0.0.1:5000")
    print("   - Network: http://192.168.1.113:5000")
    print("\n🛑 Press CTRL+C to stop the server")
    print("-" * 60)
    
    try:
        # Create and run the application
        app = create_app()
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
