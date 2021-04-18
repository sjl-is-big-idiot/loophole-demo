# _*_ coding: utf-8 _*_
# @FileName : manage.py
# @Author   : sjl
# @CreatedAt     :  2021/03/26 11:53:04
# @UpdatedAt     :  2021/03/26 11:53:04
# @description: loophole project's entry
# @Software : VSCode

from apps import create_app
from flask import redirect, url_for

from apps import api

app = create_app()
app.debug = True


if __name__ == "__main__":
    app.run()