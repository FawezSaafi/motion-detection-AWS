import boto3
# recuperation de video depuis s3
def get_s3video(parametres,BUCKET_FILE_NAME,LOCAL_FILE_NAME,IdArcAlarm):

    s3 = boto3.client('s3',aws_access_key_id=parametres['publickey'],
         aws_secret_access_key=parametres['secretkey'] )

    s3.download_file(parametres['bucketname'], BUCKET_FILE_NAME, LOCAL_FILE_NAME)

    print("download the video" ,IdArcAlarm,"to your local environment")
