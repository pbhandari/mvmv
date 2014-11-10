import codecs
import sqlite3
import re
from fuzzywuzzy import fuzz

def search(query):
    common_words = [
        "The",
        "Them",
        "A",
        "An",
        ]

    blacklist = [
        "BluRay",
        "1080p",
        "720p",
        "HDRip",
        "x264",
        "DVDRip",
        ]

    # Setup the sqlite database
    conn = sqlite3.connect("movies.db")
    c = conn.cursor()
    query = query.replace(".", " ")
    for term in blacklist:
        query.replace(term, "")

    m = re.search("(\d{4})", query)
    for match in m.groups():
        if match != "1080":
            year = match

    # Find the first relevant word
    word = ""
    for item in query.split(" "):
        if item not in common_words:
            word = item
            break

    c.execute("SELECT * FROM movies WHERE movies MATCH ?", 
            ["%s %s" % (word, year)])

    ratio = 0
    best = query
    for item in c:
        current = fuzz.ratio(item[0], query)
        if item[0] in query and len(item[0].split()) > 1:
            ratio = 100
            best = item[0]
        elif current > ratio:
            ratio = current
            best = item[0]
    return best

if __name__ == "__main__":
    import sys
    print(search(sys.argv[0]))