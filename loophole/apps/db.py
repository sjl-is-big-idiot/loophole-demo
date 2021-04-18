# _*_ coding: utf-8 _*_
# @FileName : db.py
# @Author   : sjl
# @CreatedAt     :  2021/03/24 10:59:17
# @UpdatedAt     :  2021/03/24 10:59:17
# @description: 
# @Software : VSCode

import py2neo

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db ' not in g:
        g.db = py2neo.Graph(
            current_app.config["DATABASE"],
            password=current_app.config["DB_PASSWORD"]
        )
    
    return g.db

def close_db(e=None):
    """
    py2neo not has to close db
    """
    db = g.pop('db', None)

    if db is not None:
        pass


def init_db():
    # db = get_db()
    # TODO
    from scripts.main import run
    run()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    # 告诉 Flask 在返回响应后进行清理的时候调用此函数
    app.teardown_appcontext(close_db)
    # 添加一个新的 可以与 flask 一起工作的命令
    app.cli.add_command(init_db_command)

