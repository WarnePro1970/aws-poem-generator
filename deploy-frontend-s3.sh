#!/bin/bash

# S3 Frontend Deployment Script
# Update these variables with your S3 bucket details
BUCKET_NAME="poem-generator-frontend-$(date +%s)"
REGION="us-east-1"

echo "🚀 Deploying Poem Generator Frontend to S3..."

# Step 1: Create S3 bucket
echo "📦 Creating S3 bucket: $BUCKET_NAME"
aws s3api create-bucket \
    --bucket $BUCKET_NAME \
    --region $REGION \
    --acl public-read

# Step 2: Enable static website hosting
echo "🌐 Enabling static website hosting..."
aws s3 website s3://$BUCKET_NAME/ \
    --index-document index.html \
    --error-document index.html

# Step 3: Create bucket policy for public access
echo "🔓 Setting bucket policy for public access..."
cat > bucket-policy.json <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "PublicReadGetObject",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::$BUCKET_NAME/*"
        }
    ]
}
EOF

aws s3api put-bucket-policy \
    --bucket $BUCKET_NAME \
    --policy file://bucket-policy.json

# Step 4: Upload frontend files
echo "📤 Uploading frontend files..."
aws s3 cp index.html s3://$BUCKET_NAME/ --acl public-read --content-type "text/html"
aws s3 cp styles.css s3://$BUCKET_NAME/ --acl public-read --content-type "text/css"
aws s3 cp script.js s3://$BUCKET_NAME/ --acl public-read --content-type "application/javascript"

# Cleanup
rm bucket-policy.json

# Get the website URL
WEBSITE_URL="http://$BUCKET_NAME.s3-website-$REGION.amazonaws.com"

echo "✅ Deployment complete!"
echo ""
echo "🌐 Your Poem Generator is live at:"
echo "   $WEBSITE_URL"
echo ""
echo "📝 S3 Bucket: $BUCKET_NAME"
echo "🌍 Region: $REGION"
echo ""
echo "To update the frontend, run:"
echo "   aws s3 sync . s3://$BUCKET_NAME/ --exclude '*.py' --exclude '*.sh' --exclude '*.md' --exclude '.git/*' --acl public-read"
echo ""
echo "To delete the deployment:"
echo "   aws s3 rb s3://$BUCKET_NAME --force" 