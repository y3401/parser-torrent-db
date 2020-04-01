#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Выгрузка из DB SQLite3 в CSV с сортировкой по возрастанию file_id

import sqlite3
import os, os.path

seq=[1,2,4,8,9,10,11,18,19,20,22,23,24,25,26,27,28,29,31,33,34,35,37]

dirDB = 'C://DB/'


def DBvers(dirdb=''):
    global period
    DB=sqlite3.connect(dirdb + 'torrents.db3')
    c=DB.cursor()
    c.execute('SELECT vers from vers')
    row=c.fetchall()
    if len(row) != 0:
        period = row[0][0]
    else:
        period= 'export'
    c.close()
    DB.close()
    return(period)

def DBExport(dirdb='',category=0):
    DB=sqlite3.connect(dirdb + 'torrents.db3')
    c=DB.cursor()
    c.execute("""
    SELECT file_id,hash_info,title,size_b,date_reg,forum_id,name_forum
    FROM torrent t inner join forum f on t.forum_id=f.code_forum
    WHERE category_id=?
    ORDER BY file_id;""", (category,))

    F = open(dirdb+period+'/category_'+str(category)+'.csv','w',encoding = 'utf-8')    

    for row in c.fetchall():
        file_id=row[0]
        hash_info=row[1]
        title=row[2][:254]
        size_b=row[3]
        date_reg=row[4]
        forum_id=row[5]
        name_forum=row[6]
        S = '"%s";"%s";"%s";"%s";"%s";"%s";"%s"\n' % (forum_id,name_forum,file_id,hash_info,title,size_b,str(date_reg))
        F.write(S)

    F.close()
    c.close()
    DB.close()
    print('>> category_'+str(category)+'.csv')

def expCategory(dirdb=''):
    DB=sqlite3.connect(dirdb + 'torrents.db3')
    c=DB.cursor()
    c.execute("""
    SELECT code_category,name_category
    FROM category ORDER BY code_category;""")

    F = open(dirdb+period+'/category_info.csv','w',encoding = 'utf-8')    

    for row in c.fetchall():
        code_cat=row[0]
        name_cat=row[1]

        S = '"%s";"%s";"category_%s.csv"\n' % (code_cat,name_cat,str(code_cat))
        F.write(S)

    F.close()
    c.close()
    DB.close()
    print('>> category_info.csv')

def expForums(dirdb=''):
    DB=sqlite3.connect(dirdb + 'torrents.db3')
    c=DB.cursor()
    c.execute("""
    SELECT code_forum,name_forum,category_id
    FROM forum ORDER BY category_id,code_forum;""")

    F = open(dirdb+period+'/forums.csv','w',encoding = 'utf-8')    

    for row in c.fetchall():
        code_forum=row[0]
        name_forum=row[1]
        code_cat=row[2]

        S = '%s;"%s";%s\n' % (code_forum,name_forum,code_cat)
        F.write(S)

    F.close()
    c.close()
    DB.close()
    print('>> forums.csv')

if __name__ == '__main__':
    period=DBvers(dirDB)
    catalog = dirDB + period
    print(catalog)
    if not os.path.exists(catalog):
        os.mkdir(catalog)
    for i in seq:
        DBExport(dirDB,i)
    expCategory(dirDB)
    expForums(dirDB)
    print('Ok!')
