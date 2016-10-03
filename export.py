#! /usr/bin/python
import sqlite3
import sys
import pdb

# Connect to the sqlite file
con = sqlite3.connect('places.sqlite')

# The emacs org-file we indend to use, this could be done much better
f = open('test2.org', 'w')

# Get all the shit we care about out of the database
cur = con.cursor()
cur.execute("SELECT moz_bookmarks.id, parent, position, url, content, moz_bookmarks.title, anno_attribute_id FROM moz_bookmarks LEFT JOIN moz_places ON moz_bookmarks.fk = moz_places.id LEFT JOIN moz_items_annos ON moz_bookmarks.id = moz_items_annos.item_id WHERE ifnull(anno_attribute_id, -1) in (-1, 1, 8, 9) AND parent > 1 ORDER BY parent, position;")
rows = cur.fetchall()

# Uncomment to enable debugging
#pdb.set_trace()

# Determine if a given row represents a folder
def folder(url, content, title, anno_attribute_id):

    # Deal with the special case
    if anno_attribute_id == 8:
        return True

    # Folders don't have urls
    if url <> None:
        return False

    # Folders don't have anything in content
    if content <> None:
        return False

    # Folders MUST have a Title
    if title == None:
        return False

    # Thus far in testing only folders have gotten this far, a potential bug may occur here
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
    # I am uncertain of what the values 0 and 1 mean, so I am ignoring them entirely
    
    # We know a parent value of 2 in moz_bookmarks indicates placed in Bookmarks Menu
    read(2, "Bookmarks Menu",1)
    
    # We know a parent value of 3 in moz_bookmarks indicates placed in Bookmarks toolbar
    read(3, "Bookmarks toolbar", 1)
    
    # We know a parent value of 4 in moz_bookmarks indicates item is a tag
    # But I don't feel like supporting tags at this time
    
    # We know a parent value of 5 in moz_bookmarks indicates placed in unsorted folder
    read(5, "Unsorted folder", 1)

    # All other values appear to be folders that have a parent that is another folder or one of the values above
    
