from flask import Flask
import os


def create_app(test_config=None): #使用当前目录下的各BluePrint初始化app并将其返回
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=r'9*Q213TTDDti^DZ3tVk8va8hH*dJiBl@',
        DATABASE=os.path.join(app.instance_path, 'db.sqlite')
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    try:
        os.mkdir(app.instance_path)
    except OSError:
        pass

    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    from . import movienest
    app.register_blueprint(movienest.bp)
    app.add_url_rule('/', endpoint='home')

    return app
