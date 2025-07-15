# AI Poem Generator Frontend

A beautiful, modern web interface for the AWS Lambda Poem Generator API.

## Features

- 🎨 Modern, responsive design with gradient backgrounds
- ✨ Smooth animations and transitions
- 📋 One-click copy to clipboard
- 🔄 Loading states and error handling
- 📱 Mobile-friendly interface
- 🎯 Example topic suggestions

## Files

- `index.html` - Main HTML structure
- `styles.css` - Beautiful CSS styling with animations
- `script.js` - JavaScript for API calls and interactions
- `serve.py` - Simple Python server for local testing

## Quick Start

### Option 1: Local Python Server
```bash
python3 serve.py
```
Then open http://localhost:8000 in your browser.

### Option 2: Direct File Access
Simply open `index.html` in your web browser.

### Option 3: Deploy to S3 (Static Website)
1. Create an S3 bucket with static website hosting enabled
2. Upload `index.html`, `styles.css`, and `script.js`
3. Make files public and access via S3 website URL

## API Endpoint

The frontend is configured to use:
```
https://ytxzaqj65a.execute-api.us-east-1.amazonaws.com
```

To change the API endpoint, edit the `API_ENDPOINT` constant in `script.js`.

## Usage

1. Enter a topic in the input field
2. Click "Generate Poem" or press Enter
3. Wait for the beautiful poem to appear
4. Click the copy button to copy the poem to clipboard
5. Click "Create Another Poem" to start again

## Example Topics

- Sunset over the ocean
- First day of spring
- Childhood memories
- City lights at night
- Morning coffee
- Rainy days
- Starry night sky
- Autumn leaves

## Customization

### Colors
Edit the gradient colors in `styles.css`:
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### API Response Time
Adjust the timeout in `script.js` if needed.

### Animations
Modify animation speeds and effects in `styles.css`.

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## Troubleshooting

- **CORS Error**: Make sure the Lambda function includes proper CORS headers
- **API Error**: Check that the API endpoint is correct and the Lambda function is running
- **Copy not working**: Some browsers require HTTPS for clipboard access

Enjoy creating beautiful poems! 🎭✨ 