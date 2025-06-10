# -*- coding: utf-8 -*-
"""
مسارات الإدارة - Admin Routes
"""
import base64
from io import BytesIO
from PIL import Image
from flask import render_template, redirect, url_for, flash, request, current_app, session
from flask_login import login_user, logout_user, login_required, current_user
from i18n import _
from admin import bp
from admin.forms import LoginForm, SettingsForm, CategoryForm, SubCategoryForm, ProductForm, ContentPageForm
from models import User, Settings, Category, SubCategory, Product, ContentPage
from extensions import db


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """تسجيل دخول الإدارة - Admin login"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash(_('مرحباً بك في لوحة التحكم'), 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('admin.dashboard'))
        flash(_('اسم المستخدم أو كلمة المرور غير صحيحة'), 'error')
    
    return render_template('admin/login.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    """تسجيل خروج الإدارة - Admin logout"""
    logout_user()
    flash(_('تم تسجيل الخروج بنجاح'), 'info')
    return redirect(url_for('core.index'))


@bp.route('/')
@login_required
def index():
    """الصفحة الرئيسية للإدارة - Admin home page"""
    return redirect(url_for('admin.dashboard'))


@bp.route('/dashboard')
@login_required
def dashboard():
    """لوحة التحكم الرئيسية - Main dashboard"""
    # إحصائيات سريعة - Quick stats
    stats = {
        'categories_count': Category.query.filter_by(is_active=True).count(),
        'subcategories_count': SubCategory.query.filter_by(is_active=True).count(),
        'products_count': Product.query.filter_by(is_active=True).count(),
        'featured_products_count': Product.query.filter_by(is_active=True, is_featured=True).count()
    }
    
    # أحدث المنتجات - Latest products
    latest_products = Product.query.order_by(Product.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', stats=stats, latest_products=latest_products)


@bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    """إعدادات المتجر - Shop settings"""
    settings_obj = Settings.get_settings()
    form = SettingsForm(obj=settings_obj)
    
    if form.validate_on_submit():
        settings_obj.shop_name = form.shop_name.data
        settings_obj.primary_color = form.primary_color.data
        settings_obj.secondary_color = form.secondary_color.data
        settings_obj.default_currency = form.default_currency.data
        settings_obj.default_lang = form.default_lang.data

        # روابط التواصل الاجتماعي - Social media links
        settings_obj.facebook_url = form.facebook_url.data
        settings_obj.twitter_url = form.twitter_url.data
        settings_obj.instagram_url = form.instagram_url.data
        settings_obj.whatsapp_url = form.whatsapp_url.data

        # معالجة رفع الشعار - Handle logo upload
        if form.logo.data:
            logo_b64 = process_image_upload(form.logo.data)
            if logo_b64:
                settings_obj.logo_b64 = logo_b64

        db.session.commit()
        flash(_('تم حفظ الإعدادات بنجاح'), 'success')
        return redirect(url_for('admin.settings'))
    
    return render_template('admin/settings.html', form=form, settings=settings_obj)


def process_image_upload(file):
    """معالجة رفع الصور وتحويلها إلى Base64 - Process image upload and convert to Base64"""
    try:
        # التحقق من حجم الملف - Check file size
        if len(file.read()) > current_app.config['MAX_CONTENT_LENGTH']:
            flash(_('حجم الملف كبير جداً (الحد الأقصى 1 ميجابايت)'), 'error')
            return None
        
        file.seek(0)  # إعادة تعيين مؤشر الملف - Reset file pointer
        
        # فتح الصورة وتحسينها - Open and optimize image
        image = Image.open(file)
        
        # تحويل إلى RGB إذا لزم الأمر - Convert to RGB if needed
        if image.mode in ('RGBA', 'P'):
            image = image.convert('RGB')
        
        # تغيير حجم الصورة إذا كانت كبيرة - Resize if too large
        max_size = (800, 600)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # حفظ في buffer - Save to buffer
        buffer = BytesIO()
        image.save(buffer, format='JPEG', quality=85, optimize=True)
        buffer.seek(0)
        
        # تحويل إلى Base64 - Convert to Base64
        image_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{image_b64}"
        
    except Exception as e:
        flash(_('خطأ في معالجة الصورة: {}').format(str(e)), 'error')
        return None


# مسارات الفئات - Category routes
@bp.route('/categories')
@login_required
def categories():
    """قائمة الفئات - Categories list"""
    categories = Category.query.order_by(Category.sort_order).all()
    return render_template('admin/categories.html', categories=categories)


@bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    """إضافة فئة جديدة - Add new category"""
    form = CategoryForm()
    
    if form.validate_on_submit():
        try:
            # تحويل sort_order إلى integer - Convert sort_order to integer
            sort_order_value = 0
            if form.sort_order.data:
                if hasattr(form.sort_order.data, '__int__'):
                    sort_order_value = int(form.sort_order.data)
                else:
                    sort_order_value = int(float(str(form.sort_order.data)))

            category = Category(
                name_ar=form.name_ar.data,
                name_en=form.name_en.data,
                description_ar=form.description_ar.data or '',
                description_en=form.description_en.data or '',
                icon=form.icon.data or '',
                sort_order=sort_order_value,
                is_active=form.is_active.data
            )
            db.session.add(category)
            db.session.commit()
            flash(_('تم إضافة الفئة بنجاح'), 'success')
            return redirect(url_for('admin.categories'))
        except Exception as e:
            db.session.rollback()
            flash(f'خطأ في إضافة الفئة: {str(e)}', 'error')
            print(f"Error adding category: {e}")  # للتصحيح - For debugging
    
    return render_template('admin/category_form.html', form=form, title=_('إضافة فئة جديدة'))


@bp.route('/categories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    """تعديل فئة - Edit category"""
    category = Category.query.get_or_404(id)
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.commit()
        flash(_('تم تحديث الفئة بنجاح'), 'success')
        return redirect(url_for('admin.categories'))
    
    return render_template('admin/category_form.html', form=form, category=category, title=_('تعديل الفئة'))


@bp.route('/categories/<int:id>/delete', methods=['POST'])
@login_required
def delete_category(id):
    """حذف فئة - Delete category"""
    category = Category.query.get_or_404(id)

    # التحقق من وجود منتجات في هذه الفئة - Check if category has products
    if category.products:
        flash(_('لا يمكن حذف فئة تحتوي على منتجات'), 'error')
        return redirect(url_for('admin.categories'))

    db.session.delete(category)
    db.session.commit()
    flash(_('تم حذف الفئة بنجاح'), 'success')
    return redirect(url_for('admin.categories'))


# مسارات الفئات الفرعية - Subcategory routes
@bp.route('/subcategories')
@login_required
def subcategories():
    """قائمة الفئات الفرعية - Subcategories list"""
    subcategories = SubCategory.query.join(Category).order_by(Category.sort_order, SubCategory.sort_order).all()
    return render_template('admin/subcategories.html', subcategories=subcategories)


@bp.route('/subcategories/add', methods=['GET', 'POST'])
@login_required
def add_subcategory():
    """إضافة فئة فرعية جديدة - Add new subcategory"""
    form = SubCategoryForm()

    # تحديث خيارات الفئات - Update category choices
    form.category_id.choices = [(c.id, c.get_name(session.get('lang', 'ar')))
                                for c in Category.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        subcategory = SubCategory(
            category_id=form.category_id.data,
            name_ar=form.name_ar.data,
            name_en=form.name_en.data,
            description_ar=form.description_ar.data,
            description_en=form.description_en.data,
            sort_order=form.sort_order.data,
            is_active=form.is_active.data
        )
        db.session.add(subcategory)
        db.session.commit()
        flash(_('تم إضافة الفئة الفرعية بنجاح'), 'success')
        return redirect(url_for('admin.subcategories'))

    return render_template('admin/subcategory_form.html', form=form, title=_('إضافة فئة فرعية جديدة'))


@bp.route('/subcategories/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_subcategory(id):
    """تعديل فئة فرعية - Edit subcategory"""
    subcategory = SubCategory.query.get_or_404(id)
    form = SubCategoryForm(obj=subcategory)

    # تحديث خيارات الفئات - Update category choices
    form.category_id.choices = [(c.id, c.get_name(session.get('lang', 'ar')))
                                for c in Category.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        form.populate_obj(subcategory)
        db.session.commit()
        flash(_('تم تحديث الفئة الفرعية بنجاح'), 'success')
        return redirect(url_for('admin.subcategories'))

    return render_template('admin/subcategory_form.html', form=form, subcategory=subcategory, title=_('تعديل الفئة الفرعية'))


@bp.route('/subcategories/<int:id>/delete', methods=['POST'])
@login_required
def delete_subcategory(id):
    """حذف فئة فرعية - Delete subcategory"""
    subcategory = SubCategory.query.get_or_404(id)

    # التحقق من وجود منتجات في هذه الفئة الفرعية - Check if subcategory has products
    if subcategory.products:
        flash(_('لا يمكن حذف فئة فرعية تحتوي على منتجات'), 'error')
        return redirect(url_for('admin.subcategories'))

    db.session.delete(subcategory)
    db.session.commit()
    flash(_('تم حذف الفئة الفرعية بنجاح'), 'success')
    return redirect(url_for('admin.subcategories'))


# مسارات المنتجات - Product routes
@bp.route('/products')
@login_required
def products():
    """قائمة المنتجات - Products list"""
    page = request.args.get('page', 1, type=int)
    products = Product.query.join(Category).order_by(Category.sort_order, Product.sort_order)\
                           .paginate(page=page, per_page=20, error_out=False)
    return render_template('admin/products.html', products=products)


@bp.route('/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    """إضافة منتج جديد - Add new product"""
    form = ProductForm()

    # تحديث خيارات الفئات والفئات الفرعية - Update category and subcategory choices
    categories = Category.query.filter_by(is_active=True).all()
    form.category_id.choices = [(c.id, c.get_name(session.get('lang', 'ar'))) for c in categories]
    form.subcategory_id.choices = [(0, _('بدون فئة فرعية'))] + \
                                  [(s.id, s.get_name(session.get('lang', 'ar')))
                                   for s in SubCategory.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        product = Product(
            category_id=form.category_id.data,
            subcategory_id=form.subcategory_id.data if form.subcategory_id.data != 0 else None,
            name_ar=form.name_ar.data,
            name_en=form.name_en.data,
            description_ar=form.description_ar.data,
            description_en=form.description_en.data,
            ingredients_ar=form.ingredients_ar.data,
            ingredients_en=form.ingredients_en.data,
            price=form.price.data,
            currency=form.currency.data,
            sort_order=form.sort_order.data,
            is_active=form.is_active.data,
            is_featured=form.is_featured.data
        )

        # معالجة رفع الصورة - Handle image upload
        if form.photo.data:
            photo_b64 = process_image_upload(form.photo.data)
            if photo_b64:
                product.photo_b64 = photo_b64

        db.session.add(product)
        db.session.commit()
        flash(_('تم إضافة المنتج بنجاح'), 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, title=_('إضافة منتج جديد'))


@bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    """تعديل منتج - Edit product"""
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)

    # تحديث خيارات الفئات والفئات الفرعية - Update category and subcategory choices
    categories = Category.query.filter_by(is_active=True).all()
    form.category_id.choices = [(c.id, c.get_name(session.get('lang', 'ar'))) for c in categories]
    form.subcategory_id.choices = [(0, _('بدون فئة فرعية'))] + \
                                  [(s.id, s.get_name(session.get('lang', 'ar')))
                                   for s in SubCategory.query.filter_by(is_active=True).all()]

    if form.validate_on_submit():
        form.populate_obj(product)

        # تعيين الفئة الفرعية - Set subcategory
        if form.subcategory_id.data == 0:
            product.subcategory_id = None

        # معالجة رفع الصورة - Handle image upload
        if form.photo.data:
            photo_b64 = process_image_upload(form.photo.data)
            if photo_b64:
                product.photo_b64 = photo_b64

        db.session.commit()
        flash(_('تم تحديث المنتج بنجاح'), 'success')
        return redirect(url_for('admin.products'))

    return render_template('admin/product_form.html', form=form, product=product, title=_('تعديل المنتج'))


@bp.route('/products/<int:id>/delete', methods=['POST'])
@login_required
def delete_product(id):
    """حذف منتج - Delete product"""
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash(_('تم حذف المنتج بنجاح'), 'success')
    return redirect(url_for('admin.products'))


# مسارات صفحات المحتوى - Content pages routes
@bp.route('/content-pages')
@login_required
def content_pages():
    """قائمة صفحات المحتوى - Content pages list"""
    pages = ContentPage.query.all()
    return render_template('admin/content_pages.html', pages=pages)


@bp.route('/content-pages/<page_key>/edit', methods=['GET', 'POST'])
@login_required
def edit_content_page(page_key):
    """تعديل صفحة محتوى - Edit content page"""
    # إنشاء الصفحة إذا لم تكن موجودة - Create page if it doesn't exist
    if page_key == 'about':
        page = ContentPage.get_or_create_page(
            'about',
            'حول المتجر',
            'About Us',
            'مرحباً بكم في متجرنا. نحن نقدم أفضل الأطعمة والمشروبات في المدينة.',
            'Welcome to our store. We offer the best food and drinks in the city.'
        )
    elif page_key == 'contact':
        page = ContentPage.get_or_create_page(
            'contact',
            'اتصل بنا',
            'Contact Us',
            'يمكنكم التواصل معنا عبر الطرق التالية:\n\nالهاتف: +20 123 456 789\nالبريد الإلكتروني: info@shop.com\nالعنوان: القاهرة، مصر',
            'You can contact us through the following methods:\n\nPhone: +20 123 456 789\nEmail: info@shop.com\nAddress: Cairo, Egypt'
        )
    elif page_key == 'footer':
        page = ContentPage.get_or_create_page(
            'footer',
            'تذييل الموقع',
            'Website Footer',
            'أفضل الأطعمة والمشروبات في المدينة\n\nالهاتف: +20 123 456 789\nالبريد الإلكتروني: info@shop.com\nالعنوان: القاهرة، مصر',
            'Best food and drinks in the city\n\nPhone: +20 123 456 789\nEmail: info@shop.com\nAddress: Cairo, Egypt'
        )
    else:
        flash(_('صفحة غير موجودة'), 'error')
        return redirect(url_for('admin.content_pages'))

    form = ContentPageForm(obj=page)

    if form.validate_on_submit():
        form.populate_obj(page)
        db.session.commit()
        flash(_('تم تحديث الصفحة بنجاح'), 'success')
        return redirect(url_for('admin.content_pages'))

    # تحديد عنوان الصفحة - Set page title
    page_titles = {
        'about': _('تعديل صفحة حول المتجر'),
        'contact': _('تعديل صفحة اتصل بنا'),
        'footer': _('تعديل تذييل الموقع')
    }

    return render_template('admin/content_page_form.html',
                         form=form,
                         page=page,
                         title=page_titles.get(page_key, _('تعديل صفحة المحتوى')))
