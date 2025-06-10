# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات - Database Models
"""
from datetime import datetime
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db


class User(UserMixin, db.Model):
    """نموذج المستخدم - User model"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        """تشفير كلمة المرور - Hash password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """التحقق من كلمة المرور - Check password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Settings(db.Model):
    """إعدادات المتجر - Shop settings"""
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    shop_name = db.Column(db.String(200), nullable=False, default='متجري')
    primary_color = db.Column(db.String(7), default='#3B82F6')
    secondary_color = db.Column(db.String(7), default='#10B981')
    logo_b64 = db.Column(db.Text)  # Base64 encoded logo
    default_currency = db.Column(db.String(3), default='EGP')
    default_lang = db.Column(db.String(2), default='ar')

    # معلومات الاتصال - Contact information
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    tax_number = db.Column(db.String(50))  # الرقم الضريبي - Tax registration number

    # روابط التواصل الاجتماعي - Social media links
    facebook_url = db.Column(db.String(500))
    twitter_url = db.Column(db.String(500))
    instagram_url = db.Column(db.String(500))
    whatsapp_url = db.Column(db.String(500))

    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    @classmethod
    def get_settings(cls):
        """الحصول على الإعدادات أو إنشاء إعدادات افتراضية - Get settings or create default"""
        settings = cls.query.first()
        if not settings:
            settings = cls()
            db.session.add(settings)
            db.session.commit()
        return settings
    
    def __repr__(self):
        return f'<Settings {self.shop_name}>'


class Category(db.Model):
    """فئة المنتجات - Product category"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Font Awesome icon class
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات - Relationships
    subcategories = db.relationship('SubCategory', backref='category', lazy=True, cascade='all, delete-orphan')
    products = db.relationship('Product', backref='category', lazy=True)
    
    def get_name(self, lang='ar'):
        """الحصول على الاسم باللغة المحددة - Get name in specified language"""
        return getattr(self, f'name_{lang}', self.name_ar)
    
    def get_description(self, lang='ar'):
        """الحصول على الوصف باللغة المحددة - Get description in specified language"""
        return getattr(self, f'description_{lang}', self.description_ar)
    
    def __repr__(self):
        return f'<Category {self.name_ar}>'


class SubCategory(db.Model):
    """فئة فرعية - Subcategory"""
    __tablename__ = 'subcategories'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # العلاقات - Relationships
    products = db.relationship('Product', backref='subcategory', lazy=True)
    
    def get_name(self, lang='ar'):
        """الحصول على الاسم باللغة المحددة - Get name in specified language"""
        return getattr(self, f'name_{lang}', self.name_ar)
    
    def get_description(self, lang='ar'):
        """الحصول على الوصف باللغة المحددة - Get description in specified language"""
        return getattr(self, f'description_{lang}', self.description_ar)
    
    def __repr__(self):
        return f'<SubCategory {self.name_ar}>'


class Product(db.Model):
    """منتج - Product"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategories.id'))
    name_ar = db.Column(db.String(200), nullable=False)
    name_en = db.Column(db.String(200), nullable=False)
    description_ar = db.Column(db.Text)
    description_en = db.Column(db.Text)
    ingredients_ar = db.Column(db.Text)
    ingredients_en = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='EGP')
    photo_b64 = db.Column(db.Text)  # Base64 encoded image
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_name(self, lang='ar'):
        """الحصول على الاسم باللغة المحددة - Get name in specified language"""
        return getattr(self, f'name_{lang}', self.name_ar)
    
    def get_description(self, lang='ar'):
        """الحصول على الوصف باللغة المحددة - Get description in specified language"""
        return getattr(self, f'description_{lang}', self.description_ar)
    
    def get_ingredients(self, lang='ar'):
        """الحصول على المكونات باللغة المحددة - Get ingredients in specified language"""
        return getattr(self, f'ingredients_{lang}', self.ingredients_ar)
    
    def get_formatted_price(self):
        """الحصول على السعر منسق - Get formatted price"""
        return f"{self.price} {self.currency}"
    
    def __repr__(self):
        return f'<Product {self.name_ar}>'


class Translation(db.Model):
    """ترجمات تلقائية - Auto translations cache"""
    __tablename__ = 'translations'

    id = db.Column(db.Integer, primary_key=True)
    text_key = db.Column(db.String(255), nullable=False)
    source_lang = db.Column(db.String(2), nullable=False)
    target_lang = db.Column(db.String(2), nullable=False)
    source_text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('text_key', 'source_lang', 'target_lang'),
    )


class ContentPage(db.Model):
    """صفحات المحتوى القابلة للتحرير - Editable content pages"""
    __tablename__ = 'content_pages'

    id = db.Column(db.Integer, primary_key=True)
    page_key = db.Column(db.String(50), unique=True, nullable=False)  # about, contact, footer
    title_ar = db.Column(db.String(200), nullable=False)
    title_en = db.Column(db.String(200), nullable=False)
    content_ar = db.Column(db.Text, nullable=False)
    content_en = db.Column(db.Text, nullable=False)
    meta_description_ar = db.Column(db.Text)
    meta_description_en = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def get_title(self, lang='ar'):
        """الحصول على العنوان حسب اللغة - Get title by language"""
        return getattr(self, f'title_{lang}', self.title_ar)

    def get_content(self, lang='ar'):
        """الحصول على المحتوى حسب اللغة - Get content by language"""
        return getattr(self, f'content_{lang}', self.content_ar)

    def get_meta_description(self, lang='ar'):
        """الحصول على وصف الميتا حسب اللغة - Get meta description by language"""
        return getattr(self, f'meta_description_{lang}', self.meta_description_ar)

    @staticmethod
    def get_page(page_key):
        """الحصول على صفحة بالمفتاح - Get page by key"""
        return ContentPage.query.filter_by(page_key=page_key, is_active=True).first()

    @staticmethod
    def get_or_create_page(page_key, default_title_ar, default_title_en, default_content_ar, default_content_en):
        """الحصول على صفحة أو إنشاؤها - Get or create page"""
        page = ContentPage.query.filter_by(page_key=page_key).first()
        if not page:
            page = ContentPage(
                page_key=page_key,
                title_ar=default_title_ar,
                title_en=default_title_en,
                content_ar=default_content_ar,
                content_en=default_content_en
            )
            db.session.add(page)
            db.session.commit()
        return page

    def __repr__(self):
        return f'<ContentPage {self.page_key}>'
    
    def __repr__(self):
        return f'<Translation {self.text_key} {self.source_lang}->{self.target_lang}>'


class RestaurantTable(db.Model):
    """طاولات المطعم - Restaurant tables"""
    __tablename__ = 'restaurant_tables'

    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, default=4)  # عدد الأشخاص - Number of people
    status = db.Column(db.String(20), default='available')  # available, occupied, reserved
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات - Relationships
    orders = db.relationship('Order', backref='table', lazy=True)

    def get_status_color(self):
        """الحصول على لون الحالة - Get status color"""
        status_colors = {
            'available': 'green',
            'occupied': 'red',
            'reserved': 'yellow',
            'order_placed': 'yellow'
        }
        return status_colors.get(self.status, 'gray')

    def get_status_text(self, lang='ar'):
        """الحصول على نص الحالة - Get status text"""
        if lang == 'ar':
            status_texts = {
                'available': 'متاحة',
                'occupied': 'مشغولة',
                'reserved': 'محجوزة',
                'order_placed': 'طلب في الانتظار'
            }
        else:
            status_texts = {
                'available': 'Available',
                'occupied': 'Occupied',
                'reserved': 'Reserved',
                'order_placed': 'Order Placed'
            }
        return status_texts.get(self.status, 'Unknown')

    def __repr__(self):
        return f'<RestaurantTable {self.table_number}>'


class Order(db.Model):
    """طلبات العملاء - Customer orders"""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)

    # معلومات العميل - Customer information
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)

    # معلومات الطاولة - Table information
    table_id = db.Column(db.Integer, db.ForeignKey('restaurant_tables.id'), nullable=False)

    # معلومات الطلب - Order information
    status = db.Column(db.String(20), default='pending')  # pending, preparing, ready, served, completed, cancelled
    payment_status = db.Column(db.String(20), default='unpaid')  # unpaid, paid, refunded, partial
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    currency = db.Column(db.String(3), default='EGP')

    # التواريخ - Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    # ملاحظات - Notes
    notes = db.Column(db.Text)

    # العلاقات - Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    payments = db.relationship('Payment', backref='order', lazy=True, cascade='all, delete-orphan')
    invoices = db.relationship('Invoice', backref='order', lazy=True, cascade='all, delete-orphan')

    def generate_order_number(self):
        """توليد رقم طلب فريد - Generate unique order number"""
        import random
        import string
        while True:
            # تنسيق: ORD + 6 أرقام عشوائية - Format: ORD + 6 random digits
            number = 'ORD' + ''.join(random.choices(string.digits, k=6))
            if not Order.query.filter_by(order_number=number).first():
                return number

    def get_status_color(self):
        """الحصول على لون الحالة - Get status color"""
        status_colors = {
            'pending': 'yellow',
            'preparing': 'blue',
            'ready': 'green',
            'served': 'purple',
            'completed': 'gray',
            'cancelled': 'red'
        }
        return status_colors.get(self.status, 'gray')

    def get_status_text(self, lang='ar'):
        """الحصول على نص الحالة - Get status text"""
        if lang == 'ar':
            status_texts = {
                'pending': 'في انتظار موافقة الإدارة',
                'preparing': 'قيد التحضير',
                'ready': 'جاهز للتقديم',
                'served': 'تم التقديم',
                'completed': 'مكتمل',
                'cancelled': 'ملغي'
            }
        else:
            status_texts = {
                'pending': 'Pending Admin Approval',
                'preparing': 'Preparing',
                'ready': 'Ready',
                'served': 'Served',
                'completed': 'Completed',
                'cancelled': 'Cancelled'
            }
        return status_texts.get(self.status, 'Unknown')

    def get_formatted_total(self):
        """الحصول على المجموع منسق - Get formatted total"""
        return f"{self.total_amount} {self.currency}"

    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    """عناصر الطلب - Order items"""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    quantity = db.Column(db.Integer, nullable=False, default=1)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)

    # ملاحظات خاصة بالعنصر - Item-specific notes
    notes = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات - Relationships
    product = db.relationship('Product', backref='order_items', lazy=True)

    def calculate_total(self):
        """حساب المجموع - Calculate total"""
        self.total_price = self.unit_price * self.quantity
        return self.total_price

    def get_formatted_unit_price(self):
        """الحصول على سعر الوحدة منسق - Get formatted unit price"""
        return f"{self.unit_price} {self.order.currency}"

    def get_formatted_total_price(self):
        """الحصول على السعر الإجمالي منسق - Get formatted total price"""
        return f"{self.total_price} {self.order.currency}"

    def __repr__(self):
        return f'<OrderItem {self.product.name_ar} x{self.quantity}>'


class Payment(db.Model):
    """مدفوعات الطلبات - Order payments"""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    payment_number = db.Column(db.String(20), unique=True, nullable=False)

    # معلومات الطلب - Order information
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    # معلومات الدفع - Payment information
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(20), nullable=False)  # cash, credit_card, debit_card, bank_transfer, smart_wallet, instapay
    payment_status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded

    # معلومات المعالجة - Processing information
    processed_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    payment_timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # معلومات إضافية - Additional information
    reference_number = db.Column(db.String(100))  # للمرجع الخارجي - For external reference
    notes = db.Column(db.Text)

    # التواريخ - Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات - Relationships
    processed_by = db.relationship('User', backref='processed_payments', lazy=True)

    def generate_payment_number(self):
        """توليد رقم دفع فريد - Generate unique payment number"""
        import random
        import string
        while True:
            # تنسيق: PAY + 6 أرقام عشوائية - Format: PAY + 6 random digits
            number = 'PAY' + ''.join(random.choices(string.digits, k=6))
            if not Payment.query.filter_by(payment_number=number).first():
                return number

    def get_payment_method_text(self, lang='ar'):
        """الحصول على نص طريقة الدفع - Get payment method text"""
        methods = {
            'cash': {'ar': 'نقداً', 'en': 'Cash'},
            'credit_card': {'ar': 'بطاقة ائتمان', 'en': 'Credit Card'},
            'debit_card': {'ar': 'بطاقة خصم', 'en': 'Debit Card'},
            'bank_transfer': {'ar': 'تحويل بنكي', 'en': 'Bank Transfer'},
            'smart_wallet': {'ar': 'محفظة ذكية', 'en': 'Smart Wallet'},
            'instapay': {'ar': 'إنستاباي', 'en': 'InstaPay'}
        }
        return methods.get(self.payment_method, {}).get(lang, self.payment_method)

    def get_status_text(self, lang='ar'):
        """الحصول على نص حالة الدفع - Get payment status text"""
        statuses = {
            'pending': {'ar': 'في الانتظار', 'en': 'Pending'},
            'completed': {'ar': 'مكتمل', 'en': 'Completed'},
            'failed': {'ar': 'فشل', 'en': 'Failed'},
            'refunded': {'ar': 'مسترد', 'en': 'Refunded'}
        }
        return statuses.get(self.payment_status, {}).get(lang, self.payment_status)

    def get_status_color(self):
        """الحصول على لون حالة الدفع - Get payment status color"""
        colors = {
            'pending': 'yellow',
            'completed': 'green',
            'failed': 'red',
            'refunded': 'blue'
        }
        return colors.get(self.payment_status, 'gray')

    def get_formatted_amount(self):
        """الحصول على المبلغ منسق - Get formatted amount"""
        return f"{self.amount} {self.order.currency}"

    def __repr__(self):
        return f'<Payment {self.payment_number} - {self.amount}>'


class Invoice(db.Model):
    """فواتير الطلبات - Order invoices"""
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(20), unique=True, nullable=False)

    # معلومات الطلب - Order information
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)

    # معلومات الفاتورة - Invoice information
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    tax_rate = db.Column(db.Numeric(5, 2), default=0)  # نسبة الضريبة - Tax rate percentage
    tax_amount = db.Column(db.Numeric(10, 2), default=0)  # مبلغ الضريبة - Tax amount
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)

    # معلومات الإنشاء - Creation information
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    invoice_date = db.Column(db.DateTime, default=datetime.utcnow)

    # ملاحظات - Notes
    notes = db.Column(db.Text)

    # التواريخ - Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات - Relationships
    created_by = db.relationship('User', backref='created_invoices', lazy=True)

    def generate_invoice_number(self):
        """توليد رقم فاتورة فريد - Generate unique invoice number"""
        import random
        import string
        while True:
            # تنسيق: INV + 6 أرقام عشوائية - Format: INV + 6 random digits
            number = 'INV' + ''.join(random.choices(string.digits, k=6))
            if not Invoice.query.filter_by(invoice_number=number).first():
                return number

    def calculate_totals(self, order=None):
        """حساب المجاميع - Calculate totals"""
        # استخدام الطلب المرسل أو الطلب المرتبط - Use passed order or linked order
        order_obj = order or self.order
        if not order_obj:
            raise ValueError("لا يمكن حساب المجاميع بدون طلب - Cannot calculate totals without an order")

        self.subtotal = order_obj.total_amount
        self.tax_amount = (self.subtotal * self.tax_rate) / 100 if self.tax_rate else 0
        self.total_amount = self.subtotal + self.tax_amount

    def get_formatted_subtotal(self):
        """الحصول على المجموع الفرعي منسق - Get formatted subtotal"""
        return f"{self.subtotal} {self.order.currency}"

    def get_formatted_tax_amount(self):
        """الحصول على مبلغ الضريبة منسق - Get formatted tax amount"""
        return f"{self.tax_amount} {self.order.currency}"

    def get_formatted_total(self):
        """الحصول على المجموع الكلي منسق - Get formatted total"""
        return f"{self.total_amount} {self.order.currency}"

    def __repr__(self):
        return f'<Invoice {self.invoice_number} - {self.total_amount}>'


class CashDrawer(db.Model):
    """خزنة النقد - Cash drawer"""
    __tablename__ = 'cash_drawers'

    id = db.Column(db.Integer, primary_key=True)

    # معلومات الخزنة - Drawer information
    current_balance = db.Column(db.Numeric(10, 2), default=0)
    currency = db.Column(db.String(3), default='EGP')

    # آخر تحديث - Last update
    last_updated_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    last_updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # التواريخ - Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات - Relationships
    last_updated_by = db.relationship('User', backref='cash_drawer_updates', lazy=True)
    transactions = db.relationship('CashTransaction', backref='cash_drawer', lazy=True, cascade='all, delete-orphan')
    shifts = db.relationship('Shift', backref='cash_drawer', lazy=True)

    def get_formatted_balance(self):
        """الحصول على الرصيد منسق - Get formatted balance"""
        return f"{self.current_balance} {self.currency}"

    def add_transaction(self, amount, transaction_type, description, user_id, reference_id=None):
        """إضافة معاملة نقدية - Add cash transaction"""
        transaction = CashTransaction(
            cash_drawer_id=self.id,
            amount=amount,
            transaction_type=transaction_type,
            description=description,
            user_id=user_id,
            reference_id=reference_id
        )

        # تحديث الرصيد - Update balance
        if transaction_type in ['sale', 'deposit']:
            self.current_balance += amount
        elif transaction_type in ['withdrawal', 'refund']:
            self.current_balance -= amount

        self.last_updated_by_user_id = user_id

        db.session.add(transaction)
        return transaction

    @classmethod
    def get_default_drawer(cls):
        """الحصول على الخزنة الافتراضية - Get default cash drawer"""
        drawer = cls.query.first()
        if not drawer:
            drawer = cls()
            db.session.add(drawer)
            db.session.commit()
        return drawer

    def __repr__(self):
        return f'<CashDrawer {self.current_balance} {self.currency}>'


class CashTransaction(db.Model):
    """معاملات النقد - Cash transactions"""
    __tablename__ = 'cash_transactions'

    id = db.Column(db.Integer, primary_key=True)

    # معلومات الخزنة - Drawer information
    cash_drawer_id = db.Column(db.Integer, db.ForeignKey('cash_drawers.id'), nullable=False)

    # معلومات المعاملة - Transaction information
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # sale, withdrawal, deposit, refund
    description = db.Column(db.String(200), nullable=False)

    # معلومات المرجع - Reference information
    reference_id = db.Column(db.Integer)  # معرف الطلب أو الدفع - Order or payment ID
    reference_type = db.Column(db.String(20))  # order, payment, manual

    # معلومات المستخدم - User information
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # التواريخ - Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات - Relationships
    user = db.relationship('User', backref='cash_transactions', lazy=True)

    def get_transaction_type_text(self, lang='ar'):
        """الحصول على نص نوع المعاملة - Get transaction type text"""
        types = {
            'sale': {'ar': 'بيع', 'en': 'Sale'},
            'withdrawal': {'ar': 'سحب', 'en': 'Withdrawal'},
            'deposit': {'ar': 'إيداع', 'en': 'Deposit'},
            'refund': {'ar': 'استرداد', 'en': 'Refund'}
        }
        return types.get(self.transaction_type, {}).get(lang, self.transaction_type)

    def get_formatted_amount(self):
        """الحصول على المبلغ منسق - Get formatted amount"""
        return f"{self.amount} {self.cash_drawer.currency}"

    def __repr__(self):
        return f'<CashTransaction {self.transaction_type} - {self.amount}>'


class Shift(db.Model):
    """وردية العمل - Work shift"""
    __tablename__ = 'shifts'

    id = db.Column(db.Integer, primary_key=True)
    shift_number = db.Column(db.String(20), unique=True, nullable=False)

    # معلومات المستخدم - User information
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # معلومات الخزنة - Cash drawer information
    cash_drawer_id = db.Column(db.Integer, db.ForeignKey('cash_drawers.id'), nullable=False)

    # معلومات الوردية - Shift information
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)

    # أرصدة النقد - Cash balances
    opening_balance = db.Column(db.Numeric(10, 2), nullable=False)
    closing_balance = db.Column(db.Numeric(10, 2))
    expected_balance = db.Column(db.Numeric(10, 2))
    variance = db.Column(db.Numeric(10, 2))  # الفرق بين المتوقع والفعلي - Difference between expected and actual

    # إحصائيات المبيعات - Sales statistics
    total_sales = db.Column(db.Numeric(10, 2), default=0)
    cash_sales = db.Column(db.Numeric(10, 2), default=0)
    card_sales = db.Column(db.Numeric(10, 2), default=0)
    other_sales = db.Column(db.Numeric(10, 2), default=0)

    # عدد المعاملات - Transaction counts
    total_orders = db.Column(db.Integer, default=0)
    total_payments = db.Column(db.Integer, default=0)

    # حالة الوردية - Shift status
    status = db.Column(db.String(20), default='active')  # active, closed

    # ملاحظات - Notes
    notes = db.Column(db.Text)

    # التواريخ - Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # العلاقات - Relationships
    user = db.relationship('User', backref='shifts', lazy=True)

    def generate_shift_number(self):
        """توليد رقم وردية فريد - Generate unique shift number"""
        import random
        import string
        while True:
            # تنسيق: SHF + 6 أرقام عشوائية - Format: SHF + 6 random digits
            number = 'SHF' + ''.join(random.choices(string.digits, k=6))
            if not Shift.query.filter_by(shift_number=number).first():
                return number

    def calculate_statistics(self):
        """حساب إحصائيات الوردية - Calculate shift statistics"""
        from sqlalchemy import func

        # حساب المبيعات حسب طريقة الدفع - Calculate sales by payment method
        payment_stats = db.session.query(
            Payment.payment_method,
            func.sum(Payment.amount).label('total')
        ).join(Order).filter(
            Payment.payment_timestamp >= self.start_time,
            Payment.payment_timestamp <= (self.end_time or datetime.utcnow()),
            Payment.payment_status == 'completed'
        ).group_by(Payment.payment_method).all()

        self.cash_sales = 0
        self.card_sales = 0
        self.other_sales = 0

        for method, total in payment_stats:
            if method == 'cash':
                self.cash_sales = total
            elif method in ['credit_card', 'debit_card']:
                self.card_sales += total
            else:
                self.other_sales += total

        self.total_sales = self.cash_sales + self.card_sales + self.other_sales

        # حساب عدد الطلبات والمدفوعات - Calculate order and payment counts
        self.total_orders = Order.query.filter(
            Order.created_at >= self.start_time,
            Order.created_at <= (self.end_time or datetime.utcnow())
        ).count()

        self.total_payments = Payment.query.filter(
            Payment.payment_timestamp >= self.start_time,
            Payment.payment_timestamp <= (self.end_time or datetime.utcnow()),
            Payment.payment_status == 'completed'
        ).count()

    def close_shift(self, closing_balance, notes=None):
        """إغلاق الوردية - Close shift"""
        self.end_time = datetime.utcnow()
        self.closing_balance = closing_balance
        self.expected_balance = self.opening_balance + self.cash_sales
        self.variance = self.closing_balance - self.expected_balance
        self.status = 'closed'
        if notes:
            self.notes = notes

        self.calculate_statistics()

    def get_duration(self):
        """الحصول على مدة الوردية - Get shift duration"""
        if self.end_time:
            duration = self.end_time - self.start_time
            hours = duration.total_seconds() / 3600
            return f"{hours:.1f} ساعة"
        else:
            duration = datetime.utcnow() - self.start_time
            hours = duration.total_seconds() / 3600
            return f"{hours:.1f} ساعة (نشطة)"

    def get_formatted_opening_balance(self):
        """الحصول على الرصيد الافتتاحي منسق - Get formatted opening balance"""
        return f"{self.opening_balance} {self.cash_drawer.currency}"

    def get_formatted_closing_balance(self):
        """الحصول على الرصيد الختامي منسق - Get formatted closing balance"""
        if self.closing_balance is not None:
            return f"{self.closing_balance} {self.cash_drawer.currency}"
        return "غير محدد"

    def get_formatted_total_sales(self):
        """الحصول على إجمالي المبيعات منسق - Get formatted total sales"""
        return f"{self.total_sales} {self.cash_drawer.currency}"

    def __repr__(self):
        return f'<Shift {self.shift_number} - {self.user.username}>'
