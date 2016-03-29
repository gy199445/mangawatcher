#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2,socket,urllib,sqlite3,re,argparse
from urllib2 import URLError
from HTMLParser import HTMLParser
from pushbullet import Pushbullet
from pushbullet_key import api_key
import os

#set up
urls=['m.seemh.com/comic/16739/',]
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
headers = {'User-Agent':user_agent}
db = './manga.db'
pb = Pushbullet(api_key)

def db_init():
    schema = """
        CREATE TABLE WatchList IF NOT EXISTS(
        url TEXT NOT NULL,
        name TEXT NOT NULL);
        CREATE TABLE Episode IF NOT EXSITS(
        url TEXT NOT NULL,
        name text NOT NULL
        );
        """

    con = sqlite3.connect(db)
    c = con.cursor()
    c.executescript(schema)
    con.commit()
    conn.close()

def search_episode(page):
    '''
    return episode names and urls(partial)
    '''
    chapter_block = r'<div class="chapter-list" id="chapterList"><ul>(.*?)</ul></div>'
    episode_block = r'<a href="(.*?)"><b>(.*?)</b>(?:<i class="new-icon"></i>){0,1}</a>'
    chapter_pattern = re.compile(chapter_block)
    episode_pattern = re.compile(episode_block)
    chapter = chapter_pattern.findall(page)
    episode = episode_pattern.findall(chapter[0])
    return episode

if __name__ == '__main__':
    #set current folder as working directory
    os.chdir(os.getcwd())
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-u","--update",action='store_true',help='Do not push, just update the watched episodes')
    args = argparser.parse_args()
    timeout = 10
    socket.setdefaulttimeout(timeout)
    con = sqlite3.connect(db)
    c = con.cursor()
    con_tmp = sqlite3.connect(":memory:")
    c_tmp = con_tmp.cursor()
    c_tmp.execute("create table tmp (url text, episode text, manga_name text);")
    while True:
        for row in c.execute('select url,name from WatchList;'):
            try:
                print row
                request = urllib2.Request(row[0],None,headers)
                response = urllib2.urlopen(request)
                page = response.read()
                episode = search_episode(page)
                for e in episode:
                    #save to tmp table
                    c_tmp.execute("insert into tmp values(?,?,?)",(e[0].decode('utf8'),e[1].decode('utf8'), row[1]))
            except URLError as e:
                print e.reason
        else:
            break
    #check if pushed
    c_tmp.execute("select * from tmp")
    while True:
        episode_tmp = c_tmp.fetchone()
        if episode_tmp != None:
            c.execute("select url from Episode where url=? limit 1;",(episode_tmp[0],))
            if c.fetchone() == None:
                #new episode spotted
                full_url = "m.seemh.com"+episode_tmp[0]
                if not args.update: 
                    push = pb.push_link("New episode from m.seemh.com!",full_url)
                c.execute("insert into episode values (?,?)",(episode_tmp[0],episode_tmp[1]))
        else:
            break
    con.commit()
    con.close()
