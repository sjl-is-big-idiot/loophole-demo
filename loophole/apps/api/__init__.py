# _*_ coding: utf-8 _*_
# @FileName : __init__.py
# @Author   : sjl
# @CreatedAt     :  2021/03/24 11:14:03
# @UpdatedAt     :  2021/03/24 11:14:03
# @description: main blueprint
# @Software : VSCode

from flask import (
    Blueprint, g, redirect, request
)

api = Blueprint('api', __name__)

from . import views, exceptions, models


