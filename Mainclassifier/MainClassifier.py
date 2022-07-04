import flask
from flask import request, jsonify
import INI_variables
import Recuperation_s3video
import os
import classifier
from classifier import classifierProcess
#import Update_Mysql

app = flask.Flask(__name__)
app.config["DEBUG"] = True
@app.route('/AC_Classifier/PHPScripts/PushVideoToClassifier', methods=['GET','POST'])
def PushVideoToClassifier():
    # recuperation of variables from URL
    processed_path=r'C:\Users\21658\PycharmProjects\fawezsaafi1\video\processed_{}'
    if 'idArcAlarm' in request.args:
        idArcAlarm = request.args.get('idArcAlarm')

    else:
        return "Error: No idArcAlarm field provided. Please specify an idArcAlarm."

    if 'AlarmClipPathHost' in request.args:
        AlarmClipPathHost = request.args.get('AlarmClipPathHost')
    else:
        return "Error: No AlarmClipPathHost field provided. Please specify an AlarmClipPathHost."
    if 'AlarmClipPath' in request.args:
        AlarmClipPath = request.args.get('AlarmClipPath')

    else:
        return "Error: No AlarmClipPathHost field provided. Please specify an AlarmClipPathHost."
    if 'idAbtObject' in request.args:
        idAbtObject= request.args.get('idAbtObject')

    else:
        return "Error: No AlarmClipPathHost field provided. Please specify an AlarmClipPathHost."
    #print(idArcAlarm)
    result={'idArcAlarm':idArcAlarm,'AlarmClipPath':AlarmClipPath,'idAbtObject':idAbtObject,'AlarmClipPathHost':AlarmClipPathHost}


    FileName=AlarmClipPath.split('/')[-1]
    print("File Name : ", FileName )
    #download the video from s3
    Recuperation_s3video.get_s3video(INI_variables.get_var(),AlarmClipPath,processed_path.format(FileName),idArcAlarm)
    # put the video into classifier and upload result video to s3
    classifierProcess.classifierTest(FileName,processed_path.format(FileName),idArcAlarm,AlarmClipPath,idAbtObject,processed_path)
    #Update_Mysql.update()
    result={'idArcAlarm':idArcAlarm,'AlarmClipPath':AlarmClipPath,'idAbtObject':idAbtObject,'AlarmClipPathHost':AlarmClipPathHost}
    print("final result", result)
    return jsonify(result)
app.run()



