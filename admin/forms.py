# -*- coding: utf-8 -*-
"""
نماذج الإدارة - Admin Forms
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, DecimalField, SelectField, BooleanField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length, Email, NumberRange, Optional, ValidationError

# Simple translation function for forms
def _l(text):
    return text


class LoginForm(FlaskForm):
    """نموذج تسجيل الدخول - Login form"""
    username = StringField(_l('اسم المستخدم'), validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField(_l('كلمة المرور'), validators=[DataRequired()])


class UserForm(FlaskForm):
    """نموذج المستخدم - User form"""
    username = StringField(_l('اسم المستخدم'), validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField(_l('البريد الإلكتروني'), validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField(_l('كلمة المرور'), validators=[Length(min=6)])
    confirm_password = PasswordField(_l('تأكيد كلمة المرور'))
    is_active = BooleanField(_l('نشط'), default=True)

    def validate_confirm_password(self, field):
        if self.password.data and field.data != self.password.data:
            raise ValidationError(_l('كلمات المرور غير متطابقة'))


class SettingsForm(FlaskForm):
    """نموذج إعدادات المتجر - Shop settings form"""
    shop_name = StringField(_l('اسم المتجر'), validators=[DataRequired(), Length(max=200)])
    primary_color = StringField(_l('اللون الأساسي'), validators=[DataRequired(), Length(min=7, max=7)])
    secondary_color = StringField(_l('اللون الثانوي'), validators=[DataRequired(), Length(min=7, max=7)])
    logo = FileField(_l('شعار المتجر'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], _l('الصور فقط!'))
    ])
    default_currency = SelectField(_l('العملة الافتراضية'), choices=[
        ('EGP', 'جنيه مصري'),
        ('USD', 'دولار أمريكي'),
        ('EUR', 'يورو'),
        ('SAR', 'ريال سعودي'),
        ('AED', 'درهم إماراتي')
    ])
    default_lang = SelectField(_l('اللغة الافتراضية'), choices=[
        ('ar', 'العربية'),
        ('en', 'English'),
        ('fr', 'Français'),
        ('es', 'Español')
    ])

    # معلومات الاتصال - Contact information
    phone = StringField(_l('رقم الهاتف'), validators=[Optional(), Length(max=20)])
    email = StringField(_l('البريد الإلكتروني'), validators=[Optional(), Email(), Length(max=120)])
    address = TextAreaField(_l('العنوان'), validators=[Optional()], render_kw={'rows': 3})
    tax_number = StringField(_l('الرقم الضريبي'), validators=[Optional(), Length(max=50)])

    # روابط التواصل الاجتماعي - Social media links
    facebook_url = StringField(_l('رابط فيسبوك'), validators=[Optional(), Length(max=500)])
    twitter_url = StringField(_l('رابط تويتر'), validators=[Optional(), Length(max=500)])
    instagram_url = StringField(_l('رابط إنستغرام'), validators=[Optional(), Length(max=500)])
    whatsapp_url = StringField(_l('رابط واتساب'), validators=[Optional(), Length(max=500)])


class CategoryForm(FlaskForm):
    """نموذج الفئة - Category form"""
    name_ar = StringField(_l('الاسم بالعربية'), validators=[DataRequired(), Length(max=100)])
    name_en = StringField(_l('الاسم بالإنجليزية'), validators=[DataRequired(), Length(max=100)])
    description_ar = TextAreaField(_l('الوصف بالعربية'))
    description_en = TextAreaField(_l('الوصف بالإنجليزية'))
    icon = StringField(_l('أيقونة Font Awesome'), validators=[Length(max=50)])
    sort_order = IntegerField(_l('ترتيب العرض'), validators=[NumberRange(min=0)], default=0)
    is_active = BooleanField(_l('نشط'), default=True)


class SubCategoryForm(FlaskForm):
    """نموذج الفئة الفرعية - Subcategory form"""
    category_id = SelectField(_l('الفئة الرئيسية'), coerce=int, validators=[DataRequired()])
    name_ar = StringField(_l('الاسم بالعربية'), validators=[DataRequired(), Length(max=100)])
    name_en = StringField(_l('الاسم بالإنجليزية'), validators=[DataRequired(), Length(max=100)])
    description_ar = TextAreaField(_l('الوصف بالعربية'))
    description_en = TextAreaField(_l('الوصف بالإنجليزية'))
    sort_order = IntegerField(_l('ترتيب العرض'), validators=[NumberRange(min=0)], default=0)
    is_active = BooleanField(_l('نشط'), default=True)


class ProductForm(FlaskForm):
    """نموذج المنتج - Product form"""
    category_id = SelectField(_l('الفئة الرئيسية'), coerce=int, validators=[DataRequired()])
    subcategory_id = SelectField(_l('الفئة الفرعية'), coerce=int, validators=[Optional()])
    name_ar = StringField(_l('الاسم بالعربية'), validators=[DataRequired(), Length(max=200)])
    name_en = StringField(_l('الاسم بالإنجليزية'), validators=[DataRequired(), Length(max=200)])
    description_ar = TextAreaField(_l('الوصف بالعربية'))
    description_en = TextAreaField(_l('الوصف بالإنجليزية'))
    ingredients_ar = TextAreaField(_l('المكونات بالعربية'))
    ingredients_en = TextAreaField(_l('المكونات بالإنجليزية'))
    price = DecimalField(_l('السعر'), validators=[DataRequired(), NumberRange(min=0)], places=2)
    currency = SelectField(_l('العملة'), choices=[
        ('EGP', 'جنيه مصري'),
        ('USD', 'دولار أمريكي'),
        ('EUR', 'يورو'),
        ('SAR', 'ريال سعودي'),
        ('AED', 'درهم إماراتي')
    ])
    photo = FileField(_l('صورة المنتج'), validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'webp'], _l('الصور فقط!'))
    ])
    sort_order = IntegerField(_l('ترتيب العرض'), validators=[NumberRange(min=0)], default=0)
    is_active = BooleanField(_l('نشط'), default=True)
    is_featured = BooleanField(_l('منتج مميز'), default=False)


class ContentPageForm(FlaskForm):
    """نموذج صفحة المحتوى - Content page form"""
    title_ar = StringField(_l('العنوان بالعربية'), validators=[DataRequired(), Length(max=200)])
    title_en = StringField(_l('العنوان بالإنجليزية'), validators=[DataRequired(), Length(max=200)])
    content_ar = TextAreaField(_l('المحتوى بالعربية'), validators=[DataRequired()],
                              render_kw={'rows': 10, 'class': 'form-control'})
    content_en = TextAreaField(_l('المحتوى بالإنجليزية'), validators=[DataRequired()],
                              render_kw={'rows': 10, 'class': 'form-control'})
    meta_description_ar = TextAreaField(_l('وصف الميتا بالعربية'),
                                       render_kw={'rows': 3, 'class': 'form-control'})
    meta_description_en = TextAreaField(_l('وصف الميتا بالإنجليزية'),
                                       render_kw={'rows': 3, 'class': 'form-control'})
    is_active = BooleanField(_l('نشط'), default=True)


class RestaurantTableForm(FlaskForm):
    """نموذج طاولة المطعم - Restaurant table form"""
    table_number = IntegerField(_l('رقم الطاولة'), validators=[DataRequired(), NumberRange(min=1)])
    capacity = IntegerField(_l('عدد الأشخاص'), validators=[DataRequired(), NumberRange(min=1, max=20)], default=4)
    status = SelectField(_l('الحالة'), choices=[
        ('available', 'متاحة'),
        ('occupied', 'مشغولة'),
        ('reserved', 'محجوزة'),
        ('order_placed', 'طلب في الانتظار')
    ], default='available')
    is_active = BooleanField(_l('نشط'), default=True)


class OrderForm(FlaskForm):
    """نموذج الطلب - Order form"""
    customer_name = StringField(_l('اسم العميل'), validators=[DataRequired(), Length(max=100)])
    customer_phone = StringField(_l('رقم الهاتف'), validators=[DataRequired(), Length(max=20)])
    table_id = SelectField(_l('الطاولة'), coerce=int, validators=[DataRequired()])
    status = SelectField(_l('حالة الطلب'), choices=[
        ('pending', 'في الانتظار'),
        ('preparing', 'قيد التحضير'),
        ('ready', 'جاهز للتقديم'),
        ('served', 'تم التقديم'),
        ('completed', 'مكتمل'),
        ('cancelled', 'ملغي')
    ], default='pending')
    notes = TextAreaField(_l('ملاحظات'), render_kw={'rows': 3})


class PaymentForm(FlaskForm):
    """نموذج الدفع - Payment form"""
    amount = DecimalField(_l('المبلغ'), validators=[DataRequired(), NumberRange(min=0)], places=2)
    payment_method = SelectField(_l('طريقة الدفع'), choices=[
        ('cash', 'نقداً'),
        ('credit_card', 'بطاقة ائتمان'),
        ('debit_card', 'بطاقة خصم'),
        ('bank_transfer', 'تحويل بنكي'),
        ('smart_wallet', 'محفظة ذكية'),
        ('instapay', 'إنستاباي')
    ], validators=[DataRequired()])
    reference_number = StringField(_l('رقم المرجع'), validators=[Optional(), Length(max=100)])
    notes = TextAreaField(_l('ملاحظات'), render_kw={'rows': 3})


class RefundForm(FlaskForm):
    """نموذج الاسترداد - Refund form"""
    amount = DecimalField(_l('مبلغ الاسترداد'), validators=[DataRequired(), NumberRange(min=0)], places=2)
    reason = TextAreaField(_l('سبب الاسترداد'), validators=[DataRequired()], render_kw={'rows': 3})


class InvoiceForm(FlaskForm):
    """نموذج الفاتورة - Invoice form"""
    tax_rate = DecimalField(_l('نسبة الضريبة (%)'), validators=[Optional(), NumberRange(min=0, max=100)], places=2, default=0)
    notes = TextAreaField(_l('ملاحظات'), render_kw={'rows': 3})


class CashTransactionForm(FlaskForm):
    """نموذج معاملة نقدية - Cash transaction form"""
    amount = DecimalField(_l('المبلغ'), validators=[DataRequired(), NumberRange(min=0)], places=2)
    transaction_type = SelectField(_l('نوع المعاملة'), choices=[
        ('deposit', 'إيداع'),
        ('withdrawal', 'سحب')
    ], validators=[DataRequired()])
    description = StringField(_l('الوصف'), validators=[DataRequired(), Length(max=200)])
    notes = TextAreaField(_l('ملاحظات'), render_kw={'rows': 3})


class ShiftForm(FlaskForm):
    """نموذج الوردية - Shift form"""
    opening_balance = DecimalField(_l('الرصيد الافتتاحي'), validators=[DataRequired(), NumberRange(min=0)], places=2)
    notes = TextAreaField(_l('ملاحظات'), render_kw={'rows': 3})


class CloseShiftForm(FlaskForm):
    """نموذج إغلاق الوردية - Close shift form"""
    closing_balance = DecimalField(_l('الرصيد الختامي'), validators=[DataRequired(), NumberRange(min=0)], places=2)
    notes = TextAreaField(_l('ملاحظات الإغلاق'), render_kw={'rows': 3})
