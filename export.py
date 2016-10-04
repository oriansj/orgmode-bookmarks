#! /usr/bin/python
import sqlite3
import sys
import pdb
import getopt

# Uncomment to enable debugging
# pdb.set_trace()

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

# Simple function for producing a desired number of stars
def stars(depth):

    # This code is likely wrong but it works well enough
    a = " "
    for i in range(0, depth):
        a = '*' + a

    return a

# Determine if the element is an RSS link
def rss(anno_attribute_id):

    # All of them have an anno_attribute_id of 9
    if anno_attribute_id == 9:
        return True

    # Thus far that has been the only case and I sticking with it until proven wrong
    return False

# Determine how to format our output
def content(url, content, title, anno_attribute_id):

    # if it is an rss link prepend #
    if rss(anno_attribute_id):
        return '#' + content

    # If we have a url Use That
    if url <> None:
        return url

    # Otherwise attempt to use the content
    if content <> None:
        return content

    # Attempt to use the Title information
    if title <> None:
        return title

    # Well Shit, this is clearly an unknown
    return "Unknown_Object"

# The iterative solution recursively called to our linear problem
def read(index, title, depth):
    # Strip non-ascii chars
    title = ''.join([x for x in title if ord(x) < 128])
    
    # Place the folder's name as an org section
    f.write(stars(depth) + title + "\n")

    # Ensure we can collapse subsectional lists
    f.write(stars(depth + 1) + "\n")

    # Iteratively walk down the list of all bookmarks
    for row in rows:
        # Only care about rows who's parent matches the index
        if row[1] == index:
            # If it happens to be a folder recurse
            if folder(row[3], row[4], row[5], row[6]):
                # And don't forget to increase our depth
                read(row[0], row[5], depth + 1)
            # If Not a folder simply toss it on
            else:
                f.write(content(row[3], row[4], row[5], row[6]) + "\n")

    # Add the terminating stars to deal with the long list problem
    f.write(stars(depth) + " \n")

# Place Holders for file names
inputfile = ''
outputfile = ''

# Get the System Arguments
try:
	opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile=","help"])
except getopt.GetoptError:
	print 'export.py -i <inputfile> -o <outputfile>'
	sys.exit(2)

# Parse the arguments
for opt, arg in opts:
	# Provide the standard help option
	if opt in ('-h', "--help"):
		print 'export.py -i <inputfile> -o <outputfile>'
		sys.exit()
	# Store the input file name
	elif opt in ("-i", "--ifile"):
		inputfile = arg
	# Store the output file name
	elif opt in ("-o", "--ofile"):
		outputfile = arg

# If we are missing either abort NOW
if "" == inputfile or "" == outputfile:
	print 'export.py -i <inputfile> -o <outputfile>'
	sys.exit(2)

# For the users, might remove later
print "Input file is " + inputfile.strip()
print "Output file is " + outputfile.strip()

# Connect to the input file (needs to be sqlite)
con = sqlite3.connect(inputfile.strip())

# The emacs org-file we indend to use to write our crap
f = open(outputfile.strip(), 'w')

# Get all the shit we care about out of the database
cur = con.cursor()
cur.execute("SELECT moz_bookmarks.id, parent, position, url, content, moz_bookmarks.title, anno_attribute_id FROM moz_bookmarks LEFT JOIN moz_places ON moz_bookmarks.fk = moz_places.id LEFT JOIN moz_items_annos ON moz_bookmarks.id = moz_items_annos.item_id WHERE ifnull(anno_attribute_id, -1) in (-1, 1, 8, 9) AND parent > 1 ORDER BY parent, position;")
rows = cur.fetchall()

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
