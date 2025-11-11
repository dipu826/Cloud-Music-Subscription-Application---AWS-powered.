import json
import boto3

dynamodb = boto3.resource('dynamodb')
login_table = dynamodb.Table('login')

def lambda_handler(event, context):
    try:
        print("Received event:", event)

        if 'body' in event and isinstance(event['body'], str):
            event = json.loads(event['body'])

        email = event.get('email')
        username = event.get('user_name')
        password = event.get('password')

        # Validate fields
        if not email or not username or not password:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Missing fields'})
            }

        # Checking if email already exists
        response = login_table.get_item(Key={'email': email})
        if 'Item' in response:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Email already exists'})
            }

        # Registering new user
        login_table.put_item(Item={
            'email': email,
            'user_name': username,
            'password': password
        })

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Registered'})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
