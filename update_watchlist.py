#!/usr/bin/env python
# -*- coding: utf-8 -*-
from mangawatcher import db
import sqlite3
if __name__ == '__main__':
    manga_txt = './manga.txt'
    f = open(manga_txt)
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    for line in f:
        [name, url] = line.split('@')
        cur.execute('select url from WatchList where url = ? limit 1;',(url,))
        if cur.fetchone() == None:
            cur.execute('insert into WatchList values (?,?);',(url,name.decode('utf8')))
        else:
            print ("{0} already exsists, url = {1}".format(name, url))
    conn.commit()
    conn.close()
    f.close()

