import boto3
import json

def main(event, context):
    s3 = boto3.client('s3')


    return {
        'statusCode': 200,
        'body': 'hello'
    }