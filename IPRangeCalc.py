#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
Copyright (C),2014-2015, YTC, www.bjfulinux.cn
Created on  2015-09-24 16:40

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

import IPInfo

def ip2num(ip):
    ip = [int(x) for x in ip.split('.')]
    return ip[0]<<24 | ip[1]<<16 | ip[2]<<8 | ip[3]

def num2ip(num):
    return '%s.%s.%s.%s' % ( (num & 0xff000000) >> 24,
                             (num & 0x00ff0000) >> 16,
                             (num & 0x0000ff00) >> 8,
                              num & 0x000000ff
                           )
    
def gen_ip(ip):
    start, end = [ip2num(x) for x in ip.split('-')]
    return [num2ip(num) for num in range(start, end+1) if num & 0xff]

def auto_ip_get(device):
    ip = IPInfo.find_ip(device)
    mask = IPInfo.find_mask(device)
    start=num2ip(ip2num(ip)&ip2num(mask))
    end=num2ip((ip2num(ip)|~ip2num(mask))-1)
    return start+'-'+end
