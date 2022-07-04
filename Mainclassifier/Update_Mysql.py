
import mysql.connector
import time
import datetime
import configparser
import threading
import random
from ec2_metadata import ec2_metadata
FileINI="c:\AC_Classifier\CONFIG/INI/SQLFileServerCfgINI.ini"

def GetDataBaseConnection():
    config = configparser.ConfigParser()
    config.read(FileINI)
    ServerIp=config['SGBD_SQL']['SERVER']
    #ServerPort=config['SGBD_SQL']['port']
    UserName=config['SGBD_SQL']['USER']
    Password=config['SGBD_SQL']['Password']
    DataBase=config['SGBD_SQL']['DataBase']
    from mysql.connector import Error

    try:
        connection = mysql.connector.connect(host=ServerIp,
                                             database=DataBase,
                                             user=UserName,
                                             password=Password)
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server ", db_Info)


    except Error as e:
        print("Error while connecting to MySQL", e)
    finally:
        if (connection.is_connected()):
            return(connection)
def create_id():
    random_id =str(random.randint(10000000,99999999))+'-'+str(random.randint(1000,9999))+'-'+str(random.randint(1000,9999))+'-'+str(random.randint(1000,9999))+'-'+str(random.randint(100000000000,999999999999))
    print(random_id)
    return(random_id)

def update_Mysql():
    ts = time.time()

    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    #print(timestamp)
    connection = GetDataBaseConnection()

    x = connection.cursor()
    def update() :
            try:
                sql_code="""INSERT INTO `server` (`id`, `role`, `public_ipv4`, `instance_id`, `local_ipv4`, `ami_id`, `availability_zone`, `instance_type`, `utcLastTimeGotNews`, `nbSecBeforeProblemOccurs`, `bState`, `bNplus1`, `state`, `lastTimeUsed`, `nb_failure`, `nomDomaine`, `Camera_AudioToCamPort`, `Websocket_AudioToCamPort`) VALUES (%s, 'classifier', %s,%s ,%s %s, %s, %s, NOW , '0', '1', '0', 'ALIVE', NOW, '0', '', '0', '0')"""
                values =(create_id(),ec2_metadata.public_ipv4,ec2_metadata.instance_id,ec2_metadata.local_ipv4,ec2_metadata.ami_id,ec2_metadata.availability_zone,ec2_metadata.instance_type)
                x.execute(sql_code,values)
                connection.commit()
            except:
                connection.rollback()

    t=threading.Timer(20.0,update())
    t.start()
    x.colse()
#create_id()
print((create_id(),ec2_metadata.public_ipv4,ec2_metadata.instance_id,ec2_metadata.local_ipv4,ec2_metadata.ami_id,ec2_metadata.availability_zone,ec2_metadata.instance_type))






