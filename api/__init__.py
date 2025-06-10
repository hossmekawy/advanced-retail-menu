# -*- coding: utf-8 -*-
"""
بلوبرينت API - API Blueprint
"""
from flask import Blueprint

bp = Blueprint('api', __name__)

from api import routes
