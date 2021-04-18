# _*_ coding: utf-8 _*_
# @FileName : utils.py
# @Author   : sjl
# @CreatedAt     :  2021/03/24 15:21:56
# @UpdatedAt     :  2021/03/24 15:21:56
# @description: xxxx
# @Software : VSCode

from functools import wraps
from flask import g, redirect, url_for


def login_required(view):
    @wraps
    def wrapper(*args, **kwargs):
        if "username" not in g:
            redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapper


def dedup(items, hash_func=lambda x:x):
    """Deduplication for nodes
    """
    seen = set()
    for item in items:
        key = hash_func(item)
        if key not in seen:
            yield item
            seen.add(key)
    
