# -*- coding: utf-8 -*-
"""
نظام الترجمة المبسط - Simplified Translation System
"""
from flask import session

# قاموس الترجمات - Translation dictionary
TRANSLATIONS = {
    'ar': {
        # Navigation
        'الرئيسية': 'الرئيسية',
        'القائمة': 'القائمة',
        'حول المتجر': 'حول المتجر',
        'اتصل بنا': 'اتصل بنا',
        'تسجيل الدخول': 'تسجيل الدخول',
        'لوحة التحكم': 'لوحة التحكم',
        
        # Common
        'حفظ': 'حفظ',
        'إلغاء': 'إلغاء',
        'تعديل': 'تعديل',
        'حذف': 'حذف',
        'إضافة': 'إضافة',
        'عرض': 'عرض',
        'البحث': 'البحث',
        'نشط': 'نشط',
        'غير نشط': 'غير نشط',
        
        # Admin
        'الفئات': 'الفئات',
        'المنتجات': 'المنتجات',
        'الإعدادات': 'الإعدادات',
        'إدارة الفئات': 'إدارة الفئات',
        'إضافة فئة جديدة': 'إضافة فئة جديدة',
        
        # Forms
        'الاسم بالعربية': 'الاسم بالعربية',
        'الاسم بالإنجليزية': 'الاسم بالإنجليزية',
        'الوصف بالعربية': 'الوصف بالعربية',
        'الوصف بالإنجليزية': 'الوصف بالإنجليزية',
        'اسم المستخدم': 'اسم المستخدم',
        'كلمة المرور': 'كلمة المرور',
        
        # Messages
        'تم الحفظ بنجاح': 'تم الحفظ بنجاح',
        'حدث خطأ': 'حدث خطأ',
        'لا توجد بيانات': 'لا توجد بيانات',
    },
    'en': {
        # Navigation
        'الرئيسية': 'Home',
        'القائمة': 'Menu',
        'حول المتجر': 'About',
        'اتصل بنا': 'Contact',
        'تسجيل الدخول': 'Login',
        'لوحة التحكم': 'Dashboard',
        
        # Common
        'حفظ': 'Save',
        'إلغاء': 'Cancel',
        'تعديل': 'Edit',
        'حذف': 'Delete',
        'إضافة': 'Add',
        'عرض': 'View',
        'البحث': 'Search',
        'نشط': 'Active',
        'غير نشط': 'Inactive',
        
        # Admin
        'الفئات': 'Categories',
        'المنتجات': 'Products',
        'الإعدادات': 'Settings',
        'إدارة الفئات': 'Manage Categories',
        'إضافة فئة جديدة': 'Add New Category',
        
        # Forms
        'الاسم بالعربية': 'Arabic Name',
        'الاسم بالإنجليزية': 'English Name',
        'الوصف بالعربية': 'Arabic Description',
        'الوصف بالإنجليزية': 'English Description',
        'اسم المستخدم': 'Username',
        'كلمة المرور': 'Password',
        
        # Messages
        'تم الحفظ بنجاح': 'Saved successfully',
        'حدث خطأ': 'An error occurred',
        'لا توجد بيانات': 'No data found',
    }
}


def _(text):
    """دالة الترجمة المبسطة - Simple translation function"""
    current_lang = session.get('lang', 'ar')
    
    if current_lang in TRANSLATIONS and text in TRANSLATIONS[current_lang]:
        return TRANSLATIONS[current_lang][text]
    
    # إذا لم توجد الترجمة، أرجع النص الأصلي - If no translation found, return original text
    return text


def get_current_language():
    """الحصول على اللغة الحالية - Get current language"""
    return session.get('lang', 'ar')


def set_language(lang):
    """تعيين اللغة - Set language"""
    if lang in ['ar', 'en']:
        session['lang'] = lang
        return True
    return False
