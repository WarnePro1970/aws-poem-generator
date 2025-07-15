import json
import os
import urllib.request
import urllib.parse
import ssl

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
        
        # Prepare the request data
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
        
        # Convert data to JSON
        json_data = json.dumps(data).encode('utf-8')
        
        # Create the request
        req = urllib.request.Request(
            'https://api.openai.com/v1/chat/completions',
            data=json_data,
            headers={
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
        )
        
        # Make the API call
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                response_data = json.loads(response.read().decode('utf-8'))
                
                if response.status == 200:
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
                else:
                    return {
                        'statusCode': 500,
                        'headers': {
                            'Content-Type': 'application/json',
                            'Access-Control-Allow-Origin': '*'
                        },
                        'body': json.dumps({
                            'error': f'OpenAI API error: {response.status}',
                            'success': False
                        })
                    }
                    
        except urllib.error.HTTPError as e:
            error_response = e.read().decode('utf-8')
            return {
                'statusCode': e.code,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': f'OpenAI API HTTP error: {e.code} - {error_response}',
                    'success': False
                })
            }
        except urllib.error.URLError as e:
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