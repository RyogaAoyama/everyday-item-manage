import boto3

dynamo = boto3.resource('dynamodb')

# データを新規追加
def put(self, table_name, item):
    try:
        return self.table.put_item(TableName=table_name, Item=item)
    except Exception as e:
        raise Exception('DynamoDB put error->{}'.format(e))