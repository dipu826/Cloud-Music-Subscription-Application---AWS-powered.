import json
import boto3

dynamodb = boto3.resource('dynamodb')
subscription_table = dynamodb.Table('subscription')

def lambda_handler(event, context):
    try:
        print("Received event:", event)

        email = event['email']
        title = event['title']
        artist = event['artist']
        year = event['year']
        album = event['album']
        image_url = event['image_url']

        subscription_table.put_item(Item={
            'email': email,
            'title': title,
            'artist': artist,
            'year': year,
            'album': album,
            'image_url': image_url
        })

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': 'Subscription successful'})
        }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
