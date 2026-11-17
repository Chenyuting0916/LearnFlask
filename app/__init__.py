import os
from datetime import timedelta

from flask import Flask, session, redirect, url_for
from flask_wtf.csrf import CSRFProtect
from config.settings import Config

csrf = CSRFProtect()

def create_app(config_class=Config):
    """創建並配置 Flask 應用"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config.update(
        WTF_CSRF_CHECK_DEFAULT=False,
        WTF_CSRF_TIME_LIMIT=3600,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        PERMANENT_SESSION_LIFETIME=timedelta(hours=12),
    )
    if os.environ.get("FLASK_ENV", "").lower() == "production":
        app.config["SESSION_COOKIE_SECURE"] = True
    csrf.init_app(app)

    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response

    # 確保靜態和數據目錄存在
    from app.services import japanese_service
    japanese_service._ensure_data_dir()

    # 註冊路由
    from app.routes import japanese_routes, auth_routes
    app.register_blueprint(japanese_routes.bp)
    app.register_blueprint(auth_routes.bp)

    # 添加日期格式化過濾器
    @app.template_filter('format_date')
    def format_date(value, format='%Y-%m-%d'):
        """格式化日期字符串"""
        if not value:
            return ""
        if isinstance(value, str):
            from datetime import datetime
            try:
                value = datetime.fromisoformat(value)
            except ValueError:
                return value
        return value.strftime(format)

    # 註冊全局上下文處理器
    @app.context_processor
    def inject_user():
        """將用戶信息注入所有模板"""
        return {
            'user_id': session.get('user_id'),
            'username': session.get('username'),
            'user_subscription': session.get('user_subscription', 'free')
        }

    # 首頁重定向到日語學習首頁
    @app.route('/')
    def index():
        return redirect(url_for('japanese.index'))

    return app 