#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, re, json, time

InfoList = {}

#进程信息
Cmd = 'top -b -n 1 | head -6'
CmdRes = os.popen ( Cmd ).read()
Lines = ''
Line = ''
for Line in CmdRes.splitlines() :
    Lines += Line + ' | '
MatchRes = re.match( r'(.*)up(.*?)\,(.*)Tasks\:(.*?)total\,(.*?)\%?Cpu\(s\)\:(.*?)\%?us,', Lines, re.I )
InfoList['UpTime'] = MatchRes.group(2).strip()
InfoList['Task']   = MatchRes.group(4).strip()
InfoList['Cpu']   = MatchRes.group(6).strip()

#内存信息
Cmd = 'free -m'
CmdRes = os.popen ( Cmd ).read()
Lines = ''
Line = ''
for Line in CmdRes.splitlines() :
    Lines += Line + ' | '
MatchRes = re.match( r'(.*)Mem:(.*?)(\d+)(.*?)(\d+)(.*?)(\d+)(.*?)Swap:(.*?)(\d+)(.*?)(\d+)(.*)', Lines, re.I )
InfoList['MemUse']    = str ( int(MatchRes.group(3)) - int(MatchRes.group(7)) )
InfoList['MemTotal']  = MatchRes.group(3)
InfoList['SwapUse']   = MatchRes.group(12)
InfoList['SwapTotal'] = MatchRes.group(10)

#磁盘信息
Cmd = "df -h |awk {'if ( match($1,\"^/dev\") && length($2) > 0 ) print $NF\":\"$(NF-1)'}"
CmdRes = os.popen( Cmd ).read()
DiskList = {}
for Line in CmdRes.splitlines() :
    Split = Line.split(':')
    DiskList[Split[0]] = Split[1]
InfoList['DiskList'] = DiskList

InfoList['LastTime'] = time.time()

print json.dumps(InfoList,ensure_ascii=False)
