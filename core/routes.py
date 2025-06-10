# -*- coding: utf-8 -*-
"""
مسارات البلوبرينت الأساسي - Core Blueprint Routes
"""
from flask import render_template, session, redirect, url_for, request, flash, jsonify
from datetime import datetime
from i18n import _
from core import bp
from models import Settings, Category, Product, ContentPage, RestaurantTable, Order, OrderItem
from extensions import db, csrf


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


# مسارات السلة والطلبات - Cart and Order Routes

def get_cart():
    """الحصول على السلة من الجلسة - Get cart from session"""
    if 'cart' not in session:
        session['cart'] = {}
    return session['cart']


def save_cart(cart):
    """حفظ السلة في الجلسة - Save cart to session"""
    session['cart'] = cart
    session.modified = True


def calculate_cart_total(cart):
    """حساب إجمالي السلة - Calculate cart total"""
    total = 0
    for product_id, item in cart.items():
        total += item['price'] * item['quantity']
    return total


def get_cart_count():
    """الحصول على عدد العناصر في السلة - Get cart items count"""
    cart = get_cart()
    return sum(item['quantity'] for item in cart.values())


@bp.route('/cart')
def view_cart():
    """عرض السلة - View cart"""
    cart = get_cart()
    cart_items = []

    for product_id, item in cart.items():
        product = Product.query.get(int(product_id))
        if product:
            cart_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price': item['price'],
                'total': item['price'] * item['quantity']
            })

    total = calculate_cart_total(cart)

    return render_template('core/cart.html',
                         cart_items=cart_items,
                         total=total,
                         cart_count=get_cart_count())


@bp.route('/cart/add/<int:product_id>', methods=['POST'])
@csrf.exempt
def add_to_cart(product_id):
    """إضافة منتج للسلة - Add product to cart"""
    try:
        product = Product.query.get_or_404(product_id)

        if not product.is_active:
            flash(_('هذا المنتج غير متاح حالياً'), 'error')
            return redirect(request.referrer or url_for('core.menu'))

        # Get quantity with better error handling
        try:
            quantity = int(request.form.get('quantity', 1))
        except (ValueError, TypeError):
            quantity = 1

        if quantity < 1:
            quantity = 1

        cart = get_cart()
        product_id_str = str(product_id)

        if product_id_str in cart:
            cart[product_id_str]['quantity'] += quantity
        else:
            cart[product_id_str] = {
                'quantity': quantity,
                'price': float(product.price),
                'name_ar': product.name_ar,
                'name_en': product.name_en
            }

        save_cart(cart)

        # Check if this is an AJAX request
        is_ajax = (request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
                  request.headers.get('Content-Type') == 'application/json' or
                  request.is_json)

        if is_ajax:
            return jsonify({
                'success': True,
                'message': _('تم إضافة المنتج للسلة بنجاح'),
                'cart_count': get_cart_count()
            })

        flash(_('تم إضافة المنتج للسلة بنجاح'), 'success')
        return redirect(request.referrer or url_for('core.menu'))

    except Exception as e:
        # Log the error for debugging
        print(f"Error adding to cart: {str(e)}")
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request form: {dict(request.form)}")

        # Check if this is an AJAX request
        is_ajax = (request.headers.get('X-Requested-With') == 'XMLHttpRequest' or
                  request.headers.get('Content-Type') == 'application/json' or
                  request.is_json)

        if is_ajax:
            return jsonify({
                'success': False,
                'message': _('حدث خطأ أثناء إضافة المنتج'),
                'error': str(e)
            }), 400

        flash(_('حدث خطأ أثناء إضافة المنتج'), 'error')
        return redirect(request.referrer or url_for('core.menu'))


@bp.route('/cart/update/<int:product_id>', methods=['POST'])
@csrf.exempt
def update_cart(product_id):
    """تحديث كمية منتج في السلة - Update product quantity in cart"""
    quantity = int(request.form.get('quantity', 1))
    cart = get_cart()
    product_id_str = str(product_id)

    if product_id_str in cart:
        if quantity > 0:
            cart[product_id_str]['quantity'] = quantity
        else:
            del cart[product_id_str]

        save_cart(cart)
        flash(_('تم تحديث السلة بنجاح'), 'success')

    return redirect(url_for('core.view_cart'))


@bp.route('/cart/remove/<int:product_id>', methods=['POST'])
@csrf.exempt
def remove_from_cart(product_id):
    """إزالة منتج من السلة - Remove product from cart"""
    cart = get_cart()
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        save_cart(cart)
        flash(_('تم إزالة المنتج من السلة'), 'success')

    return redirect(url_for('core.view_cart'))


@bp.route('/cart/clear', methods=['POST'])
@csrf.exempt
def clear_cart():
    """مسح السلة - Clear cart"""
    session['cart'] = {}
    session.modified = True
    flash(_('تم مسح السلة'), 'info')
    return redirect(url_for('core.view_cart'))


@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """صفحة الدفع - Checkout page"""
    cart = get_cart()

    if not cart:
        flash(_('السلة فارغة'), 'warning')
        return redirect(url_for('core.menu'))

    # الحصول على الطاولات المتاحة - Get available tables
    available_tables = RestaurantTable.query.filter_by(
        is_active=True,
        status='available'
    ).order_by(RestaurantTable.table_number).all()

    if not available_tables:
        flash(_('لا توجد طاولات متاحة حالياً'), 'warning')
        return redirect(url_for('core.view_cart'))

    if request.method == 'POST':
        # التحقق من البيانات المطلوبة - Validate required data
        customer_name = request.form.get('customer_name', '').strip()
        customer_phone = request.form.get('customer_phone', '').strip()
        table_id = request.form.get('table_id')
        notes = request.form.get('notes', '').strip()

        # التحقق من صحة البيانات - Validate data
        errors = []
        if not customer_name:
            errors.append(_('اسم العميل مطلوب'))
        if not customer_phone:
            errors.append(_('رقم الهاتف مطلوب'))
        if not table_id:
            errors.append(_('يجب اختيار طاولة'))

        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('core/checkout.html',
                                 available_tables=available_tables,
                                 cart_total=calculate_cart_total(cart),
                                 cart_count=get_cart_count())

        # التحقق من توفر الطاولة - Check table availability
        table = RestaurantTable.query.get(table_id)
        if not table or table.status != 'available':
            flash(_('الطاولة المحددة غير متاحة'), 'error')
            return render_template('core/checkout.html',
                                 available_tables=available_tables,
                                 cart_total=calculate_cart_total(cart),
                                 cart_count=get_cart_count())

        try:
            # إنشاء الطلب - Create order
            order = Order(
                customer_name=customer_name,
                customer_phone=customer_phone,
                table_id=table_id,
                total_amount=calculate_cart_total(cart),
                notes=notes,
                status='pending'  # الطلب في انتظار موافقة الإدارة - Order pending admin approval
            )
            order.order_number = order.generate_order_number()

            db.session.add(order)
            db.session.flush()  # للحصول على معرف الطلب - Get order ID

            # إضافة عناصر الطلب - Add order items
            for product_id, item in cart.items():
                product = Product.query.get(int(product_id))
                if product:
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=item['quantity'],
                        unit_price=item['price'],
                        total_price=item['price'] * item['quantity']
                    )
                    db.session.add(order_item)

            # تحديث حالة الطاولة - Update table status
            table.status = 'reserved'  # محجوزة في انتظار تأكيد الإدارة - Reserved pending admin confirmation

            db.session.commit()

            # مسح السلة - Clear cart
            session['cart'] = {}
            session.modified = True

            flash(_('تم إرسال طلبكم بنجاح وهو في انتظار موافقة الإدارة'), 'success')
            return redirect(url_for('core.order_confirmation', order_number=order.order_number))

        except Exception as e:
            db.session.rollback()
            flash(_('حدث خطأ أثناء معالجة الطلب'), 'error')
            return render_template('core/checkout.html',
                                 available_tables=available_tables,
                                 cart_total=calculate_cart_total(cart),
                                 cart_count=get_cart_count())

    return render_template('core/checkout.html',
                         available_tables=available_tables,
                         cart_total=calculate_cart_total(cart),
                         cart_count=get_cart_count())


@bp.route('/order-confirmation/<order_number>')
def order_confirmation(order_number):
    """صفحة تأكيد الطلب - Order confirmation page"""
    order = Order.query.filter_by(order_number=order_number).first_or_404()
    return render_template('core/order_confirmation.html', order=order)
