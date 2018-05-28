#!/usr/bin/python

import sys
sys.path.append( os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) ) + "/src" )
import Main

ServerPort = Main.CONFIG.get('DATA_SERVER','DATA_PORT')
ServerHost = Main.CONFIG.get('DATA_SERVER','DATA_HOST')

def DataServer ( Data ) :
    print Data

Main.LiSocketServer ( ServerHost, ServerPort, DataServer )
