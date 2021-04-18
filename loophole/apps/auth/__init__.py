# _*_ coding: utf-8 _*_
# @FileName : __init__.py
# @Author   : sjl
# @CreatedAt     :  2021/03/24 11:10:43
# @UpdatedAt     :  2021/03/24 11:10:43
# @description: auth blueprint
# @Software : VSCode

import functools

from flask import (
    Blueprint, g, redirect, request
)


auth = Blueprint('auth', __name__, url_prefix='/auth')

from . import exceptions, forms, views