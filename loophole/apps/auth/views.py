# _*_ coding: utf-8 _*_
# @FileName : views.py
# @Author   : sjl
# @CreatedAt     :  2021/03/24 15:13:51
# @UpdatedAt     :  2021/03/24 15:13:51
# @description: xxxx
# @Software : VSCode

from . import auth
from flask import request, g, current_app, render_template, jsonify
from apps.db import get_db

# page route

@auth.route('/<string:page_name>.html', methods=['GET', 'POST'])
def page(page_name):
    """return all html pages"""
    return render_template(page_name + ".html")

# auth route

@auth.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        # db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        else:
            # TODO
            pass
            
    return jsonify({"username": username, "password": password, "message": error})


@auth.route('/login', methods=['POST'])
def login():
    # TODO
    return "this is a test view function."

@auth.route('/logout', methods=['PUT'])
def logout():
    # TODO
    return "this is a test view function."
