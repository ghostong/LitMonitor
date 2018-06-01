#!/usr/bin/python
# -*- coding: utf-8 -*-
import ConfigParser, os, socket

ROOT_DIR = os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) )
CONFIG_FILE = ROOT_DIR+'/litmonitor.conf'
CONFIG = ConfigParser.ConfigParser()
CONFIG.read( CONFIG_FILE )
SSH_KEY_FILE = ROOT_DIR+"/sshkey/litmonitor"

#Socket服务端
def LiSocketServer ( Host, Port, Func ) :
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(( Host, int(Port) ))
    s.listen(100)
    while 1:
        Conn, Addr = s.accept()
        Data = Conn.recv(1024)
        Ret = Func(Data)
        Conn.sendall( Ret )
    Conn.close()
    return True

#Socket客户端
def LiSocketClient ( Host, Port, Cont ) :
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(( Host, int(Port) ))
        s.sendall( Cont )
        Ret = s.recv(1024)
        s.close()
        return Ret
    except :
        return 'Socket connect error'

