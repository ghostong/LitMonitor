#!/usr/bin/python

import sys, os, json
sys.path.append( os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) ) + "/src" )
import Main

ServerPort = Main.CONFIG.get('DATA_SERVER','DATA_PORT')
ServerHost = Main.CONFIG.get('DATA_SERVER','DATA_HOST')

ServerData = {}

def DataServer ( JsonData ) :
    Data = json.loads ( JsonData )
    if Data['Action'] == 'put' :
        print 'put:',Data['ClientName'],Data['HostIp']
        ServerData[Data['HostIp']] = Data
        return 'ok'
    else :
        print 'get:',Data['ClientName']
        Ret = json.dumps(ServerData,ensure_ascii=False)
        return Ret

if __name__=='__main__' :
    Main.LiSocketServer ( ServerHost, ServerPort, DataServer )
