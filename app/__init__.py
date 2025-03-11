from flask import Flask
from config.settings import Config

def create_app(config_class=Config):
    """創建並配置 Flask 應用"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 註冊路由
    from app.routes import vocabulary_routes
    app.register_blueprint(vocabulary_routes.bp)

    return app 