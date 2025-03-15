from app import create_app
import os

# 從環境變量獲取配置
debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
host = os.environ.get('FLASK_HOST', '0.0.0.0')
port = int(os.environ.get('PORT', 5000))

# 創建應用
app = create_app()

if __name__ == '__main__':
    app.run(host=host, port=port, debug=debug_mode)