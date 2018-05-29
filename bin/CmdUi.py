#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, json
sys.path.append( os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) ) + "/src" )
import Main

ServerPort = Main.CONFIG.get('DATA_SERVER','DATA_PORT')
ServerHost = Main.CONFIG.get('DATA_SERVER','DATA_HOST')

def GetMoniData () :
    Data = {}
    Data['Action'] = 'get'
    Data['ClientName'] = 'CmdUi'
    WdS = json.dumps(Data,ensure_ascii=False)
    ServerJson = Main.LiSocketClient ( ServerHost, ServerPort, WdS )
    ServData = json.loads( ServerJson )
    return ServData

def DataForMat ( Data ) :
    NewData = {}
    Title = {'HostName':'Name','HostIp':'IP','Cpu':'Cpu','Mem':'Mem','Swap':'Swap','Task':'Task','Disk':'Disk'}
    NewData['Title'] = Title
    for i in Data :
        d = Data[i]
        Disk = ','.join( d['AgentData']['DiskList'].values() )
        Tmp = { \
                'HostName':d['HostName'],'HostIp':d['HostIp'],'Cpu':d['AgentData']['Cpu']+'%',\
                'Mem':d['AgentData']['MemUse']+'M/'+d['AgentData']['MemTotal']+'M',\
                'Swap':d['AgentData']['SwapUse']+'M/'+d['AgentData']['SwapTotal']+'M',\
                'Task':d['AgentData']['Task'],'Disk':Disk\
                }
        NewData[i] = Tmp
    return NewData


if __name__=='__main__' :
    MoniData = GetMoniData()
    DataForMat(MoniData)
