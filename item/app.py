from chalice import Chalice, Response
import boto3
import json
import item
import dynamo_func
import os
import sys
from logging import getLogger

app = Chalice(app_name='item')

# ログ初期化
logger = getLogger(__name__)
logger.setLevel(logging.INFO)

# 定数
HEADERS = { 'content_types': 'application/json' }

# 環境変数
TABLE_NAME = os.environ['TABLE_NAME']


@app.route('/item')
def put(methods=['POST'], content_types=['application/json']):
    
    logger.info('start function->{}'.format(sys._getframe().f_code.co_name))
    
    # パラメータ受け取り
    param = app.current_request.json_body
    item_obj = item.Item(param)
    logger.info('get parameter->{}'.format(item_obj.item))

    try:
        # 検証
        if item_obj.valid():
            # 保存
            res = dynamo_fanc.put(TABLE_NAME, item_obj.item)
            logger.info('put item->{}'.format(res))
            # TODO: resがJsonそのまま返してなかったらreturn修正
            return Response(
                body=json.dumps(res),
                headers=HEADERS,
                status_code=200,
            )
        else:
            return Response(
                body=json.dumps(item_obj.errors),
                headers=HEADERS,
                status_code=422,
            )
    except Exception as e:
        # 500系のエラーを返す
        logger.error(e)
        return Response(
                body=json.dumps({'err_msg': 'システムエラーが発生しました。'}),
                headers=HEADERS,
                status_code=500,
            )
