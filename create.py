#! /usr/bin/python
import sqlite3
import sys
import os
import string
import random

# Create a new blank file
open('test.sqlite', 'w+').close()

# Connect to that file
con = sqlite3.connect('test.sqlite')
cur = con.cursor()

# Create ALL of the Tables
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

# Table not sure why it exists, just leaving it for now
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

# Stupid function required to solve the guid problem for RSS feeds
def generate_guid():
	return ''.join([random.choice(string.ascii_lowercase) for i in range(12)])

# import all bookmark structure into moz_bookmarks
# Mozilla prunes moz_places to only contain entries that match moz_bookmarks
def Import_moz_bookmarks():
	# Roots
	cur.execute("INSERT INTO moz_bookmarks (id, type, parent, position, guid ) VALUES (1,2,0,0, 'root________')")
        cur.execute("INSERT INTO moz_bookmarks (id, type, parent, position, title, guid ) VALUES (2,2,1,0, 'Bookmarks Menu', 'menu________')")
        cur.execute("INSERT INTO moz_bookmarks (id, type, parent, position, title, guid ) VALUES (3,2,1,1, 'Bookmarks Toolbar', 'toolbar_____')")
        cur.execute("INSERT INTO moz_bookmarks (id, type, parent, position, title, guid ) VALUES (4,2,1,2, 'Tags', 'tags________')")
        cur.execute("INSERT INTO moz_bookmarks (id, type, parent, position, title, guid ) VALUES (5,2,1,3, 'Unsorted Bookmarks', 'unfiled_____')")

	# Generate example bookmarked pages
        # Firefox expects position ids to be 0 to N with no gaps
        # Should the parent not exist or not be a folder the link will not show
        # but will still exist 
        for i in range(0,30):
		for j in range(0,10):
			insert = "INSERT INTO moz_bookmarks (id, type, fk, parent, position ) VALUES (" + str(i * 10 + j + 26) + ", 1, " + str(10 * i + j) + ", " + str(i+6) +", "+ str(j)  +")"
			cur.execute(insert)

        # Insert Folders
        for i in range(0,10):
            	insert = "INSERT INTO moz_bookmarks (id, type, parent, position, title) VALUES (" + str(i + 6) + ", 2, 2, "+ str(i+6) + ", " + str(i) + ")"
                cur.execute(insert)

	# Generate first half of example rss feeds
        for i in range(0,10):
		random_string = generate_guid()
            	insert = "INSERT INTO moz_bookmarks (id, type, parent, position, title, guid ) VALUES (" + str(i + 16) + ", 2, 2, "+ str(i+16) + ", " + str(i) + ", '" + random_string +"')"
                cur.execute(insert)
	return

# I'm not sure why this table exists but not sure why
def Import_moz_bookmarks_roots():
	cur.execute("INSERT INTO moz_bookmarks_roots VALUES ('places', 1)")
        cur.execute("INSERT INTO moz_bookmarks_roots VALUES ('menu', 2)")
        cur.execute("INSERT INTO moz_bookmarks_roots VALUES ('toolbar', 3)")
        cur.execute("INSERT INTO moz_bookmarks_roots VALUES ('tags', 4)")
        cur.execute("INSERT INTO moz_bookmarks_roots VALUES ('unfiled', 5)")

# The second half of the bookmark question, in short the urls
# moz_bookmarks, will not display if a matching moz_places does not exist
def Import_moz_places():
	for i in range(0, 300):
            	insert = "INSERT INTO moz_places (id, url) VALUES ( " + str(i) + ", 'http://" + str(i) + ".com')"
		cur.execute(insert)

# If you want to support RSS you need the entries that have an anno_attribute_id of 9
# and if you want to see it, its expiration needs to be 4; I have no idea why
def Import_moz_items_annos():
	# Generate second half of example rss feeds
        for i in range(0,10):
            	insert = "INSERT INTO moz_items_annos (id, item_id, anno_attribute_id, content, expiration ) VALUES (" + str(i) + ", " + str(i+16) + ", 9, 'http://" + str(i) +".com/rss/link.rss', 4)"
                cur.execute(insert)
    	return

# The Indexes that must exist, otherwise problems
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

# Finishing steps otherwise Firefox is unhappy and not sure why
def Finish_Database():
	cur.execute("PRAGMA user_version = 26;")
        cur.execute("PRAGMA journal_mode = WAL;")
        con.commit()
        #con.close()

# After we are connected to the file go do your work
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

