#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

if __name__ == '__main__':

    for f in os.listdir('.'):
        if f[-3:]=='new':
            os.remove(f)
    for f in os.listdir('.'):
        if f[:8] == 'backup.2':
            backup = f

            
    f_out=open(backup+'.new','a',encoding='utf-8')
    for line in open(backup,'r', encoding = 'utf-8'):
        lineout = line.replace('torrent hash', 'torr hash')
        f_out.write(lineout)

    f_out.close()

    os.remove(backup)
    os.rename(backup+'.new',backup)
