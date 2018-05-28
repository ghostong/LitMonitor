#!/usr/bin/python

import sys,os
sys.path.append( os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) ) + "/src" )
import Main

SshKeyFile = Main.SSH_KEY_FILE
HostList   = Main.CONFIG.items("HOST_LIST")
UserName   = Main.CONFIG.get('SSH2_CONFIG','SSH2_USER')
ClientAgentDir = Main.CONFIG.get('AGENT_CONFIG','CLIENT_AGENT_DIR')

for i in HostList :
    Cmd = "ssh -i " + SshKeyFile + " " + UserName + "@" + i[1] +" mkdir -p " + ClientAgentDir
    print Cmd
    os.popen ( Cmd ).read()
    Cmd = "scp -i " + SshKeyFile + " " + Main.ROOT_DIR + '/agent/agent.py' +" "+ UserName + "@" + i[1] + ":" + ClientAgentDir
    print Cmd
    os.popen ( Cmd ).read()
