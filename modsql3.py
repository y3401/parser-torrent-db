#!/usr/bin/env python
# -*- coding: utf-8 -*-
# модуль записи "RuTracker.org" xml в БД sqlite3

import sqlite3, zlib,re
import modbbcode

CAT=[(1,'Обсуждения, встречи, общение'), (2,'Кино, Видео и ТВ'), (4,'Новости'),
     (8,'Музыка'), (9,'Программы и Дизайн'), (10,'Обучающее видео'), (11,'Разное'),
     (18,'Сериалы'), (19,'Игры'), (20,'Документалистика и юмор'), (22,'Рок-музыка'),
     (23,'Электронная музыка'), (24,'Все по авто и мото'), (25,'Книги и журналы'),
     (26,'Apple'), (27,'Медицина и здоровье'), (28,'Спорт'), (29,'Мобильные устройства'),
     (31,'Джазовая и Блюзовая музыка'), (33,'Аудиокниги'), (34,'Обучение иностранным языкам'),
     (35,'Популярная музыка'), (37,'Hi-Res форматы, оцифровки')]

def create_db(dirdb=''):    #Создание базы и заполнение таблицы категорий
    global DB,CAT
    DB=sqlite3.connect(dirdb + 'torrents.db3')
    cur=DB.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS "category"
    ("code_category" smallint NOT NULL PRIMARY KEY,
    "name_category" varchar(50) NOT NULL,
    "load_category" bool NOT NULL);

    CREATE TABLE IF NOT EXISTS "forum"
    ("code_forum" smallint NOT NULL PRIMARY KEY,
    "name_forum" varchar(80) NOT NULL,
    "category_id" smallint NOT NULL REFERENCES "category" ("code_category"));

    CREATE INDEX IF NOT EXISTS "forum_category_id_48a15a32" ON "forum" ("category_id");

    CREATE TABLE IF NOT EXISTS "torrent"
    ("file_id" integer NOT NULL PRIMARY KEY,
    "hash_info" varchar(40) NOT NULL,
    "title" varchar(255) NOT NULL,
    "size_b" integer NOT NULL,
    "date_reg" varchar(20) NOT NULL,
    "forum_id" smallint NOT NULL REFERENCES "forum" ("code_forum"));

    CREATE INDEX IF NOT EXISTS "torrent_forum_id_b67937c0" ON "torrent" ("forum_id");

    CREATE TABLE IF NOT EXISTS "vers"
    ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    "vers" varchar(8) NOT NULL);
    """)

    cur.executescript("""DELETE FROM category; DELETE FROM forum; DELETE FROM torrent;""")
    cur.executemany('INSERT INTO category(code_category,name_category,load_category) VALUES (?, ?, 1);', CAT)
    dbc()
    cur.close()

def create_db_content(dirdb=''): # Создание доп. БД для хранения описаний раздач
    global DB1
    DB1=sqlite3.connect(dirdb + 'content.db3')
    cur=DB1.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS "contents"
    ("tid" integer NOT NULL PRIMARY KEY,
    "cont" text NOT NULL);

    DELETE FROM contents;
    """)
    cur.close()
    
def dbc():
    try:
        DB.commit()
        DB1.commit()
    except:
        pass
'''    
def ins_forums(lists):
    for LLL in lists:
        try:
            DB.execute('INSERT INTO forum(code_forum,name_forum,category_id) VALUES (?, ?, ?);', LLL)
        except:
            pass
    DB.commit()
'''
def ins_vers(dt):
    DB.execute('INSERT INTO vers(vers) VALUES (?);', (dt,))
    DB.commit()
    
def check_podr(kod_podr,name_podr,cat_id):
    c=DB.cursor()
    c.execute('SELECT * FROM forum WHERE code_forum=?', (kod_podr,))
    row=c.fetchall()
    if len(row) == 0:
        c.execute('INSERT INTO forum(code_forum,name_forum,category_id) VALUES (?,?,?)', (kod_podr,name_podr,cat_id))
    else:
        pass

def ins_tor(id_podr,id_file,hash_info,title,size_b,date_reg):
    TOR=[(id_podr,id_file,hash_info,title,size_b,date_reg)]
    try:
        DB.execute('INSERT INTO torrent(forum_id,file_id,hash_info,title,size_b,date_reg) SELECT ?,?,?,?,?,?;', (id_podr,id_file,hash_info,title,size_b,date_reg))
    except:
        dbc()

def ins_content(id_tor, cont):
    C = zlib.compress(cont.encode())
    try:
        DB1.execute('INSERT INTO contents(tid,cont) SELECT ?,?', (id_tor,C))
    except:
        dbc()

def sel_content(id_tor, dirdb=''):
    print('#'*80)
    DB1=sqlite3.connect(dirdb + 'content.db3')
    cur=DB1.cursor()
    row=cur.execute('SELECT cont FROM contents WHERE tid=?;', (id_tor,))
    r=tuple(row)
    if len(r) != 0:
        S=zlib.decompress(r[0][0])
        modbbcode.bbcode2html(S.decode('utf-8'))
        #print('========== Информация по %s ===========: \n %s ' % (id_tor, S.decode()))
    else:
        print('========== Нет информации по %s ========== \n' % (id_tor))
    
    cur.close()
    DB1.close()

def test():
    dl=0
    DIC={}
    DB=sqlite3.connect('DB/torrents.db3')
    cur=DB.cursor()
    cur.execute('select title,file_id from torrent')
    for row in cur.fetchall():
        title=row[0]
        file_id=row[1]
        L=set(re.split('\d|\W+',title))
        for word in L:
            if word!='' and len(word)>2:
                try:
                    DIC[word.upper()]+=[file_id]
                except:
                    DIC[word.upper()]=[file_id]
            #if len(word)>dl:
            #    dl=len(word)
            #    maxword=word
    n=0
    for key in sorted(DIC):
        DB.execute('INSERT INTO "links"(word, links) SELECT ?, ?;', (str(key),'{}'.format(DIC[key])) )
        n+=1
        if n>10000:
            DB.commit()
            n=0
    DB.commit()
    #print(ins)
    cur.close()
    DB.close()
    print('Все!')
    
    
def close_db():
    try:
        #DB.execute('vacuum')
        DB.close()
        #DB1.execute('vacuum')
        DB1.close()
    except:
        pass

if __name__ == '__main__':
#    create_db()
#    ins_tor(2,3,'hash','title',12345,'2017.01.07 15:17:00')
#    ins_tor(2,4,'hash','title',12345,'2016.01.06 15:17:00')
#    create_db_content()
#    ins_content(3,'''Текст описания '''*100)
    dbc()
#    sel_content(3)
#   DB.close()
    #test()

