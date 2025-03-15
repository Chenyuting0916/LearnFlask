from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app.services import auth_service
import secrets
import re
import logging

# 設置日誌
logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """用戶註冊頁面"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 簡單驗證
        if not all([username, email, password, confirm_password]):
            flash('所有欄位都是必填的', 'error')
            return render_template('auth/register.html')
        
        if password != confirm_password:
            flash('密碼不匹配', 'error')
            return render_template('auth/register.html')
        
        # 註冊用戶
        user, error = auth_service.register_user(username, email, password)
        if error:
            flash(error, 'error')
            return render_template('auth/register.html')
        
        # 註冊成功，設置會話
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['user_subscription'] = user['subscription_type']
        
        flash('註冊成功！歡迎加入我們的日語學習平台。', 'success')
        return redirect(url_for('japanese.index'))
    
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """用戶登錄頁面"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # 簡單驗證
        if not all([email, password]):
            flash('所有欄位都是必填的', 'error')
            return render_template('auth/login.html')
        
        # 登錄用戶
        user, error = auth_service.login_user(email, password)
        if error:
            flash(error, 'error')
            return render_template('auth/login.html')
        
        # 登錄成功，設置會話
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['user_subscription'] = user['subscription_type']
        
        logger.info(f"用戶登錄成功：{user['username']}, 會話ID：{session.get('user_id')}")
        flash('登錄成功！', 'success')
        return redirect(url_for('japanese.index'))
    
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    """用戶登出"""
    username = session.get('username', '未知用戶')
    
    # 清除會話
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('user_subscription', None)
    session.clear()  # 完全清除會話
    
    logger.info(f"用戶登出：{username}")
    flash('您已成功登出', 'success')
    return redirect(url_for('japanese.index'))

@bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """忘記密碼頁面"""
    if request.method == 'POST':
        email = request.form.get('email')
        
        if not email:
            flash('電子郵件是必填的', 'error')
            return render_template('auth/forgot_password.html')
        
        # 生成重置令牌
        token, error = auth_service.generate_reset_token(email)
        if error:
            flash(error, 'error')
            return render_template('auth/forgot_password.html')
        
        # 在實際應用中，這裡應該發送一封電子郵件
        # 為了測試方便，我們直接顯示重置鏈接
        reset_url = url_for('auth.reset_password', token=token, _external=True)
        flash(f'密碼重置鏈接已生成：{reset_url}', 'success')
        
        return render_template('auth/forgot_password.html')
    
    return render_template('auth/forgot_password.html')

@bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """重置密碼頁面"""
    # 驗證令牌
    user_id, error = auth_service.verify_reset_token(token)
    if error:
        flash(error, 'error')
        return redirect(url_for('auth.forgot_password'))
    
    if request.method == 'POST':
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # 簡單驗證
        if not all([password, confirm_password]):
            flash('所有欄位都是必填的', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        if password != confirm_password:
            flash('密碼不匹配', 'error')
            return render_template('auth/reset_password.html', token=token)
        
        # 重置密碼
        success, error = auth_service.reset_password(token, password)
        if error:
            flash(error, 'error')
            return render_template('auth/reset_password.html', token=token)
        
        flash('密碼已成功重置，請使用新密碼登錄', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/reset_password.html', token=token)

@bp.route('/profile')
def profile():
    """用戶個人資料頁面"""
    # 檢查用戶是否已登錄
    if 'user_id' not in session:
        flash('請先登錄以訪問個人資料', 'warning')
        return redirect(url_for('auth.login'))
    
    # 獲取用戶資料
    user = auth_service.get_user_by_id(session['user_id'])
    if not user:
        flash('找不到用戶資料', 'error')
        return redirect(url_for('auth.logout'))
    
    return render_template('auth/profile.html', user=user)

@bp.route('/profile/edit', methods=['GET', 'POST'])
def edit_profile():
    """編輯個人資料頁面"""
    # 檢查用戶是否已登錄
    if 'user_id' not in session:
        flash('請先登錄以編輯個人資料', 'warning')
        return redirect(url_for('auth.login'))
    
    # 獲取用戶資料
    user = auth_service.get_user_by_id(session['user_id'])
    if not user:
        flash('找不到用戶資料', 'error')
        return redirect(url_for('auth.logout'))
    
    if request.method == 'POST':
        # 獲取表單數據
        username = request.form.get('username')
        email = request.form.get('email')
        
        # 簡單驗證
        if not all([username, email]):
            flash('所有欄位都是必填的', 'error')
            return render_template('auth/edit_profile.html', user=user)
        
        # 更新用戶資料
        updated_user, error = auth_service.update_user_profile(
            session['user_id'], username, email
        )
        
        if error:
            flash(error, 'error')
            return render_template('auth/edit_profile.html', user=user)
        
        # 更新會話中的用戶名
        session['username'] = updated_user['username']
        
        flash('個人資料更新成功！', 'success')
        return redirect(url_for('auth.profile'))
    
    return render_template('auth/edit_profile.html', user=user)

@bp.route('/profile/change_password', methods=['GET', 'POST'])
def change_password():
    """修改密碼頁面"""
    # 檢查用戶是否已登錄
    if 'user_id' not in session:
        flash('請先登錄以修改密碼', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        # 獲取表單數據
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # 簡單驗證
        if not all([current_password, new_password, confirm_password]):
            flash('所有欄位都是必填的', 'error')
            return render_template('auth/change_password.html')
        
        if new_password != confirm_password:
            flash('新密碼不匹配', 'error')
            return render_template('auth/change_password.html')
        
        # 更新密碼
        success, error = auth_service.change_user_password(
            session['user_id'], current_password, new_password
        )
        
        if not success:
            flash(error, 'error')
            return render_template('auth/change_password.html')
        
        flash('密碼修改成功！請使用新密碼登錄。', 'success')
        return redirect(url_for('auth.logout'))
    
    return render_template('auth/change_password.html')

@bp.route('/subscription')
def subscription():
    """訂閱頁面"""
    # 檢查用戶是否已登錄
    if 'user_id' not in session:
        flash('請先登錄以查看訂閱資訊', 'warning')
        return redirect(url_for('auth.login'))
    
    # 獲取用戶資料
    user = auth_service.get_user_by_id(session['user_id'])
    if not user:
        flash('找不到用戶資料', 'error')
        return redirect(url_for('auth.logout'))
    
    # 更新會話中的訂閱狀態
    session['user_subscription'] = user['subscription_type']
    
    return render_template('auth/subscription.html', user=user)

@bp.route('/payment', methods=['GET', 'POST'])
def payment():
    """付款頁面"""
    # 檢查用戶是否已登錄
    if 'user_id' not in session:
        flash('請先登錄以進行付款', 'warning')
        return redirect(url_for('auth.login'))
    
    if request.method == 'GET':
        # 從 URL 參數獲取訂閱類型和月份
        subscription_type = request.args.get('type', 'premium')
        months = request.args.get('months', '1')
        
        # 驗證參數
        if subscription_type not in ['basic', 'premium']:
            subscription_type = 'premium'
        
        try:
            months = int(months)
            if months not in [1, 3, 12]:
                months = 1
        except (TypeError, ValueError):
            months = 1
        
        return render_template('auth/payment.html',
                             subscription_type=subscription_type,
                             months=months)
    
    # 處理 POST 請求（實際支付邏輯）
    if request.method == 'POST':
        subscription_type = request.form.get('subscription_type')
        months = request.form.get('months')
        payment_method = request.form.get('payment_method')
        
        # TODO: 實現實際的支付處理邏輯
        
        flash('支付成功！您的訂閱已經更新。', 'success')
        return redirect(url_for('auth.profile')) 