#! /usr/bin/python
import sqlite3
import sys
import os
import string
import random

open('test.sqlite', 'w+').close()
con = sqlite3.connect('test.sqlite')

cur = con.cursor()

def create_tables():
	cur.execute("CREATE TABLE moz_anno_attributes ( id INTEGER,name VARCHAR(32) NOT NULL, PRIMARY KEY(id));")
	cur.execute("CREATE TABLE moz_annos ( id INTEGER, place_id INTEGER NOT NULL, anno_attribute_id INTEGER, mime_type VARCHAR(32), content LONGVARCHAR, flags INTEGER DEFAULT '0', expiration INTEGER DEFAULT '0', type INTEGER DEFAULT '0', dateAdded INTEGER DEFAULT '0', lastModified INTEGER DEFAULT '0', PRIMARY KEY(id));")
	cur.execute("CREATE TABLE moz_bookmarks ( id INTEGER, type INTEGER, fk INTEGER, parent INTEGER, position INTEGER, title LONGVARCHAR, keyword_id INTEGER, folder_type TEXT, dateAdded INTEGER, lastModified INTEGER, guid TEXT, PRIMARY KEY(id));")
	cur.execute("CREATE TABLE moz_bookmarks_roots ( root_name VARCHAR(16), folder_id INTEGER);")
	cur.execute("CREATE TABLE moz_favicons ( id INTEGER, url LONGVARCHAR, data BLOB, mime_type VARCHAR(32), expiration LONG, guid TEXT, PRIMARY KEY(id));")
	cur.execute("CREATE TABLE moz_historyvisits ( id INTEGER, from_visit INTEGER, place_id INTEGER, visit_date INTEGER, visit_type INTEGER, session INTEGER, PRIMARY KEY(id));")
	cur.execute("CREATE TABLE moz_hosts ( id INTEGER, host TEXT NOT NULL, frecency INTEGER, typed INTEGER NOT NULL DEFAULT '0', prefix TEXT, PRIMARY KEY(id));")
	cur.execute("CREATE TABLE moz_inputhistory ( place_id INTEGER NOT NULL, input LONGVARCHAR NOT NULL, use_count INTEGER, PRIMARY KEY(place_id,input));")
	cur.execute("CREATE TABLE moz_items_annos ( id INTEGER, item_id INTEGER NOT NULL, anno_attribute_id INTEGER, mime_type VARCHAR(32), content LONGVARCHAR, flags INTEGER DEFAULT '0', expiration INTEGER DEFAULT '0', type INTEGER DEFAULT '0', dateAdded INTEGER DEFAULT '0', lastModified INTEGER DEFAULT '0', PRIMARY KEY(id));")
	cur.execute("CREATE TABLE moz_keywords ( id INTEGER PRIMARY KEY AUTOINCREMENT, keyword TEXT, place_id INTEGER, post_data TEXT);")
	cur.execute("CREATE TABLE moz_places ( id INTEGER, url LONGVARCHAR, title LONGVARCHAR, rev_host LONGVARCHAR, visit_count INTEGER DEFAULT '0', hidden INTEGER NOT NULL DEFAULT '0', typed INTEGER NOT NULL DEFAULT '0', favicon_id INTEGER, frecency INTEGER NOT NULL DEFAULT '-1', last_visit_date INTEGER, guid TEXT, foreign_count INTEGER NOT NULL DEFAULT '0', PRIMARY KEY(id));")

def Import_moz_anno_attributes():
	cur.execute("INSERT INTO moz_anno_attributes VALUES (1, 'bookmarkProperties/description')")
        cur.execute("INSERT INTO moz_anno_attributes VALUES (3, 'URIProperties/characterSet')")
        cur.execute("INSERT INTO moz_anno_attributes VALUES (4, 'places/excludeFromBackup')")
        cur.execute("INSERT INTO moz_anno_attributes VALUES (5, 'placesInternal/READ_ONLY')")
        cur.execute("INSERT INTO moz_anno_attributes VALUES (6, 'PlacesOrganizer/OrganizerFolder')")
        cur.execute("INSERT INTO moz_anno_attributes VALUES (7, 'PlacesOrganizer/OrganizerQuery')")
        cur.execute("INSERT INTO moz_anno_attributes VALUES (8, 'bookmarkPropertiesDialog/folderLastUsed')")
        cur.execute("INSERT INTO moz_anno_attributes VALUES (9, 'livemark/feedURI')")
        cur.execute("INSERT INTO moz_anno_attributes VALUES (10, 'livemark/siteURI')")

def Import_moz_bookmarks():
	return
	#cur.execute(".import moz_bookmarks.txt moz_bookmarks")

def Import_moz_bookmarks_roots():
	cur.execute("INSERT INTO moz_bookmarks_roots VALUES ('places', 1)")
        cur.execute("INSERT INTO moz_bookmarks_roots VALUES ('menu', 2)")
        cur.execute("INSERT INTO moz_bookmarks_roots VALUES ('toolbar', 3)")
        cur.execute("INSERT INTO moz_bookmarks_roots VALUES ('tags', 4)")
        cur.execute("INSERT INTO moz_bookmarks_roots VALUES ('unfiled', 5)")

def generate_guid():
	return ''.join([random.choice(string.ascii_lowercase) for i in range(16)])
        
def Import_moz_places():
	for i in range(0, 300):
		random_string = generate_guid()
            	insert = "INSERT INTO moz_places (id, url) VALUES ( " + str(i) + ", 'http://" + str(i) + ".com')"
		cur.execute(insert)

def Import_moz_items_annos():
    	return
	#cur.execute(".import moz_items_annos.txt moz_items_annos")

def Create_Indexes():
	cur.execute("CREATE INDEX moz_places_faviconindex ON moz_places (favicon_id);")
        cur.execute("CREATE INDEX moz_places_hostindex ON moz_places (rev_host);")
        cur.execute("CREATE INDEX moz_places_visitcount ON moz_places (visit_count);")
        cur.execute("CREATE INDEX moz_places_frecencyindex ON moz_places (frecency);")
        cur.execute("CREATE INDEX moz_places_lastvisitdateindex ON moz_places (last_visit_date);")
        cur.execute("CREATE INDEX moz_historyvisits_placedateindex ON moz_historyvisits (place_id, visit_date);")
        cur.execute("CREATE INDEX moz_historyvisits_fromindex ON moz_historyvisits (from_visit);")
        cur.execute("CREATE INDEX moz_historyvisits_dateindex ON moz_historyvisits (visit_date)")
        cur.execute("CREATE INDEX moz_bookmarks_itemindex ON moz_bookmarks (fk, type);")
        cur.execute("CREATE INDEX moz_bookmarks_parentindex ON moz_bookmarks (parent, position);")
        cur.execute("CREATE INDEX moz_bookmarks_itemlastmodifiedindex ON moz_bookmarks (fk, lastModified);")
        cur.execute("CREATE UNIQUE INDEX moz_places_url_uniqueindex ON moz_places (url);")
        cur.execute("CREATE UNIQUE INDEX moz_places_guid_uniqueindex ON moz_places (guid);")
        cur.execute("CREATE UNIQUE INDEX moz_bookmarks_guid_uniqueindex ON moz_bookmarks (guid);")
        cur.execute("CREATE UNIQUE INDEX moz_annos_placeattributeindex ON moz_annos (place_id, anno_attribute_id);")
        cur.execute("CREATE UNIQUE INDEX moz_items_annos_itemattributeindex ON moz_items_annos (item_id, anno_attribute_id);")
        cur.execute("CREATE UNIQUE INDEX moz_keywords_placepostdata_uniqueindex ON moz_keywords (place_id, post_data);")

def Finish_Database():
	cur.execute("PRAGMA user_version = 26;")
        cur.execute("PRAGMA journal_mode = WAL;")
        con.commit()
        #con.close()

with con:
	create_tables()
        # Data
        Import_moz_anno_attributes()
        Import_moz_bookmarks()
        Import_moz_bookmarks_roots()
        Import_moz_places()
        Import_moz_items_annos()
        
        Create_Indexes()
        Finish_Database()

