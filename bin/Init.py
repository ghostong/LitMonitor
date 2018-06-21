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
    print "Build ssh keygen !" ,
    Cmd = "ssh-keygen -t rsa -q -N '' -f "+SshKeyFile
    RunStatus = os.system ( Cmd )
    if RunStatus == 0 :
        print ": Success "
    else :
        print ": Error "
else :
    print "SSH keygen "+SshKeyFile + " exists !"

UserName = Main.CONFIG.get('SSH2_CONFIG','SSH2_USER')
print "UserName: " + UserName
PassWord = raw_input("PassWord: ")

HostList = Main.CONFIG.items("HOST_LIST")
for i in HostList :
    print "+-----------------"
    Cmd = "sshpass -p "+PassWord+" ssh -o StrictHostKeyChecking=no -i "+SshKeyFile+" "+UserName+"@"+i[1] + " echo 1 > /dev/null 2>&1";
    print "|- ssh-connect to " + UserName+"@"+i[1] ,
    RunStatus = os.system ( Cmd )
    if RunStatus == 0 :
        print ": Success "
    else :
        print ": Error "
    Cmd = "sshpass -p "+PassWord+" ssh-copy-id -i "+SshKeyFile+" "+UserName+"@"+i[1]+" > /dev/null 2>&1";
    print "|- ssh-copy-id to " + UserName+"@"+i[1] ,
    RunStatus = os.system ( Cmd )
    if RunStatus == 0 :
        print ": Success "
    else :
        print ": Error "
print "+-----------------"
