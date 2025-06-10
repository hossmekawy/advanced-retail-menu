@echo off
REM Advanced Retail Menu - Windows Run Script
REM سكريبت تشغيل ويندوز - قائمة البيع المتقدمة

echo.
echo ========================================
echo   Advanced Retail Menu Application
echo   تطبيق قائمة البيع المتقدمة
echo ========================================
echo.

REM Set environment variables
set FLASK_ENV=development
set FLASK_APP=app.py

echo Starting application...
echo بدء تشغيل التطبيق...
echo.

REM Run the application
python run.py

pause
