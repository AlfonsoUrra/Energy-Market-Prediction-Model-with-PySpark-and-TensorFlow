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
# carpetas dentro del bucket



# Local directory where the files to be uploaded are stored
local_directory = r'C:\Users\Usuario\Portfolio\Energy-Market-Prediction-Model-with-PySpark-and-TensorFlow\data'

# List all the files in the local directory
for filename in os.listdir(local_directory):
    local_file_path = os.path.join(local_directory, filename)
    
    # Verify that the file is a file, not a directory, and that it ends with .csv
    if os.path.isfile(local_file_path) and filename.endswith('.csv'):
        # Define the key, which is the path of the file in the bucket
        s3_key = os.path.join(filename)
        
        
        # Sube el archivo al bucket de S3
        client.upload_file(local_file_path, upload_file_bucket, s3_key)



    
   
import psycopg2
import logging

# Redshift connection
try:
    con = psycopg2.connect(dbname='dev',
                            host='default-workgroup.484808363891.eu-north-1.redshift-serverless.amazonaws.com',
                            port='5439',
                            user='admin',
                            password='Caraculo22$')
    logging.info("Connected to Redshift")
except Exception as e:
    logging.exception("Unable to connect to Redshift")

con.autocommit = True
cur = con.cursor()
schema_name = 'data_query'
table_name = 'yearly_prices'
s3_location = 's3://energy-market-prices-spain/df_yearly_prices.csv'

copy_query = """copy {}.{} from '{}'
iam_role 'arn:aws:iam::484808363891:role/service-role/AmazonRedshift-CommandsAccessRole-20231004T223449'
IGNOREHEADER 1
CSV
TIMEFORMAT 'auto'
DELIMITER ',';
""".format(schema_name, table_name, s3_location)

cur.execute(copy_query)