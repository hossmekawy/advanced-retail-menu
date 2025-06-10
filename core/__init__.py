# -*- coding: utf-8 -*-
"""
البلوبرينت الأساسي - Core Blueprint
"""
from flask import Blueprint

bp = Blueprint('core', __name__)

from core import routes
