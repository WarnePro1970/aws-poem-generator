# AWS Lambda Poem Generator

A serverless AWS Lambda function that generates creative poems on any topic using OpenAI's GPT API.

🌐 **Live Demo**: [https://warnepro1970.github.io/aws-poem-generator/](https://warnepro1970.github.io/aws-poem-generator/)

## Features

- 🎭 Generate poems on any topic
- ⚡ Serverless AWS Lambda deployment
- 🌐 Optional API Gateway integration
- 🔒 Secure OpenAI API key management via environment variables
- 📱 CORS-enabled for web app integration

## Prerequisites

1. **AWS CLI** installed and configured with your credentials
   ```bash
   aws configure
   ```

2. **Python 3.9+** installed on your system

3. **OpenAI API Key** (already provided in the deployment script)

## Quick Deployment

### Option 1: Automated Deployment (Recommended)

Run the deployment script:

```bash
chmod +x deploy.sh
./deploy.sh
```

This script will:
- Create a virtual environment
- Install dependencies
- Package the Lambda function
- Create IAM roles
- Deploy the Lambda function
- Set up API Gateway (optional)

### Option 2: Manual AWS CLI Commands

If you prefer to run commands manually:

```bash
# 0. Set your OpenAI API key as environment variable
export OPENAI_API_KEY="your-openai-api-key-here"

# 1. Install dependencies locally
python3 -m venv lambda-env
source lambda-env/bin/activate
pip install -r requirements.txt

# 2. Create deployment package
mkdir package
cp lambda_function.py package/
cp -r lambda-env/lib/python*/site-packages/* package/
cd package && zip -r ../lambda-deployment.zip . && cd ..

# 3. Create IAM role
aws iam create-role \
    --role-name lambda-poem-generator-role \
    --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "lambda.amazonaws.com"},
                "Action": "sts:AssumeRole"
            }
        ]
    }'

aws iam attach-role-policy \
    --role-name lambda-poem-generator-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# 4. Deploy Lambda function
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
aws lambda create-function \
    --function-name poem-generator \
    --runtime python3.9 \
    --role arn:aws:iam::${ACCOUNT_ID}:role/lambda-poem-generator-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://lambda-deployment.zip \
    --environment Variables="{OPENAI_API_KEY=$OPENAI_API_KEY}" \
    --timeout 30 \
    --memory-size 256
```

## Testing the Function

### Test via AWS CLI

```bash
# Test with direct Lambda invocation
aws lambda invoke \
    --function-name poem-generator \
    --payload '{"topic":"sunset"}' \
    output.json

# View the result
cat output.json
```

### Test via API Gateway (if deployed)

```bash
# Replace with your actual API endpoint
curl -X POST https://YOUR_API_ID.execute-api.us-east-1.amazonaws.com \
    -H 'Content-Type: application/json' \
    -d '{"topic":"ocean"}'
```

## Request Format

The function accepts JSON input with a `topic` field:

```json
{
    "topic": "mountains"
}
```

## Response Format

The function returns a JSON response:

```json
{
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*"
    },
    "body": {
        "topic": "mountains",
        "poem": "Majestic peaks reach toward the sky...",
        "success": true
    }
}
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (automatically set by deployment script)

### Lambda Settings

- **Runtime**: Python 3.9
- **Timeout**: 30 seconds
- **Memory**: 256 MB
- **Handler**: `lambda_function.lambda_handler`

## Cost Considerations

- **AWS Lambda**: Pay per request and execution time
- **OpenAI API**: Pay per token usage (~$0.002 per 1K tokens for GPT-3.5-turbo)
- **API Gateway** (optional): Pay per API call

## Security

- OpenAI API key is stored as an environment variable
- Function includes basic error handling
- CORS headers included for web integration

## Troubleshooting

### Common Issues

1. **IAM Role Permissions**: Ensure the Lambda execution role has proper permissions
2. **API Key**: Verify the OpenAI API key is valid and has sufficient credits
3. **Timeout**: Increase timeout if OpenAI API calls are slow
4. **Dependencies**: Ensure all Python packages are included in the deployment package

### Logs

View Lambda logs:
```bash
aws logs describe-log-groups --log-group-name-prefix /aws/lambda/poem-generator
```

## Cleanup

To remove all resources:

```bash
# Delete Lambda function
aws lambda delete-function --function-name poem-generator

# Delete IAM role
aws iam detach-role-policy \
    --role-name lambda-poem-generator-role \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam delete-role --role-name lambda-poem-generator-role

# Delete API Gateway (if created)
aws apigatewayv2 delete-api --api-id YOUR_API_ID
```

## Example Poems

Here are some example topics you can try:
- "sunset over the ocean"
- "first day of spring"
- "childhood memories"
- "city lights at night"
- "love and friendship" 