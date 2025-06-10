# 🚀 Deployment Guide / دليل النشر

This guide covers deploying the Advanced Retail Menu System to various platforms.

هذا الدليل يغطي نشر نظام قائمة المتجر المتقدم على منصات مختلفة.

## 📋 Pre-deployment Checklist / قائمة ما قبل النشر

### ✅ Required Files / الملفات المطلوبة
- [ ] `requirements.txt` - Python dependencies / تبعيات Python
- [ ] `wsgi.py` - WSGI entry point / نقطة دخول WSGI
- [ ] `runtime.txt` - Python version / إصدار Python
- [ ] `.env` file configured / ملف البيئة مُعد
- [ ] Database migrations ready / هجرات قاعدة البيانات جاهزة

### ✅ Security Checklist / قائمة الأمان
- [ ] Create admin users through admin panel / إنشاء مستخدمين إداريين من لوحة الإدارة
- [ ] Set strong SECRET_KEY / تعيين مفتاح سري قوي
- [ ] Configure proper database URL / تكوين رابط قاعدة البيانات الصحيح
- [ ] Enable HTTPS in production / تفعيل HTTPS في الإنتاج
- [ ] Remove or disable default admin account / إزالة أو تعطيل حساب الإدارة الافتراضي
- [ ] Set FLASK_ENV=production / تعيين بيئة الإنتاج

## 🌐 PythonAnywhere Deployment / النشر على PythonAnywhere

### Step 1: Upload Files / الخطوة 1: رفع الملفات

1. **Zip your project / ضغط المشروع**
```bash
# Exclude unnecessary files / استبعاد الملفات غير الضرورية
zip -r menu-system.zip . -x "venv/*" "__pycache__/*" "*.pyc" ".git/*" "node_modules/*"
```

2. **Upload to PythonAnywhere / رفع إلى PythonAnywhere**
   - Go to Files tab / اذهب لتبويب الملفات
   - Upload the zip file / ارفع الملف المضغوط
   - Extract in your home directory / استخرج في المجلد الرئيسي

### Step 2: Setup Virtual Environment / الخطوة 2: إعداد البيئة الافتراضية

```bash
# Open Bash console / افتح وحدة تحكم Bash
cd ~/menu-system

# Create virtual environment / إنشاء بيئة افتراضية
mkvirtualenv --python=/usr/bin/python3.10 menu-system

# Activate environment / تفعيل البيئة
workon menu-system

# Install dependencies / تثبيت التبعيات
pip install -r requirements.txt
```

### Step 3: Configure Environment / الخطوة 3: تكوين البيئة

Create `.env` file / إنشاء ملف البيئة:
```bash
nano .env
```

Add configuration / إضافة التكوين:
```env
FLASK_ENV=production
SECRET_KEY=your-super-secret-production-key-here
DATABASE_URL=sqlite:///shop_menu.db
```

### Step 4: Initialize Database / الخطوة 4: تهيئة قاعدة البيانات

```bash
# Initialize database / تهيئة قاعدة البيانات
python -c "
from app import create_app
from extensions import db
from models import Settings

app = create_app('production')
with app.app_context():
    db.create_all()

    # Create default settings / إنشاء إعدادات افتراضية
    Settings.get_settings()
    print('Database initialized successfully!')
    print('Note: Default admin user will be created automatically on first run.')
    print('Use the admin panel to create additional users.')
"
```

### Step 5: Configure Web App / الخطوة 5: تكوين تطبيق الويب

1. **Go to Web tab / اذهب لتبويب الويب**
2. **Create new web app / إنشاء تطبيق ويب جديد**
3. **Choose Manual configuration / اختر التكوين اليدوي**
4. **Select Python 3.10 / اختر Python 3.10**

### Step 6: Configure WSGI File / الخطوة 6: تكوين ملف WSGI

Edit the WSGI file / تعديل ملف WSGI:
```python
import sys
import os

# Add your project directory to sys.path
path = '/home/yourusername/menu-system'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['FLASK_ENV'] = 'production'

from wsgi import app as application
```

### Step 7: Configure Virtual Environment / الخطوة 7: تكوين البيئة الافتراضية

In the Web tab / في تبويب الويب:
- **Virtualenv**: `/home/yourusername/.virtualenvs/menu-system`
- **Source code**: `/home/yourusername/menu-system`
- **Working directory**: `/home/yourusername/menu-system`

### Step 8: Configure Static Files / الخطوة 8: تكوين الملفات الثابتة

Add static files mapping / إضافة تخطيط الملفات الثابتة:
- **URL**: `/static/`
- **Directory**: `/home/yourusername/menu-system/static/`

### Step 9: Reload and Test / الخطوة 9: إعادة التحميل والاختبار

1. **Click "Reload" button / اضغط زر "إعادة التحميل"**
2. **Visit your domain / زر موقعك**
3. **Test admin login / اختبر تسجيل دخول الإدارة**

## 🐳 Docker Deployment / النشر باستخدام Docker

### Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=your-secret-key
      - DATABASE_URL=sqlite:///shop_menu.db
    volumes:
      - ./data:/app/data
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - web
    restart: unless-stopped
```

### Build and Run / البناء والتشغيل
```bash
# Build and start / البناء والتشغيل
docker-compose up -d

# View logs / عرض السجلات
docker-compose logs -f

# Stop services / إيقاف الخدمات
docker-compose down
```

## ☁️ Cloud Platform Deployment / النشر على المنصات السحابية

### Heroku
```bash
# Install Heroku CLI / تثبيت Heroku CLI
# Create Procfile
echo "web: gunicorn wsgi:app" > Procfile

# Initialize git and deploy / تهيئة git والنشر
git init
git add .
git commit -m "Initial commit"
heroku create your-app-name
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
```

### Railway
```bash
# Install Railway CLI / تثبيت Railway CLI
npm install -g @railway/cli

# Login and deploy / تسجيل الدخول والنشر
railway login
railway init
railway up
```

### DigitalOcean App Platform
1. Connect GitHub repository / ربط مستودع GitHub
2. Configure build settings / تكوين إعدادات البناء
3. Set environment variables / تعيين متغيرات البيئة
4. Deploy / النشر

## 🔧 Production Optimizations / تحسينات الإنتاج

### 1. Database Optimization / تحسين قاعدة البيانات
```python
# Use PostgreSQL for production / استخدم PostgreSQL للإنتاج
DATABASE_URL=postgresql://user:password@localhost/dbname

# Add database indexes / إضافة فهارس قاعدة البيانات
# In models.py
class Product(db.Model):
    # Add indexes for better performance
    __table_args__ = (
        db.Index('idx_product_category', 'category_id'),
        db.Index('idx_product_active', 'is_active'),
        db.Index('idx_product_featured', 'is_featured'),
    )
```

### 2. Caching / التخزين المؤقت
```python
# Install Redis / تثبيت Redis
pip install redis flask-caching

# Configure caching / تكوين التخزين المؤقت
from flask_caching import Cache
cache = Cache(app, config={'CACHE_TYPE': 'redis'})
```

### 3. CDN for Static Files / شبكة توصيل محتوى للملفات الثابتة
```python
# Use AWS S3 or CloudFlare / استخدم AWS S3 أو CloudFlare
STATIC_URL = 'https://cdn.yourdomain.com/static/'
```

### 4. SSL/HTTPS Configuration / تكوين SSL/HTTPS
```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /etc/nginx/ssl/cert.pem;
    ssl_certificate_key /etc/nginx/ssl/key.pem;
    
    location / {
        proxy_pass http://web:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔍 Monitoring and Maintenance / المراقبة والصيانة

### 1. Logging / السجلات
```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
```

### 2. Health Checks / فحوصات الصحة
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()}
```

### 3. Database Backups / النسخ الاحتياطية لقاعدة البيانات
```bash
# SQLite backup / نسخة احتياطية SQLite
cp shop_menu.db shop_menu_backup_$(date +%Y%m%d).db

# PostgreSQL backup / نسخة احتياطية PostgreSQL
pg_dump dbname > backup_$(date +%Y%m%d).sql
```

## 🚨 Troubleshooting / استكشاف الأخطاء

### Common Issues / المشاكل الشائعة

1. **Import Errors / أخطاء الاستيراد**
   - Check Python path / تحقق من مسار Python
   - Verify virtual environment / تحقق من البيئة الافتراضية

2. **Database Connection / اتصال قاعدة البيانات**
   - Check DATABASE_URL / تحقق من رابط قاعدة البيانات
   - Verify database permissions / تحقق من صلاحيات قاعدة البيانات

3. **Static Files Not Loading / الملفات الثابتة لا تحمل**
   - Check static files mapping / تحقق من تخطيط الملفات الثابتة
   - Verify file permissions / تحقق من صلاحيات الملفات

4. **Memory Issues / مشاكل الذاكرة**
   - Optimize image sizes / حسن أحجام الصور
   - Use pagination for large datasets / استخدم التصفح للبيانات الكبيرة

### Debug Mode / وضع التصحيح
```python
# Enable debug mode for troubleshooting / تفعيل وضع التصحيح
FLASK_ENV=development
FLASK_DEBUG=1
```

## 📞 Support / الدعم

For deployment issues / لمشاكل النشر:
- Check logs first / تحقق من السجلات أولاً
- Review configuration / راجع التكوين
- Contact support / اتصل بالدعم

---

**Note**: Always test your deployment in a staging environment before going live.

**ملاحظة**: اختبر دائماً النشر في بيئة تجريبية قبل النشر المباشر.
