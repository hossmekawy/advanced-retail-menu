#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Production Deployment Script - سكريبت النشر للإنتاج
Use this script to run the application with Gunicorn for production
"""

import os
import sys
import subprocess

def check_gunicorn():
    """Check if Gunicorn is installed"""
    try:
        import gunicorn
        return True
    except ImportError:
        return False

def install_gunicorn():
    """Install Gunicorn"""
    print("📦 Installing Gunicorn...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "gunicorn"])
        print("✅ Gunicorn installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Gunicorn")
        return False

def main():
    """Main function to run the application in production"""
    
    # Set production environment
    os.environ['FLASK_ENV'] = 'production'
    os.environ['FLASK_APP'] = 'wsgi.py'
    
    print("🚀 Starting Advanced Retail Menu Application (Production Mode)")
    print("📊 Environment: Production")
    
    # Check if Gunicorn is available
    if not check_gunicorn():
        print("⚠️  Gunicorn not found. Installing...")
        if not install_gunicorn():
            print("❌ Cannot install Gunicorn. Falling back to development server.")
            from app import create_app
            app = create_app('production')
            app.run(host='0.0.0.0', port=5000, debug=False)
            return
    
    print("📱 Application will be available at:")
    print("   - Local: http://127.0.0.1:5000")
    print("   - Network: http://0.0.0.0:5000")
    print("\n🛑 Press CTRL+C to stop the server")
    print("-" * 60)
    
    try:
        # Run with Gunicorn
        cmd = [
            "gunicorn",
            "--bind", "0.0.0.0:5000",
            "--workers", "4",
            "--timeout", "120",
            "--keep-alive", "2",
            "--max-requests", "1000",
            "--max-requests-jitter", "100",
            "wsgi:app"
        ]
        
        print("🔧 Starting Gunicorn server...")
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
