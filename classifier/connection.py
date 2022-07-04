import boto3
from botocore.exceptions import NoCredentialsError
import requests
import INI_variables
import os

def upload_to_aws(event, s3_file,occurences,IdArcAlarm):

    #upload the video to aws
    params = INI_variables.get_var()
    print("alarm clip path out  : ",event["AlarmClipPath_out"])
    session = boto3.Session(
        aws_access_key_id=params['publickey'],
        aws_secret_access_key=params['secretkey'],
    )
    s3 = session.resource('s3')
    try:
        print(event["AlarmClipPath_out"])
        s3.meta.client.upload_file(Filename=event["AlarmClipPath_out"], Bucket=params['bucketname'], Key=s3_file)

        print("Upload the video ",IdArcAlarm, " successfuly")

    except FileNotFoundError:
        print("The file was not found")
        return False
    except NoCredentialsError:
        print("Credentials not available")
        return False

    #delete the output file from my local environment
    #os.remove(event['AlarmClipPath_out'])

    post_parametrs = '{"idAbtObject":"' + event["idAbtObject"] + '","idArcAlarm":"' + event[
        "idArcAlarm"] + '","AlarmClipWithAnalyticsPath":"' + "files/ALARM/"+str(occurences)+ \
                     '","ResultClassifier1":-2,"ResultClassifier2":-2,"ResultClassifier3":-2,"ResultClassifier4":' + str(occurences) + '}'

    print(post_parametrs)
    headers = {'Content-Type': 'application/json'}
    #print(headers)
    r = requests.post(params['pushresulturl'],
                      data=post_parametrs, headers=headers)
    #print(r.text)



