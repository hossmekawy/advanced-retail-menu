# -*- coding: utf-8 -*-
"""
مسارات API - API Routes
"""
from flask import jsonify, request, session
from api import bp
from models import Category, SubCategory, Product, Settings


def serialize_category(category, lang='ar'):
    """تسلسل الفئة - Serialize category"""
    return {
        'id': category.id,
        'name': category.get_name(lang),
        'description': category.get_description(lang),
        'icon': category.icon,
        'sort_order': category.sort_order,
        'products': [serialize_product(p, lang) for p in category.products if p.is_active],
        'subcategories': [serialize_subcategory(s, lang) for s in category.subcategories if s.is_active]
    }


def serialize_subcategory(subcategory, lang='ar'):
    """تسلسل الفئة الفرعية - Serialize subcategory"""
    return {
        'id': subcategory.id,
        'category_id': subcategory.category_id,
        'name': subcategory.get_name(lang),
        'description': subcategory.get_description(lang),
        'sort_order': subcategory.sort_order,
        'products': [serialize_product(p, lang) for p in subcategory.products if p.is_active]
    }


def serialize_product(product, lang='ar'):
    """تسلسل المنتج - Serialize product"""
    return {
        'id': product.id,
        'category_id': product.category_id,
        'subcategory_id': product.subcategory_id,
        'name': product.get_name(lang),
        'description': product.get_description(lang),
        'ingredients': product.get_ingredients(lang),
        'price': float(product.price),
        'currency': product.currency,
        'formatted_price': product.get_formatted_price(),
        'photo_b64': product.photo_b64,
        'sort_order': product.sort_order,
        'is_featured': product.is_featured
    }


def serialize_settings(settings):
    """تسلسل الإعدادات - Serialize settings"""
    return {
        'shop_name': settings.shop_name,
        'primary_color': settings.primary_color,
        'secondary_color': settings.secondary_color,
        'logo_b64': settings.logo_b64,
        'default_currency': settings.default_currency,
        'default_lang': settings.default_lang
    }


@bp.route('/menu')
def get_menu():
    """الحصول على القائمة الكاملة - Get full menu"""
    lang = request.args.get('lang', session.get('lang', 'ar'))
    
    # الحصول على الفئات النشطة مع المنتجات - Get active categories with products
    categories = Category.query.filter_by(is_active=True)\
                              .order_by(Category.sort_order).all()
    
    # تصفية المنتجات النشطة فقط - Filter only active products
    for category in categories:
        category.products = [p for p in category.products if p.is_active]
        for subcategory in category.subcategories:
            if subcategory.is_active:
                subcategory.products = [p for p in subcategory.products if p.is_active]
    
    # تسلسل البيانات - Serialize data
    result = [serialize_category(cat, lang) for cat in categories]

    return jsonify({
        'success': True,
        'data': result,
        'language': lang
    })


@bp.route('/categories')
def get_categories():
    """الحصول على قائمة الفئات - Get categories list"""
    lang = request.args.get('lang', session.get('lang', 'ar'))
    
    categories = Category.query.filter_by(is_active=True)\
                              .order_by(Category.sort_order).all()
    
    result = [serialize_category(cat, lang) for cat in categories]
    
    return jsonify({
        'success': True,
        'data': result,
        'language': lang
    })


@bp.route('/categories/<int:category_id>')
def get_category(category_id):
    """الحصول على فئة محددة - Get specific category"""
    lang = request.args.get('lang', session.get('lang', 'ar'))
    
    category = Category.query.filter_by(id=category_id, is_active=True).first()
    
    if not category:
        return jsonify({
            'success': False,
            'message': 'Category not found'
        }), 404
    
    # تصفية المنتجات النشطة فقط - Filter only active products
    category.products = [p for p in category.products if p.is_active]
    
    result = serialize_category(category, lang)
    
    return jsonify({
        'success': True,
        'data': result,
        'language': lang
    })


@bp.route('/products')
def get_products():
    """الحصول على قائمة المنتجات - Get products list"""
    lang = request.args.get('lang', session.get('lang', 'ar'))
    category_id = request.args.get('category_id', type=int)
    subcategory_id = request.args.get('subcategory_id', type=int)
    featured_only = request.args.get('featured', type=bool, default=False)
    
    # بناء الاستعلام - Build query
    query = Product.query.filter_by(is_active=True)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if subcategory_id:
        query = query.filter_by(subcategory_id=subcategory_id)
    
    if featured_only:
        query = query.filter_by(is_featured=True)
    
    products = query.order_by(Product.sort_order).all()
    
    result = [serialize_product(prod, lang) for prod in products]
    
    return jsonify({
        'success': True,
        'data': result,
        'language': lang,
        'count': len(result)
    })


@bp.route('/products/<int:product_id>')
def get_product(product_id):
    """الحصول على منتج محدد - Get specific product"""
    lang = request.args.get('lang', session.get('lang', 'ar'))
    
    product = Product.query.filter_by(id=product_id, is_active=True).first()
    
    if not product:
        return jsonify({
            'success': False,
            'message': 'Product not found'
        }), 404
    
    result = serialize_product(product, lang)
    
    return jsonify({
        'success': True,
        'data': result,
        'language': lang
    })


@bp.route('/settings')
def get_settings():
    """الحصول على إعدادات المتجر - Get shop settings"""
    settings = Settings.get_settings()
    
    result = serialize_settings(settings)
    
    return jsonify({
        'success': True,
        'data': result
    })


@bp.route('/search')
def search_products():
    """البحث في المنتجات - Search products"""
    lang = request.args.get('lang', session.get('lang', 'ar'))
    query = request.args.get('q', '').strip()
    
    if not query:
        return jsonify({
            'success': False,
            'message': 'Search query is required'
        }), 400
    
    # البحث في أسماء المنتجات والأوصاف - Search in product names and descriptions
    if lang == 'ar':
        products = Product.query.filter(
            Product.is_active == True,
            (Product.name_ar.contains(query) | 
             Product.description_ar.contains(query) |
             Product.ingredients_ar.contains(query))
        ).order_by(Product.sort_order).all()
    else:
        products = Product.query.filter(
            Product.is_active == True,
            (Product.name_en.contains(query) | 
             Product.description_en.contains(query) |
             Product.ingredients_en.contains(query))
        ).order_by(Product.sort_order).all()
    
    result = [serialize_product(prod, lang) for prod in products]
    
    return jsonify({
        'success': True,
        'data': result,
        'language': lang,
        'query': query,
        'count': len(result)
    })
