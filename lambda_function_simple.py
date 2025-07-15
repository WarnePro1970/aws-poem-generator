import json
import os
import requests

def lambda_handler(event, context):
    """
    AWS Lambda function that generates poems based on a given topic using OpenAI API
    
    Expected event format:
    {
        "topic": "your poem topic here"
    }
    """
    
    try:
        # Get OpenAI API key from environment
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'OpenAI API key not configured',
                    'success': False
                })
            }
        
        # Extract topic from event
        if 'body' in event:
            # Handle API Gateway requests
            body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']
            topic = body.get('topic', 'love')
        else:
            # Handle direct Lambda invocation
            topic = event.get('topic', 'love')
        
        if not topic:
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Topic is required',
                    'success': False
                })
            }
        
        # Create the poem prompt
        prompt = f"Write a beautiful and creative poem about {topic}. Make it engaging, emotional, and well-structured with proper rhythm and flow."
        
        # Prepare the request to OpenAI API
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {
                    'role': 'system',
                    'content': 'You are a talented poet. Write beautiful, creative poems with good rhythm, imagery, and emotion.'
                },
                {
                    'role': 'user',
                    'content': prompt
                }
            ],
            'max_tokens': 500,
            'temperature': 0.8
        }
        
        # Make the API call
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code != 200:
            return {
                'statusCode': 500,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': f'OpenAI API error: {response.status_code}',
                    'success': False
                })
            }
        
        # Parse the response
        response_data = response.json()
        poem = response_data['choices'][0]['message']['content'].strip()
        
        # Return successful response
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'topic': topic,
                'poem': poem,
                'success': True
            })
        }
        
    except requests.exceptions.Timeout:
        return {
            'statusCode': 504,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Request timeout - OpenAI API took too long to respond',
                'success': False
            })
        }
    except requests.exceptions.RequestException as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Network error: {str(e)}',
                'success': False
            })
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': f'Failed to generate poem: {str(e)}',
                'success': False
            })
        } 