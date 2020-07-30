ENV=$1
PROFILE=$2

# パラメータ読み込み
. ./params/environment.txt

# デプロイするファイル名を組み立て
DEPLOY_TEMPLATE="./deploy/Resources.yml"

# 新しく作成するテンプレートパス
NEW_DEPLOY_TEMPLATE="./deploy/resources.deploy"

# S3にアップロード
aws --profile ${PROFILE} cloudformation package --template-file ${DEPLOY_TEMPLATE} --output-template-file ${NEW_DEPLOY_TEMPLATE} --s3-bucket ${S3_BUCKET} --s3-prefix ${S3_PREFIX}
ret=$?
if [ ! $ret -eq 0 ] ;then
  echo "Package Error:${ret}"
  exit
fi
echo "package upload success->${DEPLOY_BUCKET_NAME}/${S3_PREFIX}"

# スタックのステータスによってデプロイ待機
STACK_NAME="${APP_NAME}-resources"
echo "stack name->${STACK_NAME}"

STATUS=`aws --profile ${PROFILE} cloudformation describe-stacks --stack-name ${STACK_NAME} --query "Stacks[].StackStatus[]" --output text`
echo "stack status is ${STATUS}"

if [ "${STATUS}" = "CREATE_IN_PROGRESS" ]; then
  echo "wait create...."
  aws --profile ${PROFILE} cloudformation wait stack-create-complete --stack-name ${STACK_NAME}
fi

if [ "${STATUS}" = "UPDATE_IN_PROGRESS" ]; then
  echo "wait update...."
  aws --profile ${PROFILE} cloudformation wait stack-update-complete --stack-name ${STACK_NAME}
fi

if [ "${STATUS}" = "DELETE_IN_PROGRESS" ]; then
  echo "wait delete...."
  aws --profile ${PROFILE} cloudformation wait stack-delete-complete --stack-name ${STACK_NAME}
fi

if [ "${STATUS}" = "ROLLBACK_COMPLETE" ]; then
  echo "delete stack...."
  aws --profile ${PROFILE} cloudformation delete-stack --stack-name ${STACK_NAME}
  aws --profile ${PROFILE} cloudformation wait stack-delete-complete --stack-name ${STACK_NAME}
fi

# デプロイ
aws --profile ${PROFILE} cloudformation deploy --template-file ${NEW_DEPLOY_TEMPLATE} --stack-name ${STACK_NAME} \
    --s3-bucket ${S3_BUCKET} --s3-prefix ${S3_PREFIX} \
    --capabilities CAPABILITY_NAMED_IAM --no-fail-on-empty-changeset \
    --parameter-overrides Env=${ENV}

rm ${NEW_DEPLOY_TEMPLATE}
