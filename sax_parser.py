#!/usr/bin/env python
# -*- coding: utf-8 -*-
# парсинг дампа БД "RuTracker.org" xml->csv

import xml.sax
import os, os.path
import sys

D = {}
forums = 'forums.csv'
k = 0
seq=[1,2,4,8,9,10,11,18,19,20,
     22,23,24,25,26,27,28,29,
     31,33,34,35,36]

class TorHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.tid = ''
        self.reg_date = ''
        self.b_size = ''
        self.title = ''
        self.url = ''
        self.magnet = ''
        self.forum_id = ''
        self.forum = ''
        self.contents = ''

   # Call when an element starts
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        global tid,reg_date,b_size,forum_id
        if tag == 'torrent':
            tid = attributes['id']
            reg_date = attributes['registred_at']
            b_size = attributes['size']
        elif tag == 'forum':
            forum_id = attributes['id']
                   
   # Call when an elements ends 
    def endElement(self, tag):
        global magnet,forum,title,k
        if self.CurrentData == 'url':
            pass
        elif self.CurrentData == 'magnet':
            magnet = self.magnet
            magnet = magnet.replace('magnet:?xt=urn:btih:','')
            magnet = magnet.replace('&tr=1','')
            self.magnet = ''
        elif self.CurrentData == 'forum':
            forum = self.forum
            self.forum = ''
        elif tag == 'content':
            #F=open('u'+str(tid)+'.txt','w',encoding='utf-8')
            #F.write(self.contents)
            #F.close()
            self.contents = ''
        elif tag == 'title':
            title = self.title
            self.title = ''
        elif tag == 'torrent':
            k += 1
            sline = '"%s";"%s";"%s";"%s";"%s";"%s";"%s"\n' % (forum_id,forum,tid,magnet,title,b_size,reg_date)
            fileWrite(sline)
            if k == 1000: print(tid); k = 0
        self.CurrentData = ''
        
   # Call when a character is read
    def characters(self, content):
        if self.CurrentData == 'title':
            self.title += content
        elif self.CurrentData == 'url':
            self.url = content
        elif self.CurrentData == 'magnet':
            self.magnet += content
        elif self.CurrentData == 'forum':
            self.forum += content
        elif self.CurrentData == 'content':
            self.contents += content

def fileOpen():
    for i in seq:
        s='F'+str(i)
        if sys.version[0] == '3':
            globals()[s] = open(catalog+'/category_'+str(i)+'.csv','a',encoding = 'utf-8')
        else:
            globals()[s] = open(catalog+'/category_'+str(i)+'.csv','ab')

    
def fileClose():
    for i in seq:
        s='F'+str(i)
        globals()[s].close()


def fileWrite(stroka):
    n = int(D.get(forum_id,0)) 
    if not sys.version[0] == '3':
        st=u''
        st=stroka
        stroka = st.encode('utf-8')
    if n == 0:
        F0 = open(catalog+'/category_0.csv','a',encoding = 'utf-8')
        F0.write(stroka)
        F0.close()
    else:
        globals()['F'+str(n)].write(stroka)
        

def instor(): # insert start and end tags '<torrents>'
    FB = open(backup,'r+b')
    FB.seek(0)
    FB.write(b'<?xml version="1.0"?>\n<torrents>      ')
    FB.close()
    FB = open(backup,'ab')
    FB.write(b'</torrents>')
    FB.close()

def load_forums3():
    # Load dic FORUMS vers 3
    for line in open(forums, encoding = 'utf-8'):
        forum = line.split(sep=';"')[0]
        category = line.split(sep='";')[1]
        D[forum] = category
    print('Dictionary loaded')

def load_forums2():
    # Load dic FORUMS vers 2
    for line in open(forums,'rb').xreadlines():
        xline=line.decode('utf-8')
        forum = xline.split(';"')[0]
        category = xline.split('";')[1]
        D[forum] = category
    print('Dictionary loaded')
    
def test_tor():
    # test for '<torrents>'
    f = open(backup,'rb')
    a = str(f.read(50))
    f.close()
    if a.find('<torrents>') == -1: instor()

    
# START PROG ->
if __name__ == '__main__':
    for f in os.listdir('.'):
        if f[:8] == 'backup.2':
            backup = f
            #break
    	
    period = backup.split(".")[1][:8]
    catalog = './'+period
    if os.path.exists(catalog):
        for f in os.listdir(catalog):
            os.remove(catalog+'/'+f)
    else:
        os.mkdir(catalog)
    
    test_tor()

    if sys.version[0] == '3':
        load_forums3()
    else:
        load_forums2()
    
    # create an XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    
    # override the default ContextHandler
    Handler = TorHandler()
    parser.setContentHandler( Handler )

    fileOpen()
    parser.parse(backup)
    fileClose()
    print('Extract OK!')
