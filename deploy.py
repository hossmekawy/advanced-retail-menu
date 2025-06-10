#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deployment Script - سكريبت النشر
Run this script to start the application in production mode
"""

import os
import sys
from app import create_app

def main():
    """Main deployment function"""
    
    # Set environment variables for production
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_APP'] = 'wsgi.py'
    
    # Create the application
    app = create_app('production')
    
    print("🚀 Starting Advanced Retail Menu Application...")
    print("📱 Application will be available at:")
    print("   - Local: http://127.0.0.1:5000")
    print("   - Network: http://0.0.0.0:5000")
    print("\n⚠️  Note: This is a development server. For production, use a WSGI server like Gunicorn.")
    print("   Example: gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app")
    print("\n🛑 Press CTRL+C to stop the server")
    print("-" * 60)
    
    try:
        # Run the application
        app.run(
            host='0.0.0.0',
            port=5000,
            debug=False,  # Disable debug in production
            threaded=True
        )
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
