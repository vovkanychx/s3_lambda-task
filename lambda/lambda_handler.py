import boto3
import json

s3 = boto3.resource('s3')
client = boto3.client('s3')

def main(event, context):
    
    bucket_name = 'task-buck'
    
    # Set the new policy on the given bucket
    response = client.put_bucket_policy(
    Bucket='task-buck',
    Policy='{"Version": "2012-10-17","Id": "Policy14564645656","Statement": [{"Sid": "Stmt1445654645618","Effect": "Allow","Principal": {"AWS": "arn:aws:iam::589041093153:user/vovkanychx"},"Action": "s3:Get*","Resource": "arn:aws:s3:::task-buck/*"}]}')
    
    response1 = client.put_object(
    Bucket=bucket_name,
    Key='task-directory-source/test.txt',
    Body='Sample Text',
    ACL='public-read'
    )
    print(response) 
            
    for bucket in s3.buckets.all():
        print(bucket.name)

    return {
        'statusCode': 200,
        'body': 'Finally, success!'
    }