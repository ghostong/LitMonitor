#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys, os, json, time
sys.path.append( os.path.dirname( os.path.dirname( os.path.realpath(__file__) ) ) + "/src" )
import Main

ServerPort = Main.CONFIG.get('DATA_SERVER','DATA_PORT')
ServerHost = Main.CONFIG.get('DATA_SERVER','DATA_HOST')
ColumeOrder= Main.CONFIG.get('CMDUI_CONFIG','COLUMN_ORDER').split(',')
UiFlushTime= Main.CONFIG.get('CMDUI_CONFIG','UI_FLUSH_TIME')

def GetMoniData () :
    Data = {}
    Data['Action'] = 'get'
    Data['ClientName'] = 'CmdUi'
    WdS = json.dumps(Data,ensure_ascii=False)
    ServerJson = Main.LiSocketClient ( ServerHost, ServerPort, WdS )
    try :
        ServData = json.loads( ServerJson )
    except :
        print ServerJson
        os._exit(0)
    return ServData

def DataForMat ( Data ) :
    NewData = {}
    Title = {'Name':'Name','Ip':'Ip','Cpu':'Cpu','Mem':'Mem','Swap':'Swap','Task':'Task','Disk':'Disk','Time':'Time'}
    NewData['Title'] = Title
    for i in Data :
        d = Data[i]
        Disk = ','.join( d['AgentData']['DiskList'].values() )
        Time = time.strftime( "%H:%M:%S", time.localtime( d['AgentData']['LastTime'] ) )
        Tmp = { \
                'Name':d['HostName'],'Ip':d['HostIp'],'Cpu':d['AgentData']['Cpu']+'%',\
                'Mem':d['AgentData']['MemUse']+'M/'+d['AgentData']['MemTotal']+'M',\
                'Swap':d['AgentData']['SwapUse']+'M/'+d['AgentData']['SwapTotal']+'M',\
                'Task':d['AgentData']['Task'],'Disk':Disk,'Time':Time\
                }
        NewData[i] = Tmp
    return NewData

def ColumnCalc ( Data ) :
    NewData = {}
    for i in Data.values() :
        for j in i :
            NewData[j] = len(i[j]) if ( len(i[j]) > NewData.get(j,0) ) else NewData.get(j,0)
    return NewData

def BuildTopLine ( Data ) :
    RowLen = ( len( Data ) - 1 ) * 3 + 4 + sum ( Data.values() ) - 2
    Line = '+' + ('-'*RowLen) + '+'
    return Line

def BuildDataLine ( Data ) :
    Tmp = []
    EndStr = '| '
    for i in ColumeOrder :
        TitleLen = len(Data[i])
        Half = int(( ColuCalc[i] - TitleLen ) / 2)
        Tmp.append(' '*Half + Data[i] + ' '*( ColuCalc[i]- TitleLen - Half))
    EndStr += ' | '.join( Tmp )
    EndStr += ' |'
    return EndStr

def PrintScreen ( ColuCalc, ForMatRes ) :
    os.system('clear')
    Line = BuildTopLine(ColuCalc)
    OutStr = Line + "\n"
    OutStr += BuildDataLine ( ForMatRes['Title'] )  + "\n"
    OutStr += Line + "\n"
    ForMatRes.pop('Title')
    for i in ForMatRes :
        OutStr += BuildDataLine ( ForMatRes[i] )  + "\n"
    OutStr += Line  + "\n"
    print OutStr

if __name__=='__main__' :
    while 1 :
        try:
            MoniData  = GetMoniData()
            ForMatRes = DataForMat( MoniData )
            ColuCalc  = ColumnCalc( ForMatRes )
            PrintScreen ( ColuCalc , ForMatRes )
            for i in range( int(UiFlushTime) - 1, -1, -1 ) :
                NowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                sys.stdout.write( "litmonitor:v0.01        Waiting:"+ str(i) + '        [' + NowTime +']'+"\r" )
                sys.stdout.flush()
                time.sleep (1)
        except KeyboardInterrupt :
            print '\n\nUser exit !'
            os._exit(0)
        except :
            os._exit(0)
