#!/bin/bash

# AWS Lambda Poem Generator Deployment Script
# Make sure you have AWS CLI configured with proper credentials

FUNCTION_NAME="poem-generator"
REGION="us-east-1"  # Change this to your preferred region

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ Error: OPENAI_API_KEY environment variable is not set"
    echo "Please set it with: export OPENAI_API_KEY='your-api-key'"
    exit 1
fi

echo "🚀 Starting deployment of AWS Lambda Poem Generator..."

# Step 1: Create a virtual environment and install dependencies
echo "📦 Creating virtual environment and installing dependencies..."
python3 -m venv lambda-env
source lambda-env/bin/activate
pip install -r requirements.txt

# Step 2: Create deployment package
echo "📦 Creating deployment package..."
mkdir -p package
cp lambda_function.py package/

# Copy installed packages to the package directory
cp -r lambda-env/lib/python*/site-packages/* package/

# Create the zip file
cd package
zip -r ../lambda-deployment.zip .
cd ..

# Step 3: Create IAM role for Lambda (if it doesn't exist)
echo "🔑 Creating IAM role for Lambda..."
aws iam create-role \
    --role-name lambda-poem-generator-role \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "Service": "lambda.amazonaws.com"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }' \
    --region $REGION 2>/dev/null || echo "Role already exists"

# Attach basic execution policy
aws iam attach-role-policy \
    --role-name lambda-poem-generator-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole \
    --region $REGION

# Wait a moment for role to be ready
echo "⏳ Waiting for IAM role to be ready..."
sleep 10

# Get account ID for the role ARN
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/lambda-poem-generator-role"

# Step 4: Create or update Lambda function
echo "🔧 Creating/updating Lambda function..."
aws lambda create-function \
    --function-name $FUNCTION_NAME \
    --runtime python3.9 \
    --role $ROLE_ARN \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://lambda-deployment.zip \
    --environment Variables="{OPENAI_API_KEY=$OPENAI_API_KEY}" \
    --timeout 30 \
    --memory-size 256 \
    --region $REGION 2>/dev/null

# If create failed, try update instead
if [ $? -ne 0 ]; then
    echo "Function exists, updating..."
    aws lambda update-function-code \
        --function-name $FUNCTION_NAME \
        --zip-file fileb://lambda-deployment.zip \
        --region $REGION
    
    aws lambda update-function-configuration \
        --function-name $FUNCTION_NAME \
        --environment Variables="{OPENAI_API_KEY=$OPENAI_API_KEY}" \
        --timeout 30 \
        --memory-size 256 \
        --region $REGION
fi

# Step 5: Create API Gateway (optional)
echo "🌐 Creating API Gateway..."
API_ID=$(aws apigatewayv2 create-api \
    --name poem-generator-api \
    --protocol-type HTTP \
    --target arn:aws:lambda:$REGION:$ACCOUNT_ID:function:$FUNCTION_NAME \
    --region $REGION \
    --query 'ApiId' \
    --output text 2>/dev/null)

if [ $? -eq 0 ]; then
    # Give API Gateway permission to invoke Lambda
    aws lambda add-permission \
        --function-name $FUNCTION_NAME \
        --statement-id api-gateway-permission \
        --action lambda:InvokeFunction \
        --principal apigateway.amazonaws.com \
        --source-arn "arn:aws:execute-api:$REGION:$ACCOUNT_ID:$API_ID/*" \
        --region $REGION 2>/dev/null
    
    API_ENDPOINT="https://${API_ID}.execute-api.${REGION}.amazonaws.com"
    echo "✅ API Gateway created: $API_ENDPOINT"
fi

# Cleanup
echo "🧹 Cleaning up..."
rm -rf lambda-env package lambda-deployment.zip
deactivate 2>/dev/null || true

echo "✅ Deployment complete!"
echo ""
echo "🎯 Function Name: $FUNCTION_NAME"
echo "🌍 Region: $REGION"
echo "📝 You can test the function with:"
echo "   aws lambda invoke --function-name $FUNCTION_NAME --payload '{\"topic\":\"sunset\"}' output.json --region $REGION"
echo ""
if [ ! -z "$API_ENDPOINT" ]; then
    echo "🌐 API Endpoint: $API_ENDPOINT"
    echo "📡 Test with curl:"
    echo "   curl -X POST $API_ENDPOINT -H 'Content-Type: application/json' -d '{\"topic\":\"ocean\"}'"
fi 