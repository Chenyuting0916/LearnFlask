import json
import os
import hashlib
import uuid
import secrets
import logging
from datetime import datetime, timedelta
from app.models.user import User

# 模擬用戶數據庫（實際應用中應使用真正的數據庫）
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
USERS_FILE = os.path.join(DATA_DIR, 'users.json')
RESET_TOKENS_FILE = os.path.join(DATA_DIR, 'reset_tokens.json')

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def _ensure_data_dir():
    """確保數據目錄存在"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        logger.info(f"創建數據目錄: {DATA_DIR}")
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            json.dump([], f)
            logger.info(f"創建用戶文件: {USERS_FILE}")
    if not os.path.exists(RESET_TOKENS_FILE):
        with open(RESET_TOKENS_FILE, 'w') as f:
            json.dump({}, f)
            logger.info(f"創建密碼重置令牌文件: {RESET_TOKENS_FILE}")

def _hash_password(password):
    """對密碼進行雜湊處理"""
    return hashlib.sha256(password.encode()).hexdigest()

def _load_users():
    """載入所有用戶"""
    _ensure_data_dir()
    try:
        with open(USERS_FILE, 'r') as f:
            users_data = json.load(f)
            
        # 將密碼字段添加到用戶字典中
        for user_data in users_data:
            if 'password' not in user_data and user_data.get('password_hash'):
                user_data['password'] = user_data['password_hash']
                
        users = [User.from_dict(user_data) for user_data in users_data]
        logger.info(f"成功載入 {len(users)} 名用戶")
        return users
    except Exception as e:
        logger.error(f"載入用戶時出錯: {str(e)}")
        return []

def _save_users(users):
    """保存所有用戶"""
    _ensure_data_dir()
    try:
        users_data = []
        for user in users:
            user_dict = user.to_dict()
            if hasattr(user, 'password') and user.password:
                user_dict['password'] = user.password
            users_data.append(user_dict)
            
        with open(USERS_FILE, 'w') as f:
            json.dump(users_data, f, indent=2)
        logger.info(f"成功保存 {len(users)} 名用戶")
    except Exception as e:
        logger.error(f"保存用戶時出錯: {str(e)}")

def _load_reset_tokens():
    """載入所有重置令牌"""
    _ensure_data_dir()
    try:
        with open(RESET_TOKENS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"載入重置令牌時出錯: {str(e)}")
        return {}

def _save_reset_tokens(tokens):
    """保存所有重置令牌"""
    _ensure_data_dir()
    try:
        with open(RESET_TOKENS_FILE, 'w') as f:
            json.dump(tokens, f, indent=2)
        logger.info(f"成功保存 {len(tokens)} 個重置令牌")
    except Exception as e:
        logger.error(f"保存重置令牌時出錯: {str(e)}")

def register_user(username, email, password):
    """註冊新用戶"""
    users = _load_users()
    
    # 檢查用戶名或電子郵件是否已存在
    if any(u.username == username for u in users) or any(u.email == email for u in users):
        logger.warning(f"嘗試註冊已存在的用戶: {username}/{email}")
        return None, "用戶名或電子郵件已存在"
    
    # 創建新用戶
    new_user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        password=_hash_password(password),
        created_at=datetime.now(),
        subscription_type='free'
    )
    
    users.append(new_user)
    _save_users(users)
    logger.info(f"新用戶註冊成功: {username}/{email}")
    
    # 返回新用戶（不包含密碼）
    user_dict = new_user.to_dict()
    if 'password' in user_dict:
        user_dict.pop('password', None)
    return user_dict, None

def login_user(email, password):
    """登錄用戶"""
    logger.info(f"嘗試登錄: {email}")
    users = _load_users()
    hashed_password = _hash_password(password)
    
    # 遍歷用戶並打印調試信息
    for user in users:
        logger.info(f"檢查用戶: {user.email}")
        
        # 檢查用戶電子郵件
        if user.email == email:
            logger.info(f"找到匹配的電子郵件: {email}")
            
            # 檢查密碼
            stored_password = getattr(user, 'password', None)
            logger.info(f"存儲的密碼雜湊: {stored_password}")
            logger.info(f"輸入的密碼雜湊: {hashed_password}")
            
            if stored_password and stored_password == hashed_password:
                logger.info(f"用戶 {email} 密碼驗證成功")
                
                # 返回用戶（不包含密碼）
                user_dict = user.to_dict()
                if 'password' in user_dict:
                    user_dict.pop('password', None)
                return user_dict, None
            else:
                logger.warning(f"用戶 {email} 密碼不匹配")
                
    logger.warning(f"登錄失敗: {email}")
    return None, "電子郵件或密碼不正確"

def get_user_by_id(user_id):
    """根據ID獲取用戶"""
    users = _load_users()
    
    for user in users:
        if user.id == user_id:
            user_dict = user.to_dict()
            if 'password' in user_dict:
                user_dict.pop('password', None)
            return user_dict
    
    return None

def get_user_by_email(email):
    """根據電子郵件獲取用戶"""
    users = _load_users()
    
    for user in users:
        if user.email == email:
            user_dict = user.to_dict()
            if 'password' in user_dict:
                user_dict.pop('password', None)
            return user_dict
    
    return None

def generate_reset_token(email):
    """生成密碼重置令牌"""
    user = get_user_by_email(email)
    if not user:
        logger.warning(f"嘗試為不存在的用戶生成重置令牌: {email}")
        return None, "找不到用戶"
    
    # 生成令牌
    token = secrets.token_urlsafe(32)
    expiry = (datetime.now() + timedelta(hours=1)).isoformat()
    
    # 保存令牌
    tokens = _load_reset_tokens()
    tokens[token] = {
        "user_id": user["id"],
        "expiry": expiry
    }
    _save_reset_tokens(tokens)
    logger.info(f"為用戶 {email} 生成重置令牌成功")
    
    return token, None

def verify_reset_token(token):
    """驗證密碼重置令牌"""
    tokens = _load_reset_tokens()
    
    if token not in tokens:
        logger.warning(f"嘗試驗證不存在的令牌")
        return None, "無效的令牌"
    
    token_data = tokens[token]
    expiry = datetime.fromisoformat(token_data["expiry"])
    
    if expiry < datetime.now():
        # 令牌已過期，刪除它
        del tokens[token]
        _save_reset_tokens(tokens)
        logger.warning(f"令牌已過期")
        return None, "令牌已過期"
    
    logger.info(f"令牌驗證成功，用戶ID: {token_data['user_id']}")
    return token_data["user_id"], None

def reset_password(token, new_password):
    """重置用戶密碼"""
    # 驗證令牌
    user_id, error = verify_reset_token(token)
    if error:
        return False, error
    
    # 更新密碼
    users = _load_users()
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i].password = _hash_password(new_password)
            _save_users(users)
            
            # 刪除令牌
            tokens = _load_reset_tokens()
            if token in tokens:
                del tokens[token]
                _save_reset_tokens(tokens)
            
            logger.info(f"用戶 {user_id} 密碼重置成功")
            return True, None
    
    logger.warning(f"嘗試重置不存在用戶的密碼: {user_id}")
    return False, "找不到用戶"

def update_user_profile(user_id, username, email):
    """更新用戶個人資料"""
    users = _load_users()
    updated_user = None
    
    # 檢查電子郵件是否已被其他用戶使用
    for user in users:
        if user.email == email and user.id != user_id:
            logger.warning(f"嘗試更新電子郵件到已存在的電子郵件: {email}")
            return None, "該電子郵件已被使用"
    
    # 更新用戶資料
    for i, user in enumerate(users):
        if user.id == user_id:
            users[i].username = username
            users[i].email = email
            updated_user = users[i]
            break
    
    if updated_user:
        _save_users(users)
        user_dict = updated_user.to_dict()
        if 'password' in user_dict:
            user_dict.pop('password', None)
        logger.info(f"用戶 {user_id} 個人資料更新成功")
        return user_dict, None
    
    logger.warning(f"嘗試更新不存在用戶的個人資料: {user_id}")
    return None, "找不到用戶"

def change_user_password(user_id, current_password, new_password):
    """修改用戶密碼"""
    users = _load_users()
    
    for i, user in enumerate(users):
        if user.id == user_id:
            # 驗證當前密碼
            if user.password != _hash_password(current_password):
                logger.warning(f"用戶 {user_id} 密碼驗證失敗")
                return False, "當前密碼不正確"
            
            # 更新密碼
            users[i].password = _hash_password(new_password)
            _save_users(users)
            logger.info(f"用戶 {user_id} 密碼修改成功")
            return True, None
    
    logger.warning(f"嘗試修改不存在用戶的密碼: {user_id}")
    return False, "找不到用戶"

def update_subscription(user_id, subscription_type, months=1):
    """更新用戶訂閱"""
    users = _load_users()
    updated_user = None
    
    for i, user in enumerate(users):
        if user.id == user_id:
            # 計算新的訂閱結束日期
            if user.subscription_end_date and datetime.fromisoformat(user.subscription_end_date) > datetime.now():
                end_date = datetime.fromisoformat(user.subscription_end_date) + timedelta(days=30*months)
            else:
                end_date = datetime.now() + timedelta(days=30*months)
            
            # 更新用戶
            users[i].subscription_type = subscription_type
            users[i].subscription_end_date = end_date
            updated_user = users[i]
            break
    
    if updated_user:
        _save_users(users)
        user_dict = updated_user.to_dict()
        if 'password' in user_dict:
            user_dict.pop('password', None)
        logger.info(f"用戶 {user_id} 訂閱更新成功: {subscription_type}")
        return user_dict, None
    
    logger.warning(f"嘗試更新不存在用戶的訂閱: {user_id}")
    return None, "找不到用戶"

# 用於測試的功能：創建測試用戶
def create_test_user():
    """創建測試用戶"""
    test_username = "testuser"
    test_email = "test@example.com"
    test_password = "password123"
    
    users = _load_users()
    
    # 檢查測試用戶是否已存在
    for user in users:
        if user.email == test_email:
            logger.info(f"測試用戶已存在: {test_email}")
            user_dict = user.to_dict()
            if 'password' in user_dict:
                user_dict.pop('password', None)
            return user_dict
    
    # 創建新的測試用戶
    new_user = User(
        id=str(uuid.uuid4()),
        username=test_username,
        email=test_email,
        password=_hash_password(test_password),
        created_at=datetime.now(),
        subscription_type='free'
    )
    
    users.append(new_user)
    _save_users(users)
    logger.info(f"測試用戶創建成功: {test_email}")
    
    # 返回新用戶（不包含密碼）
    user_dict = new_user.to_dict()
    if 'password' in user_dict:
        user_dict.pop('password', None)
    return user_dict 