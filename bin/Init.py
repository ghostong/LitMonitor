#!/usr/bin/python

import sys, os
sys.path.append( os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) ) + "/src" )
import Main

Cmd = "which sshpass"
CmdRes = os.popen ( Cmd ).read()
if not CmdRes :
    print "Install sshpass by yum or apt-get"
    os._exit(0)

SshKeyFile = Main.SSH_KEY_FILE

if not os.path.isfile( SshKeyFile ) :
    Cmd = "ssh-keygen -t rsa -q -N '' -f "+SshKeyFile
    print Cmd
    print os.popen ( Cmd ).read()
else :
    print "File "+SshKeyFile + " exists"

UserName = Main.CONFIG.get('SSH2_CONFIG','SSH2_USER')
PassWord = raw_input("PassWord: ")

HostList = Main.CONFIG.items("HOST_LIST")
for i in HostList :
    Cmd = "sshpass -p "+PassWord+" ssh-copy-id -i "+SshKeyFile+" "+UserName+"@"+i[1] +" -o StrictHostKeyChecking=no";
    print Cmd
    print os.popen ( Cmd ).read()
