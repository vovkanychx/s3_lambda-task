import boto3
import json

client = boto3.client('s3')
s3 = boto3.resource('s3')
    
task_bucket_name = 'task-buck'
src_dir = 'task-src-dir/'
dest_dir = 'task-dest-dir/'

def main(event, context):
    
    for record in event['Records']:
        file = {
            'bucket' : record['s3']['bucket']['name'],
            'key' : record['s3']['object']['key']
        }
        json.dumps(file)
        
        client.copy_object(
            Bucket = task_bucket_name,
            CopySource = {
                'Bucket': task_bucket_name,
                'Key': src_dir
            },
            Key = dest_dir + file['key']
        )
        #need to take uploaded keys, not 'task-src-dir/key' but 'key' to create correct copy in 'task-dest-dir' like: 
        #'task-dest-dir/key' but not 'task-dest-dir/task-src-dir/key' because it takes 'task-src-dir/key' as object key
        print(json.dumps(file))

    return {
        'statusCode': 200,
        'body': 'Finally, success!'
    }