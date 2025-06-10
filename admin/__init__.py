# -*- coding: utf-8 -*-
"""
بلوبرينت الإدارة - Admin Blueprint
"""
from flask import Blueprint

bp = Blueprint('admin', __name__)

from admin import routes, forms
