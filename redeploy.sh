#!/bin/bash

# Simple AWS Lambda Redeployment Script
FUNCTION_NAME="poem-generator"
REGION="us-east-1"

echo "🔄 Redeploying Lambda function with fixed dependencies..."

# Create a clean package directory
rm -rf package
mkdir package

# Copy the Lambda function
cp lambda_function.py package/

# Install dependencies directly to the package directory
pip install --target package openai==1.57.4

# Create the zip file
cd package
zip -r ../lambda-deployment-fixed.zip .
cd ..

# Update the Lambda function
echo "📦 Updating Lambda function code..."
aws lambda update-function-code \
    --function-name $FUNCTION_NAME \
    --zip-file fileb://lambda-deployment-fixed.zip \
    --region $REGION

echo "✅ Function updated successfully!"
echo "🧹 Cleaning up..."
rm -rf package lambda-deployment-fixed.zip

echo "🎯 Test the function with:"
echo "   aws lambda invoke --function-name $FUNCTION_NAME --payload \$(echo '{\"topic\":\"ocean\"}' | base64) output.json --region $REGION" 