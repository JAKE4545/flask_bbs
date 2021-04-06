from flask import Flask
from apps.cms.views import cms as cms_bp
# from apps.common.views import bp as common_bp
# from apps.front.views import bp as front_bp
from apps.OnlineQuestion.view import OnlineQuestion
import config
from exts import db
from flask_wtf import CSRFProtect
# from apps.main import main

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(cms_bp)
    # app.register_blueprint(main)
    app.register_blueprint(OnlineQuestion,)
    db.init_app(app=app)
    db.create_all(app=app)
    # db.session.commit()
    # login_manager.init_app(app)
    # db.create_all(app=app)
    # mail.init_app(app)
    CSRFProtect(app)
    return app

if __name__ == '__main__':
    app = create_app()
    # print(app.url_map)
    app.run()