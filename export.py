#! /usr/bin/python
import sqlite3
import sys
import pdb

con = sqlite3.connect('places.sqlite')
f = open('test2.org', 'w')
cur = con.cursor()

cur.execute("SELECT moz_bookmarks.id, parent, position, url, content, moz_bookmarks.title, anno_attribute_id FROM moz_bookmarks LEFT JOIN moz_places ON moz_bookmarks.fk = moz_places.id LEFT JOIN moz_items_annos ON moz_bookmarks.id = moz_items_annos.item_id WHERE ifnull(anno_attribute_id, -1) in (-1, 1, 8, 9) AND parent > 1 ORDER BY parent, position;")
rows = cur.fetchall()

#pdb.set_trace()

def folder(a,b,c,d):

    if d == 8:
        return True
    
    if a <> None:
        return False

    if b <> None:
        return False

    if c == None:
        return False

    return True

def stars(depth):
    a = ""
    for i in range(1, depth):
        a = a + '*'

    return a + "* "

def rss(a):
    if a == 9:
        return True
    return False

def content(a,b,c,d):

    if rss(d):
        return '#' + b
    
    if a <> None:
        return a

    if b <> None:
        return b

    return c

def read(index, title, depth):
    f.write(stars(depth) + title + "\n")
    f.write(stars(depth + 1) + "\n")
    for row in rows:
        if row[1] == index:
            if folder(row[3], row[4], row[5], row[6]):
                read(row[0], row[5], depth + 1)
            else:
                f.write(content(row[3], row[4], row[5], row[6]) + "\n")

    f.write(stars(depth) + "\n")

with con:
    read(2, "Bookmarks Menu",1)
    read(3, "Bookmarks toolbar", 1)
    read(5, "Unsorted folder", 1)

