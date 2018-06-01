#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, json, time
sys.path.append( os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) ) + "/src" )
import Main

SshKeyFile = Main.SSH_KEY_FILE
HostList   = Main.CONFIG.items("HOST_LIST")
UserName   = Main.CONFIG.get('SSH2_CONFIG','SSH2_USER')
ServerPort = Main.CONFIG.get('DATA_SERVER','DATA_PORT')
ServerHost = Main.CONFIG.get('DATA_SERVER','DATA_HOST')
ClientAgentDir = Main.CONFIG.get('AGENT_CONFIG','CLIENT_AGENT_DIR')
CircleTime = int ( Main.CONFIG.get('AGENT_CONFIG','CIRCLE_TIME') )

def InitAgent () :
    for i in HostList :
        Cmd = "ssh -i " + SshKeyFile + " " + UserName + "@" + i[1] +" 'mkdir -p " + ClientAgentDir + " && echo 1' "
        print "Connect to "+ UserName + "@" + i[1] ,
        Ret = os.popen ( Cmd ).read()
        if not Ret.strip() or int(Ret.strip()) != 1 :
            print "[Error Use Init.py]"
            os._exit(0)
        print "[Scccess]"
        Cmd = "scp -i " + SshKeyFile + " " + Main.ROOT_DIR + '/agent/agent.py' +" "+ UserName + "@" + i[1] + ":" + ClientAgentDir
        #print Cmd
        os.popen ( Cmd ).read()

def DoAgent () :
    for i in HostList :
        Cmd = "ssh -i " + SshKeyFile + " " + UserName + "@" + i[1] +" python " + ClientAgentDir + "/agent.py"
        #print Cmd
        WorkerData = {}
        WorkerData['Action']    = 'put'
        WorkerData['HostName']  = i[0]
        WorkerData['HostIp']    = i[1]
        WorkerData['ClientName']= 'Worker'
        print  "Work on "+ UserName + "@" + i[1] ,
        try :
            CmdRes = os.popen( Cmd ).read()
            WorkerData['AgentData'] = json.loads( CmdRes )
            WdS = json.dumps(WorkerData,ensure_ascii=False)
        except :
            print "[Error]"
            continue
        #print WdS
        CliRes = Main.LiSocketClient ( ServerHost, ServerPort, WdS )
        print "[" + CliRes + "]"

if __name__=='__main__' :
    InitAgent ()
    StartTime = 0
    EndTime = 0
    while 1 :
        St = EndTime - StartTime
        if ( StartTime > 0 and St < CircleTime ) :
            print 'waiting:', int( CircleTime - St ), 's'
            time.sleep( CircleTime - St )
        StartTime = time.time()
        #print '正在执行'
        DoAgent ()
        EndTime = time.time()
