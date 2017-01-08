#!/usr/bin/env python
# -*- coding: utf-8 -*-
# модуль записи "RuTracker.org" xml в БД sqlite3

import sqlite3, zlib

def create_db(dirdb=''):    #Создание базы и заполнение таблицы категорий
    global DB
    DB=sqlite3.connect(dirdb + 'torrents.db3')
    cur=DB.cursor()
    CAT=[(1,'Обсуждения, встречи, общение'), (2,'Кино, Видео и ТВ'), (4,'Новости'),
         (8,'Музыка'), (9,'Программы и дизайн'), (10,'Обучающее видео'), (11,'Разное'),
         (18,'Сериалы'), (19,'Игры'), (20,'Документалистика и юмор'), (22,'Рок-музыка'),
         (23,'Электронная музыка'), (24,'Все по авто и мото'), (25,'Книги и журналы'),
         (26,'Apple'), (27,'Медицина и здоровье'), (28,'Спорт'), (29,'Мобильные устройства'),
         (31,'Джазовая и Блюзовая музыка'), (33,'Аудиокниги'), (34,'Обучение иностранным языкам'),
         (35,'Популярная музыка'), (36,'ОБХОД БЛОКИРОВОК')]
    
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS razd
    (id_razd INTEGER PRIMARY KEY AUTOINCREMENT,
    kod_cat INTEGER UNIQUE,
    name_cat TEXT NOT NULL);

    CREATE TABLE IF NOT EXISTS podr
    (id_podr INTEGER PRIMARY KEY AUTOINCREMENT,
    kod_cat INTEGER DEFAULT 0,
    podr_number INTEGER UNIQUE,
    podr_name TEXT NOT NULL);

    CREATE TABLE IF NOT EXISTS torrent
    (id_torrent INTEGER PRIMARY KEY AUTOINCREMENT,
    razd_id INTEGER,
    podr_id INTEGER,
    file_id INTEGER UNIQUE,
    hash_info TEXT,
    title TEXT,
    size_b INTEGER,
    date_reg NUMERIC);
    """)

    cur.executescript("""DELETE FROM razd; DELETE FROM podr; DELETE FROM torrent;""")
    cur.executemany('INSERT INTO razd(kod_cat,name_cat) VALUES (?, ?);', CAT)
    dbc()
    cur.close()

def create_db_content(dirdb=''): # Создание доп. БД для хранения описаний раздач
    global DB1
    DB1=sqlite3.connect(dirdb + 'content.db3')
    cur=DB1.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS cont
    (id_cont INTEGER PRIMARY KEY AUTOINCREMENT,
    id_tor INTEGER UNIQUE,
    content NONE NOT NULL);
    DELETE FROM cont;
    """)
    cur.close()
    
def dbc():
    try:
        DB.commit()
        DB1.commit()
    except:
        pass
    
def ins_forums(lists):
    for LLL in lists:
        try:
            DB.execute('INSERT INTO podr(podr_number,podr_name,kod_cat) VALUES (?, ?, ?);', LLL)
        except:
            pass
    DB.commit()

def check_podr(kod_podr,name_podr):
    c=DB.cursor()
    c.execute('SELECT * FROM podr WHERE podr_number=?', (kod_podr,))
    row=c.fetchall()
    if len(row) == 0:
        c.execute('INSERT INTO podr(podr_number,podr_name,kod_cat) VALUES (?,?,0)', (kod_podr,name_podr))
    else:
        pass

def ins_tor(id_razd,id_podr,id_file,hash_info,title,size_b,date_reg):
    TOR=[(id_razd,id_podr,id_file,hash_info,title,size_b,date_reg)]
    try:
        DB.executemany('INSERT INTO torrent(razd_id,podr_id,file_id,hash_info,title,size_b,date_reg) VALUES (?,?,?,?,?,?,?);', TOR)
    except:
        dbc()

def ins_content(id_tor, cont):
    C = zlib.compress(cont.encode())
    try:
        DB1.execute('INSERT INTO cont(id_tor,content) SELECT ?,?', (id_tor,C))
    except:
        dbc()

def sel_content(id_tor, dirdb=''):
    print('#'*80)
    DB1=sqlite3.connect(dirdb + 'content.db3')
    cur=DB1.cursor()
    row=cur.execute('SELECT content FROM cont WHERE id_tor=?;', (id_tor,))
    r=tuple(row)
    if len(r) != 0:
        S=zlib.decompress(r[0][0])
        print('========== Информация по %s ===========: \n %s ' % (id_tor, S.decode()))
    else:
        print('========== Нет информации по %s ========== \n' % (id_tor))
    
    cur.close()
    DB1.close()
    
    
def close_db():
    try:
        #DB.execute('vacuum')
        DB.close()
        #DB1.execute('vacuum')
        DB1.close()
    except:
        pass

if __name__ == '__main__':
    create_db()
    ins_tor(1,2,3,'hash','title',12345,'2017.01.07 15:17:00')
    ins_tor(1,2,4,'hash','title',12345,'2016.01.06 15:17:00')
    create_db_content()
    ins_content(3,'''Текст описания '''*100)
    dbc()
    sel_content(3)
    DB.close()
