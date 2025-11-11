import json
import boto3
from boto3.dynamodb.conditions import Attr
from decimal import Decimal

# Setup DynamoDB
dynamodb = boto3.resource('dynamodb')
music_table = dynamodb.Table('music')

# Fix for Decimal serialization issue
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    try:
        print("Received event:", event)

        filters = []

    
        if event.get('title'):
            filters.append(Attr('title').contains(event['title']))
        if event.get('artist'):
            filters.append(Attr('artist').contains(event['artist']))
        if event.get('year'):
            try:
                filters.append(Attr('year').eq(int(event['year'])))
            except ValueError:
                return {
                    'statusCode': 400,
                    'headers': {'Access-Control-Allow-Origin': '*'},
                    'body': json.dumps({'error': 'Year must be a number'})
                }
        if event.get('album'):
            filters.append(Attr('album').contains(event['album']))

        if not filters:
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'error': 'At least one field is required'})
            }

        # Combining filter expressions
        filter_exp = filters[0]
        for f in filters[1:]:
            filter_exp = filter_exp & f

        # Query music table
        response = music_table.scan(FilterExpression=filter_exp)
        results = response['Items']

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'results': results}, cls=DecimalEncoder)
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
