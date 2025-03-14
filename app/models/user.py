from datetime import datetime

class User:
    def __init__(self, id=None, username=None, email=None, password=None, 
                 created_at=None, subscription_type=None, subscription_end_date=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password  # 存儲時應該被加密
        self.created_at = created_at or datetime.now()
        self.subscription_type = subscription_type or 'free'  # 'free', 'basic', 'premium'
        self.subscription_end_date = subscription_end_date
        
    def to_dict(self):
        """將用戶對象轉換為字典"""
        result = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at,
            'subscription_type': self.subscription_type
        }
        
        if self.subscription_end_date:
            if isinstance(self.subscription_end_date, datetime):
                result['subscription_end_date'] = self.subscription_end_date.isoformat()
            else:
                result['subscription_end_date'] = self.subscription_end_date
        else:
            result['subscription_end_date'] = None
            
        return result
    
    @classmethod
    def from_dict(cls, data):
        """從字典創建用戶對象"""
        created_at = None
        if data.get('created_at'):
            try:
                created_at = datetime.fromisoformat(data.get('created_at'))
            except (ValueError, TypeError):
                created_at = data.get('created_at')
        
        subscription_end_date = None
        if data.get('subscription_end_date'):
            try:
                subscription_end_date = datetime.fromisoformat(data.get('subscription_end_date'))
            except (ValueError, TypeError):
                subscription_end_date = data.get('subscription_end_date')
        
        # 優先使用password字段，如果沒有則使用password_hash字段
        password = data.get('password') or data.get('password_hash')
        
        return cls(
            id=data.get('id'),
            username=data.get('username'),
            email=data.get('email'),
            password=password,
            created_at=created_at,
            subscription_type=data.get('subscription_type'),
            subscription_end_date=subscription_end_date
        ) 