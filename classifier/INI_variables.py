from configparser import ConfigParser
FileINI="C:\AC_Classifier\CONFIG\INI\AC_Classifier.ini"
#recuperation of variables from INI file
def get_var(FileLocation=FileINI):
    parser = ConfigParser()
    parser.read(FileLocation)
    d=dict()

    for name, value in parser.items(parser.sections()[parser.sections().index('ClipStorage')]):
            #retrieving parameters from the dictionary d
            if name in['bucketname','secretkey','publickey','pushresulturl']:
                d[name]=value
    return(d)