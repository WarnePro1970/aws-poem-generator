import json
import os
from openai import OpenAI

def lambda_handler(event, context):
    """
    AWS Lambda function that generates poems based on a given topic using OpenAI API
    
    Expected event format:
    {
        "topic": "your poem topic here"
    }
    """
    
    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        
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
                    'error': 'Topic is required'
                })
            }
        
        # Create the poem prompt
        prompt = f"Write a beautiful and creative poem about {topic}. Make it engaging, emotional, and well-structured with proper rhythm and flow."
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a talented poet. Write beautiful, creative poems with good rhythm, imagery, and emotion."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            max_tokens=500,
            temperature=0.8
        )
        
        # Extract the poem from the response
        poem = response.choices[0].message.content.strip()
        
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