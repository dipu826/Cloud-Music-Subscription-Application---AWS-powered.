import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
subscription_table = dynamodb.Table('subscription')

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        print("Incoming event:", json.dumps(event))  # Debug log

        email = event.get('email')

        if not email:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'Email parameter is required'})
            }

        print("Getting subscriptions for:", email)

        response = subscription_table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        subscriptions = response.get('Items', [])

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'subscriptions': subscriptions}, cls=DecimalEncoder)
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
