from cerberus import Validator
from datetime import date, datetime


class Item():
    # TODO: NoSQLインジェクション対策
    # TODO: 気が向いたらバリデーションメッセージを日本語化
    schema = {
        'item_name': {
            'type': 'string',
            'required': True,
            'empty': False,
        },
        'brand_id': { 
            'type': 'string',
            'required': True,
            'empty': False,
        },
        'item_price': {
            'type': 'integer',
            'required': True,
            'empty': False,
        },
        'picture': {
            'type': 'string',
        },
        'place': {
            'type': 'string',
        },
        'url': {
            'type': 'string',
            'regex': '^http[s]?://.*$',
        },
        'limit_days': {
            'type': 'integer',
            'required': True,
            'empty': False,
        },
    }
    v = Validator(schema)
    item = {}
    errors = {}
    
    def __init__(self, param):
        # パラメーター
        self.item = param.copy()
        # 補充日
        self.item['reload'] = date.today()
        # 登録日
        self.item['created_at'] = datetime.today()
        # 更新日
        self.item['updated_at'] = datetime.today()
    
    # 検証
    def valid(self):
        result = self.v.validate(self.item)
        self.errors = self.v.errors
        return result