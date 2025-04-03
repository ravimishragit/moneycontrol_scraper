#!/bin/bash

set -e  # Exit on error

LAMBDA_FUNCTION_NAME="brokerLambda"
LAMBDA_ROLE_ARN="arn:aws:iam::123456789012:role/LambdaExecutionRole"
S3_BUCKET_NAME="your-bucket-name"
JOB_DEFINITION_NAME="dataCleanup"
JOB_QUEUE_NAME="default"

echo "🚀 Packaging Lambda function..."
zip -r lambda_function.zip apis/lambda_handler.py processor utils

echo "☁️ Deploying AWS Lambda..."
aws lambda create-function --function-name $LAMBDA_FUNCTION_NAME \
    --runtime python3.8 --role $LAMBDA_ROLE_ARN \
    --handler lambda_handler.lambda_handler \
    --zip-file fileb://lambda_function.zip || \
aws lambda update-function-code --function-name $LAMBDA_FUNCTION_NAME \
    --zip-file fileb://lambda_function.zip

echo "🌐 Setting up API Gateway..."
REST_API_ID=$(aws apigateway create-rest-api --name "BrokerAPI" --query "id" --output text)
RESOURCE_ID=$(aws apigateway create-resource --rest-api-id $REST_API_ID --parent-id $(aws apigateway get-resources --rest-api-id $REST_API_ID --query "items[0].id" --output text) --path-part "recommendations" --query "id" --output text)
aws apigateway put-method --rest-api-id $REST_API_ID --resource-id $RESOURCE_ID --http-method GET --authorization-type "NONE"
aws apigateway put-integration --rest-api-id $REST_API_ID --resource-id $RESOURCE_ID --http-method GET --type AWS_PROXY --uri "arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/arn:aws:lambda:us-east-1:123456789012:function:$LAMBDA_FUNCTION_NAME/invocations"

echo "🔄 Deploying API Gateway..."
aws apigateway create-deployment --rest-api-id $REST_API_ID --stage-name "prod"

echo "🗑️ Setting up AWS Batch cleanup job..."
aws batch register-job-definition --job-definition-name $JOB_DEFINITION_NAME \
    --type container --container-properties "{\"image\": \"python:3.8\", \"command\": [\"python\", \"cleanup.py\"]}" || true

aws batch submit-job --job-name cleanupJob --job-queue $JOB_QUEUE_NAME --job-definition $JOB_DEFINITION_NAME

echo "🎉 Deployment Complete!"
