# import my_secrets.py file
import my_secrets as ms
import boto3
import os

# Create an S3 client
client = boto3.client('s3',
                      aws_access_key_id=ms.access_key,
                      aws_secret_access_key=ms.secret_access_key)

# Bucket names must be unique across all S3 users
upload_file_bucket = 'energy-market-prices-spain'

# Local directory where the files to be uploaded are stored
local_directory = r'C:\Users\Usuario\Portfolio\Energy-Market-Prediction-Model-with-PySpark-and-TensorFlow\data'

# List all the files in the local directory
for filename in os.listdir(local_directory):
    local_file_path = os.path.join(local_directory, filename)
    
    # Verify that the file is a file, not a directory, and that it ends with .csv
    if os.path.isfile(local_file_path) and filename.endswith('.csv'):
        # Define the key, which is the path of the file in the bucket
        s3_key = os.path.relpath(local_file_path, start=local_directory)
        
        # Sube el archivo al bucket de S3
        client.upload_file(local_file_path, upload_file_bucket, s3_key)



    
   
