#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (C),2014-2015, YTC, www.bjfulinux.cn
Created on  2015-09-25 12:17

@author: ytc recessburton@gmail.com
@version: 1.0

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

import subprocess
import re
import platform

def find_ip(device):
    ipstr = '([0-9]{1,3}\.){3}[0-9]{1,3}'
    system = platform.system()
    if system == "Darwin" or system == "Linux":
        ipconfig_process = subprocess.Popen("ifconfig",stdout=subprocess.PIPE)
        output = ipconfig_process.stdout.read()
        ip_pattern = re.compile('(inet %s)' % ipstr)
        if system == "Linux":
            ip_pattern = re.compile('%s.*\n.*inet .*:%s' % (device,ipstr))
        pattern = re.compile(ipstr)
        iplist = []
        for ipaddr in re.finditer(ip_pattern, str(output)):
            ip = pattern.search(ipaddr.group())
            if ip.group() != "127.0.0.1":
                iplist.append(ip.group())
        return iplist[0]
    elif system == "Windows":
        ipconfig_process = subprocess.Popen("ipconfig", stdout=subprocess.PIPE)
        output = ipconfig_process.stdout.read()
        ip_pattern = re.compile("IPv4 Address(\. )*: %s" % ipstr)
        pattern = re.compile(ipstr)
        iplist = []
        for ipaddr in re.finditer(ip_pattern, str(output)):
            ip = pattern.search(ipaddr.group())
            if ip.group() != "127.0.0.1":
                iplist.append(ip.group())
        return iplist[0]
 
 
def find_mask(device):
    ipstr = '255\.([0-9]{1,3}\.){2}[0-9]{1,3}'
    system = platform.system()
    maskstr = '0x([0-9a-f]{8})'
    if system == "Darwin" or system == "Linux":
        ipconfig_process = subprocess.Popen("ifconfig", stdout=subprocess.PIPE)
        output = ipconfig_process.stdout.read()
        mask_pattern = re.compile('(inet %s)' % maskstr)
        pattern = re.compile(maskstr)
        if system == "Linux":
            mask_pattern = re.compile(r'%s.*\n.*掩码:%s' % (device,ipstr))
            pattern = re.compile(ipstr)
        masklist = []
        for maskaddr in mask_pattern.finditer(str(output)):
            mask = pattern.search(maskaddr.group())
            if mask.group() != '0xff000000' and mask.group() != '255.0.0.0':
                masklist.append(mask.group())
        return masklist[0]
    elif system == "Windows":
        ipconfig_process = subprocess.Popen("ipconfig", stdout=subprocess.PIPE)
        output = ipconfig_process.stdout.read()
        mask_pattern = re.compile(r"Subnet Mask (\. )*: %s" % ipstr)
        pattern = re.compile(ipstr)
        masklist = []
        for maskaddr in mask_pattern.finditer(str(output)):
            mask = pattern.search(maskaddr.group())
            if mask.group() != '255.0.0.0':
                masklist.append(mask.group())
        return masklist[0]