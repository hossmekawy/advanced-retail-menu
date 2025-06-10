# -*- coding: utf-8 -*-
"""
مسارات البلوبرينت الأساسي - Core Blueprint Routes
"""
from flask import render_template, session, redirect, url_for, request, flash
from i18n import _
from core import bp
from models import Settings, Category, Product, ContentPage


@bp.route('/')
def index():
    """الصفحة الرئيسية - Home page"""
    settings = Settings.get_settings()
    
    # الحصول على المنتجات المميزة - Get featured products
    featured_products = Product.query.filter_by(
        is_active=True, 
        is_featured=True
    ).order_by(Product.sort_order).limit(6).all()
    
    # الحصول على الفئات النشطة - Get active categories
    categories = Category.query.filter_by(
        is_active=True
    ).order_by(Category.sort_order).all()
    
    return render_template('core/index.html',
                         featured_products=featured_products,
                         categories=categories)


@bp.route('/menu')
def menu():
    """صفحة القائمة الكاملة - Full menu page"""
    # الحصول على الفئات مع المنتجات - Get categories with products
    categories = Category.query.filter_by(is_active=True)\
                              .order_by(Category.sort_order).all()
    
    return render_template('core/menu.html', categories=categories)


@bp.route('/category/<int:category_id>')
def category_detail(category_id):
    """تفاصيل الفئة - Category detail page"""
    category = Category.query.get_or_404(category_id)
    
    if not category.is_active:
        flash(_('هذه الفئة غير متاحة حالياً'), 'warning')
        return redirect(url_for('core.menu'))
    
    # الحصول على المنتجات في هذه الفئة - Get products in this category
    products = Product.query.filter_by(
        category_id=category_id,
        is_active=True
    ).order_by(Product.sort_order).all()
    
    return render_template('core/category_detail.html',
                         category=category,
                         products=products)


@bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """تفاصيل المنتج - Product detail page"""
    product = Product.query.get_or_404(product_id)
    
    if not product.is_active:
        flash(_('هذا المنتج غير متاح حالياً'), 'warning')
        return redirect(url_for('core.menu'))
    
    # منتجات مشابهة من نفس الفئة - Similar products from same category
    similar_products = Product.query.filter(
        Product.category_id == product.category_id,
        Product.id != product.id,
        Product.is_active == True
    ).limit(4).all()
    
    return render_template('core/product_detail.html',
                         product=product,
                         similar_products=similar_products)


@bp.route('/settings/lang/<lang>')
def set_language(lang):
    """تغيير اللغة - Change language"""
    from flask import current_app
    
    if lang in current_app.config['LANGUAGES']:
        session['lang'] = lang
        flash(_('تم تغيير اللغة بنجاح'), 'success')
    else:
        flash(_('اللغة المحددة غير مدعومة'), 'error')
    
    # العودة للصفحة السابقة أو الرئيسية - Return to previous page or home
    return redirect(request.referrer or url_for('core.index'))


@bp.route('/about')
def about():
    """صفحة حول المتجر - About page"""
    page = ContentPage.get_page('about')
    return render_template('core/about.html', page=page)


@bp.route('/contact')
def contact():
    """صفحة الاتصال - Contact page"""
    page = ContentPage.get_page('contact')
    return render_template('core/contact.html', page=page)
