# -*- coding:utf-8 -*-

from flask import Blueprint

pic =Blueprint('pic', __name__)

from . import views,forms