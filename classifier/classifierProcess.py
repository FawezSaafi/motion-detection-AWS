import boto3
from botocore.exceptions import NoCredentialsError
import requests
import os

import classifier
from classifier import analyse, connection, INI_variables

def classifierTest(FileName,AlarmClipWithAnalyticsPath,idArcAlarm,AlarmClipPath,idAbtObject,processed_path):
	fileNameWithoutExtension = FileName.split('.')[0]
	output_filePATH = processed_path.format(fileNameWithoutExtension)

	c=analyse.analyseVideoClip(None,AlarmClipWithAnalyticsPath, FileName,
							 output_filePATH,None,None,True,True)

	event ={"idArcAlarm":idArcAlarm,"AlarmClipPath_IN":AlarmClipWithAnalyticsPath,
		   "AlarmClipPath_out":output_filePATH,"idAbtObject":idAbtObject}
	S3_key = AlarmClipPath.split('.')[0]+"_processed.mp4"
	connection.upload_to_aws(event,S3_key,c,idArcAlarm)
	print("fin")



