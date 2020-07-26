#!/usr/bin/python3

from bs4 import BeautifulSoup
import urllib3
import re
import sys

http = urllib3.PoolManager()

url = "https://c19study.com/"

response = http.request('GET', url)

soup = BeautifulSoup(response.data, "lxml")

# pretty output to study
pretty_html = open("Output.html", "w")
pretty_html.write(soup.prettify())
pretty_html.close()

prog_id = re.compile( "^r[0-9]+$" )
index = 1

sys.stdout.write( "\nProcessing results ..." )

results = []
titles = []
refs = []
for table_row in soup.find_all( "td"):
    # study result
    try:
        print (  set( table_row['class'] ) )
        if set( [ 'xatd' , 'xresult' ] ) & set( table_row['class'] ) == set( [ 'xatd' , 'xresult' ] ):
            results.append( table_row.contents )
    except:
        pass

    # study reference
    try:
        if table_row['class'] == [ 'xctd' , 'xref' ]:
            #print("\n\nStudy " + str(index))
            #print(table_row)
            #print(table_row.contents)

            refs.append( table_row.contents )

            index += 1
    except:
        pass

    # study title
    try:
        if table_row['class'] == [ 'xctd' , 'xtitle' ]:
            titles.append( table_row.contents )
    except:
        pass

sys.stdout.write("\nTotal titles: " + str(len(titles)) )
sys.stdout.write("\nTotal refs: " + str(len(refs)) )
sys.stdout.write("\nTotal results: " + str(len(results)) )

print('\n')