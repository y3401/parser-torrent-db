#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
''' Парсинг дампа БД "RuTracker.org" xml->csv + sqlite3

    Описание обрабатываемого формата XML:

<torrent id="{ID топика}" registred_at="{Дата регистрации в формате Y.[*]m.d H:i:s}" size="{Размер раздачи в байтах}">
    <title>{Название раздачи}</title>
    <torrent hash="{Инфохеш}" tracker_id="{Номер трекера}"/>
    <forum id="{ID форума}">{Название форума с категориями}</forum>
    <content>{Оформление раздачи}</content>
    <dir name="{Имя каталога}">
        <file size="{Размер в байтах}" name="{Имя файла}/>
    </dir>
    <dup p="{Уверенность в процентах}" id="{ID топика возможного дубля}">{Заголовок возможного дубля}</dup>
</torrent>

    Тэги <dir>, <file>, <dup>, а также атрибут 'tracker_id' в этом скрипте игнорируются.

    Обрабатываемый файл должен именоваться по маске "backup.YYYYMMDD*.xml",
например: "backup.20180721.xml"

    Режимы работы:
 1 - Сохранение в CSV:        разбирает исходный файл на текстовые файлы по категориям.
                              Описание формата:
                                  category_info.csv: 
                                      "ID категории";"Название категории";"Файл с раздачами"
                                  category_*.csv:
                                      "ID форума";"Название форума";"ID раздачи";"Info hash";"Название раздачи";"Размер в байтах","Дата регистрации торрента"

 2 - Сохранение в БД(sqlite): выборка и сохрание раздач в БД формата sqlite3 (файл "torrents.db3").
                              БД содержит справочник категорий, справочник форумов и список раздач без
                              описаний (как и в CSV).

 3 - Сохранение описания
     раздач в отдельную БД:   дополнительно создается БД для записи "Оформления раздач" (тэг <content>).
                              Данные упаковываются архиватором для уменьшения размера файла.
 4 - Выход

    Названия форумов и принадлежность к конкретным категориям берутся из исходного файла. Внешний файл "forums.csv" не нужен. 
'''
import xml.sax
import os, os.path
import sys
import modsql3 as lite
import zipfile
import time

D = {}
Dn = {}
List=[]
forums = 'forums.csv'
k = 0
seq=[1,2,4,8,9,10,11,18,19,20,
     22,23,24,25,26,27,28,29,
     31,33,34,35,37]    
time_begin = 0  
time_end = 0    
CAT_INV = {}
fr = ''

class TorHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.tid = ''
        self.reg_date = ''
        self.b_size = ''
        self.title = ''
        self.magnet = ''
        self.forum_id = ''
        self.forum = ''
        self.contents = ''
        self.levl = 0
        
   # Call when an element starts
    def startElement(self, tag, attributes):
        global tid, reg_date, b_size, forum_id, magnet
        self.CurrentData = tag
        if tag == 'torrent':
            if self.levl == 0:
                tid = attributes['id']
                reg_date = attributes['registred_at']
                b_size = attributes['size']
            elif self.levl == 1:
                magnet =  attributes['hash']
        elif tag == 'forum':
            forum_id = attributes['id']
                   
   # Call when an elements ends 
    def endElement(self, tag):
        global forum, title, k, contents
        if tag == 'forum':
            forum = self.forum
            forum=forum.replace('"',"'")
            self.forum = ''
        elif tag == 'content':
            contents = self.contents
            self.contents = ''
            self.levl=2
        elif tag == 'title':
            title = self.title
            title=title.replace('"',"'")
            self.title = ''
            self.levl = 1
        if self.levl==2 and tag == 'torrent':
            self.levl=0
            k += 1
            n=CAT_INV.get(forum.split(sep=" - ")[0],0)
            fr=forum.split(sep=" - ")[-1]
            if un == '1':
                sline = '"%s";"%s";"%s";"%s";"%s";"%s";"%s"\n' % (forum_id,fr,tid,magnet,title,b_size,reg_date)
                fileWrite(sline,n)
            else:
                lite.check_podr(forum_id,fr,n)
                lite.ins_tor(forum_id,tid,magnet,title,b_size,reg_date)
                if un == '3':
                    lite.ins_content(tid,contents)
            if k%1000==0:
                if un != '1': lite.dbc()
                print(k) #tid
                #k = 0
        self.CurrentData = ''
        
   # Call when a character is read
    def characters(self, content):
        if self.CurrentData == 'title':
            self.title += content
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
    
    F_info=open(catalog+'/category_info.csv','w',encoding = 'utf-8')    # пока для 3-й версии
    for ctg in sorted(lite.CAT):
        catline='"%s";"%s";"category_%s.csv"\n' % (ctg[0],ctg[1],ctg[0])
        F_info.write(catline)
    F_info.close()

#"ID категории";"Название категории";"Файл с раздачами"
    
def fileClose():
    for i in seq:
        s='F'+str(i)
        globals()[s].close()


def fileWrite(stroka,n):
     
    if not sys.version[0] == '3':
        st=u''
        st=stroka
        stroka = st.encode('utf-8')
    if n == 0:
        F0 = open(catalog+'/cat_0000.csv','a',encoding = 'utf-8')
        F0.write(stroka)
        F0.close()
    else:
        if un != '0':
            globals()['F'+str(n)].write(stroka)
        
'''def load_forums3():                           Список форумов берется из конвертируемого файла
    # Load dic FORUMS vers 3
    for line in open(forums, encoding = 'utf-8'):
        forum = line.split(sep=';"')[0]
        category = line.split(sep='";')[1]
        name_forum=line.split(sep=';"')[1].split(sep='";')[0]
        D[forum] = category
        Dn[forum] = name_forum
        List.append((int(forum),name_forum,int(category)))
        
def load_forums2():
    # Load dic FORUMS vers 2
    for line in open(forums,'rb').xreadlines():
        xline=line.decode('utf-8')
        L=xline.split(sep=';')
        forum = xline.split(';"')[0]
        category = xline.split('";')[1]
        name_forum=line.split(sep=';"')[1].split(sep='";')[0]
        D[forum] = category
        Dn[forum] = name_forum
        List.append((int(forum),name_forum,int(category)))
'''    
def invers_category():
    for la in lite.CAT:
        CAT_INV[la[1]]=la[0]

	

# START PROG ->
if __name__ == '__main__':
    global un
    
    for f in os.listdir('.'):
        if f[:8] == 'backup.2':
            backup = f
            #break
    	
    period = backup.split(".")[1][:8]
    catalog = './'+period
    dirDB = 'C://DB'
    print('Обрабатываемый файл: ' + backup)

    un = input('''Выберите нужное действие:
    1. Сохранить в CSV;
    2. Сохранить в БД(sqlite);
    3. Сохранить описания раздач в отдельную БД(дополнительно, со сжатием);
    4. Выход (любой ввод кроме 1,2,3)\n''')

    if un in ('1','2','3'):
        time_begin=time.time()
        '''if sys.version[0] == '3':
            load_forums3()
        else:
            load_forums2()
        print('Dictionary loaded')'''

        invers_category()
        
        if un in ('1'):
            if os.path.exists(catalog):
                for f in os.listdir(catalog):
                    os.remove(catalog+'/'+f)
            else:
                os.mkdir(catalog)
        elif un in ('2','3'):
            if not os.path.exists(dirDB):
                os.mkdir(dirDB)
            lite.create_db(dirDB+'/')                               # Исключено: lite.ins_forums(List) 
            if un == '3':
                lite.create_db_content(dirDB+'/')
            lite.ins_vers(period)
        

        parser = xml.sax.make_parser()                              # create an XMLReader
        parser.setFeature(xml.sax.handler.feature_namespaces, 0)    # turn off namepsaces
        Handler = TorHandler()                                      # override the default ContextHandler
        parser.setContentHandler( Handler )

        if backup[-3:]=='zip':
            print('ZIP')
            backup=zipfile.ZipFile(backup).extract(backup[:-3]+'xml')
            
        if un == '1':
            fileOpen()
            
        parser.parse(backup)
        
        if un == '1':
            fileClose()
        else:
            lite.dbc()
            lite.close_db()
        print (k)
        time_end=time.time()
        tsec=time_end-time_begin
        stsec=(str(tsec)).split('.')
        tsec=int(stsec[0])
        seconds=0
        minutes=0
        hours=0
        n=0
        seconds=tsec % 60
        minutes=(tsec//60) % 60
        hours=(tsec//3600) % 24
        print('Extract OK!')
        print('Затраченное время - %s:%s:%s' % (str(hours),('0'+str(minutes))[-2:],('0'+str(seconds))[-2:]))

    else:
        print('Goodbye!')
