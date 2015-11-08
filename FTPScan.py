#! /usr/bin/python
# -*- coding: utf-8 -*-
'''
Copyright (C),2014-2015, YTC, www.bjfulinux.cn
Created on  2015-09-24 15:11

@author: ytc recessburton@gmail.com
@version: 2.0

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''


import ftplib
import cmd
import sys
import socket
import time
import IPRangeCalc
from IPRangeCalc import auto_ip_get
import MySQLdb
import multiprocessing

manager=multiprocessing.Manager()
IPList=manager.list()

def scan_work(targetIP):
    #global IPList
    print "%s: Scanning %s..." % (time.ctime(),targetIP)
    try:
        ftplib.FTP(targetIP,'anonymous','user@',5).quit()
    except:
        print "%s: %s Closed!" % (time.ctime(),targetIP)
    else:
        print "%s: %s Open!" % (time.ctime(),targetIP)
        IPList.append(targetIP)

class ProcShell(cmd.Cmd):
    u'''Usage：
    scan [IP begin]-[IP end] :To scan in the given IP range
    example: scan 192.168.1.1-192.168.1.100
    
    autoscan [DEVICE] : To scan automatically on DEVICE
    example: autoscan eth0 
    '''
    def __init__(self):
        cmd.Cmd.__init__(self)
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.prompt = ">>"
        self.intro = "     FTP Scanner \nType 'help' for more info."
        
    def do_EOF(self, line):
        return True
    
    def do_help(self, line):
        print self.__doc__
        
    def do_scan(self, line):
        global IPList
        ProcessingList = []
        try:
            (BeginIP, EndIP) = line.split("-")
            socket.inet_aton(BeginIP)
            socket.inet_aton(EndIP)
        except:
            print "Command ERROR! Type 'help for more info.' "
            return
        for targetIP in IPRangeCalc.gen_ip(line): 
            p=multiprocessing.Process(target=scan_work,args=(targetIP,))
            ProcessingList.append(p)
        for p in ProcessingList:
            p.start()
        for p in ProcessingList:
            p.join(timeout=1)
        for p in ProcessingList:
            if p.is_alive():
                p.terminate()
        del(ProcessingList)
        
        print "%s Scan Done!" % (time.ctime())
        if IPList.__len__():
            IPList = list(set(IPList))
            IPList.sort()
            print 'IP:',IPList
            print 'Inserting to MySQL...'
            #Insert into DataBase 
            conn=MySQLdb.connect(host='localhost',user='root',passwd='gaoxiang',port=3306)
            cur=conn.cursor()
            conn.select_db('FTPScan')
            cur.executemany('insert into iptable (ip) values(%s);',IPList)
            conn.commit()
            cur.close()
            conn.close()
            del IPList[:]
        else:
            print "No FTP server scanned!"
        print "All Done."
        return
    
    def do_autoscan(self, line):
        try:
            if not line.strip():
                print "Command ERROR! Type 'help for more info.' "
                return
        except:
            print "Command ERROR! Type 'help for more info.' "
            return
        ipstring = auto_ip_get(line)
        self.do_scan(ipstring)
        return

if __name__ == "__main__": 
    shell = ProcShell()
    shell.cmdloop()
    