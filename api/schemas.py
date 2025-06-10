# -*- coding: utf-8 -*-
"""
مخططات API - API Schemas
"""
from marshmallow import Schema, fields, post_load
from models import Category, SubCategory, Product


class CategorySchema(Schema):
    """مخطط الفئة - Category schema"""
    id = fields.Int(dump_only=True)
    name = fields.Method('get_localized_name')
    description = fields.Method('get_localized_description')
    icon = fields.Str()
    sort_order = fields.Int()
    subcategories = fields.Nested('SubCategorySchema', many=True, exclude=['category'])
    products = fields.Nested('ProductSchema', many=True, exclude=['category'])
    
    def get_localized_name(self, obj):
        """الحصول على الاسم المترجم - Get localized name"""
        lang = self.context.get('lang', 'ar')
        return obj.get_name(lang)
    
    def get_localized_description(self, obj):
        """الحصول على الوصف المترجم - Get localized description"""
        lang = self.context.get('lang', 'ar')
        return obj.get_description(lang)


class SubCategorySchema(Schema):
    """مخطط الفئة الفرعية - Subcategory schema"""
    id = fields.Int(dump_only=True)
    category_id = fields.Int()
    name = fields.Method('get_localized_name')
    description = fields.Method('get_localized_description')
    sort_order = fields.Int()
    products = fields.Nested('ProductSchema', many=True, exclude=['subcategory'])
    
    def get_localized_name(self, obj):
        """الحصول على الاسم المترجم - Get localized name"""
        lang = self.context.get('lang', 'ar')
        return obj.get_name(lang)
    
    def get_localized_description(self, obj):
        """الحصول على الوصف المترجم - Get localized description"""
        lang = self.context.get('lang', 'ar')
        return obj.get_description(lang)


class ProductSchema(Schema):
    """مخطط المنتج - Product schema"""
    id = fields.Int(dump_only=True)
    category_id = fields.Int()
    subcategory_id = fields.Int(allow_none=True)
    name = fields.Method('get_localized_name')
    description = fields.Method('get_localized_description')
    ingredients = fields.Method('get_localized_ingredients')
    price = fields.Decimal(places=2)
    currency = fields.Str()
    formatted_price = fields.Method('get_formatted_price')
    photo_b64 = fields.Str()
    sort_order = fields.Int()
    is_featured = fields.Bool()
    category = fields.Nested(CategorySchema, exclude=['products', 'subcategories'])
    subcategory = fields.Nested(SubCategorySchema, exclude=['products'])
    
    def get_localized_name(self, obj):
        """الحصول على الاسم المترجم - Get localized name"""
        lang = self.context.get('lang', 'ar')
        return obj.get_name(lang)
    
    def get_localized_description(self, obj):
        """الحصول على الوصف المترجم - Get localized description"""
        lang = self.context.get('lang', 'ar')
        return obj.get_description(lang)
    
    def get_localized_ingredients(self, obj):
        """الحصول على المكونات المترجمة - Get localized ingredients"""
        lang = self.context.get('lang', 'ar')
        return obj.get_ingredients(lang)
    
    def get_formatted_price(self, obj):
        """الحصول على السعر منسق - Get formatted price"""
        return obj.get_formatted_price()


class SettingsSchema(Schema):
    """مخطط الإعدادات - Settings schema"""
    shop_name = fields.Str()
    primary_color = fields.Str()
    secondary_color = fields.Str()
    logo_b64 = fields.Str()
    default_currency = fields.Str()
    default_lang = fields.Str()


# إنشاء مثيلات المخططات - Create schema instances
category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)
subcategory_schema = SubCategorySchema()
subcategories_schema = SubCategorySchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)
settings_schema = SettingsSchema()
