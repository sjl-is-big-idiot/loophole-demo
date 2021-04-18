# _*_ coding: utf-8 _*_
# @FileName : views.py
# @Author   : sjl
# @CreatedAt     :  2021/03/24 15:13:51
# @UpdatedAt     :  2021/03/24 15:13:51
# @description: xxxx
# @Software : VSCode

from . import auth
from flask import request, g, current_app
from apps.db import get_db


@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            # TODO
            pass

@auth.route('/login', methods=['POST'])
def login():
    # TODO
    pass

@auth.route('/logout', methods=['PUT'])
def logout():
    # TODO
    pass