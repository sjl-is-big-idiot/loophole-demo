# _*_ coding: utf-8 _*_
# @FileName : __init__.py
# @Author   : sjl
# @CreatedAt     :  2021/03/24 10:46:48
# @UpdatedAt     :  2021/03/24 10:46:48
# @description: factory fucntion
# @Software : VSCode

import os

from flask import Flask


def create_app(config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder="./templates", static_folder="./static")
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE="bolt://localhost:7687",
        DB_PASSWORD="neo4j123456"
    )

    if config is None:
        # Load the instance confg, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(config)
    
    # ensure the instance folder exists
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    from . import db
    # db.init_app(app)

    from .auth  import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth")

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api/v1")

    return app